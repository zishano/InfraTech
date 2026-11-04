#!/usr/bin/env python3
"""Evidence collection and editable architecture diagrams; Python standard library only."""
import argparse
import collections
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

LIMIT = 32 * 1024 * 1024
STATUSES = {'verified', 'inferred', 'unverified'}

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def safe_url(url):
    p = urllib.parse.urlsplit(url)
    if p.scheme != 'https' or not p.hostname or p.username or p.password or p.fragment:
        raise ValueError('Sources require HTTPS URLs without embedded credentials or fragments')
    if p.query:
        raise ValueError('Use public source URLs without query strings or access tokens')
    if p.path.lower().endswith(('.safetensors', '.bin', '.pt', '.pth', '.ckpt')):
        raise ValueError('Full weight downloads are not supported; provide an index JSON instead')
    return url

def init_manifest(model, revision, github=None):
    if not re.fullmatch(r'[\w.-]+/[\w.-]+', model):
        raise ValueError('Model must be owner/repository')
    rev = urllib.parse.quote(revision, safe='')
    base = f'https://huggingface.co/{model}/resolve/{rev}/'
    sources = [dict(id=k, url=base+f, kind=kind, required=required)
               for k, f, kind, required in [
                   ('config', 'config.json', 'config', True),
                   ('model_card', 'README.md', 'documentation', False),
                   ('weight_index', 'model.safetensors.index.json', 'weight_index', False)]]
    if github:
        if not re.fullmatch(r'[\w.-]+/[\w.-]+', github):
            raise ValueError('GitHub repository must be owner/repository')
        sources.append(dict(id='github_readme', url=f'https://raw.githubusercontent.com/{github}/main/README.md', kind='documentation', required=False))
    return dict(version=1, model=model, revision=revision, sources=sources)

def collect(manifest, out):
    """Read-only bounded downloads. Never import/execute collected model code."""
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    sources = manifest['sources']; seen = set()
    # Validate all destinations before any network or file writes.
    for s in sources:
        if not re.fullmatch(r'[A-Za-z0-9_-]+', s['id']) or s['id'] in seen:
            raise ValueError('Source IDs must be unique safe filenames')
        seen.add(s['id']); safe_url(s['url'])
    results = []
    for s in sources:
        item = dict(s)
        target = out / (s['id'] + '.source')
        try:
            with urllib.request.urlopen(s['url'], timeout=45) as r:
                safe_url(r.geturl())
                data = r.read(LIMIT + 1)
                if len(data) > LIMIT:
                    raise ValueError('Source exceeds 32 MiB limit')
                # Config/index must be actual JSON, not a login page with HTTP 200.
                if s['kind'] in ('config', 'weight_index'):
                    value = json.loads(data)
                    if not isinstance(value, dict):
                        raise ValueError('Expected JSON object')
                item.update(status='downloaded', final_url=r.geturl(), bytes=len(data),
                            sha256=hashlib.sha256(data).hexdigest(), path=target.name,
                            resolved_revision=r.headers.get('x-repo-commit'))
            target.write_bytes(data)
        except (OSError, ValueError) as e:
            # Do not copy request headers, proxy credentials, or exception URLs into logs.
            item.update(status='failed', error=(f'HTTP {e.code}' if isinstance(e, urllib.error.HTTPError) else type(e).__name__))
        results.append(item)
        print(s['id'] + ': ' + item['status'])
    inventory = dict(version=1, model=manifest.get('model'), sources=results)
    write(out / 'inventory.json', inventory)
    return not any(s.get('required', False) and s['status'] != 'downloaded' for s in results)

FIELDS = {
    'hidden_size': 'hidden_size', 'num_hidden_layers': 'layers',
    'num_attention_heads': 'attention_heads', 'num_key_value_heads': 'kv_heads',
    'head_dim': 'head_dim', 'intermediate_size': 'ffn_intermediate',
    'moe_intermediate_size': 'moe_intermediate', 'n_routed_experts': 'routed_experts',
    'num_local_experts': 'routed_experts', 'num_experts_per_tok': 'active_experts',
    'n_shared_experts': 'shared_experts', 'vocab_size': 'vocab_size',
    'max_position_embeddings': 'context_config_limit', 'layer_types': 'layer_types',
    'architectures': 'architectures', 'model_type': 'model_type',
    'q_lora_rank': 'q_lora_rank', 'kv_lora_rank': 'kv_lora_rank',
}

def extract(directory):
    directory = Path(directory); inventory = read(directory / 'inventory.json')
    facts, weights = [], []
    for s in inventory['sources']:
        if s['status'] != 'downloaded' or s['kind'] not in ('config', 'weight_index'):
            continue
        path = directory / s['path']; raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != s['sha256']:
            raise ValueError('Source hash mismatch: ' + s['id'])
        obj = json.loads(raw)
        if s['kind'] == 'weight_index':
            mapping = obj.get('weight_map')
            if not isinstance(mapping, dict):
                raise ValueError('weight_index must contain weight_map')
            weights.append(dict(source=s['id'], tensor_names=len(mapping),
                                shard_count=len(set(mapping.values())),
                                # Names are useful evidence, but do not establish tensor shapes.
                                module_prefix_counts=dict(collections.Counter('.'.join(k.split('.')[:3]) for k in mapping)),
                                limitation='Index contains tensor names and shard mapping, not shapes or exact parameter counts.'))
        else:
            def walk(v, prefix=''):
                if not isinstance(v, dict):
                    return
                for k, val in v.items():
                    ptr = prefix + '/' + k.replace('~', '~0').replace('/', '~1')
                    if k in FIELDS:
                        facts.append(dict(name=FIELDS[k], value=val, status='verified',
                                          evidence=dict(source=s['id'], pointer=ptr),
                                          scope=prefix or '/'))
                    if isinstance(val, dict):
                        walk(val, ptr)
            walk(obj)
    return dict(version=1, model=inventory.get('model'), facts=facts, weight_indexes=weights,
                sources={s['id']: s.get('final_url', s.get('url', s['id'])) for s in inventory['sources'] if s['status']=='downloaded'},
                limitations=['Config declarations do not prove forward-pass connectivity.',
                             'Context config limit is not independently validated usable context.',
                             'Conflicting aliases are retained, never silently overwritten.',
                             'Attention gates, positional encoding, residual paths and expert routing require source/report review.'])

def validate(g):
    if g.get('version') != 1:
        raise ValueError('Unsupported graph version')
    w, h = g['width'], g['height']
    if any(not isinstance(x, (int, float)) or not math.isfinite(x) or x <= 0 for x in (w,h)):
        raise ValueError('Invalid canvas dimensions')
    nodes, edges = g['nodes'], g['edges']; known = {}
    sources = g.get('sources', {})
    for n in nodes:
        if not isinstance(n['id'], str) or not n['id'] or n['id'] in known or n['id'] in ('0','1'):
            raise ValueError('Duplicate / invalid node id')
        known[n['id']] = n
        x,y,nw,nh = n['box']
        if not all(isinstance(v,(float,int)) and math.isfinite(v) for v in (x,y,nw,nh)) or x<0 or y<0 or nw<=0 or nh<=0 or x+nw>w or y+nh>h:
            raise ValueError('Invalid/out-of-bounds geometry: ' + n['id'])
        if n.get('status', 'unverified') not in STATUSES:
            raise ValueError('Unknown evidence status')
        for e in n.get('evidence', []):
            if e['source'] not in sources or not e.get('locator'):
                raise ValueError('Evidence needs existing source and specific locator')
        if n.get('status') == 'verified' and not n.get('evidence'):
            raise ValueError('Verified node requires evidence: ' + n['id'])
    edge_ids = set(known) | {'0','1'}
    for i, e in enumerate(edges):
        if e['source'] not in known or e['target'] not in known:
            raise ValueError('Dangling edge')
        eid = e.get('id', f'edge_{i}')
        if eid in edge_ids:
            raise ValueError('Duplicate edge id')
        edge_ids.add(eid)
        for value in e.get('ports', [0.5,0,0.5,1]):
            if not isinstance(value,(float,int)) or not math.isfinite(value) or not 0<=value<=1:
                raise ValueError('Invalid edge port')
        if len(e.get('ports',[0.5,0,0.5,1])) != 4:
            raise ValueError('Expected four edge port coordinates')
        for x,y in e.get('points',[]):
            if not all(isinstance(v,(float,int)) and math.isfinite(v) for v in (x,y)) or not (0<=x<=w and 0<=y<=h):
                raise ValueError('Invalid edge waypoint')
    return known

DEFAULT_STYLE = 'rounded=1;whiteSpace=wrap;html=0;fillColor=#eef4fb;strokeColor=#6685a9;fontFamily=Arial;fontSize=20;'

def drawio(g, path):
    validate(g)
    f=ET.Element('mxfile', host='app.diagrams.net', type='device')
    d=ET.SubElement(f,'diagram',id='architecture',name=g['title'])
    m=ET.SubElement(d,'mxGraphModel',grid='1',gridSize='10',page='1',pageScale='1',pageWidth=str(g['width']),pageHeight=str(g['height']))
    r=ET.SubElement(m,'root'); ET.SubElement(r,'mxCell',id='0'); ET.SubElement(r,'mxCell',id='1',parent='0')
    for n in g['nodes']:
        style=n.get('style',DEFAULT_STYLE)
        if n.get('kind') == 'decoration':
            style+='architectureDecoration=1;'
        if n.get('status') == 'unverified' and n.get('kind') != 'decoration':
            style+='dashed=1;'
        c=ET.SubElement(r,'mxCell',id=n['id'],value=n['label'],style=style,vertex='1',parent='1')
        x,y,w,h=n['box'];ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    for i,e in enumerate(g['edges']):
        a,b,c,d=e.get('ports',[.5,0,.5,1])
        routing='segmentEdgeStyle' if e.get('points') else 'orthogonalEdgeStyle'
        style=f'edgeStyle={routing};html=0;endArrow=block;endFill=1;strokeColor=#333333;fontColor=#333333;strokeWidth=1;fontSize=7;labelBackgroundColor=#ffffff;exitX={a};exitY={b};entryX={c};entryY={d};'
        if e.get('dashed'):style+='dashed=1;'
        cell=ET.SubElement(r,'mxCell',id=e.get('id',f'edge_{i}'),source=e['source'],target=e['target'],value=e.get('label',''),edge='1',parent='1',style=style)
        geo=ET.SubElement(cell,'mxGeometry',relative='1',attrib={'as':'geometry'})
        if e.get('points'):
            arr=ET.SubElement(geo,'Array',attrib={'as':'points'})
            for x,y in e['points']:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
    ET.indent(f);ET.ElementTree(f).write(path,encoding='utf-8',xml_declaration=True)

def parse_style(s):
    return dict(part.split('=',1) for part in s.split(';') if '=' in part)

def draft(facts):
    """Make an explicitly incomplete review scaffold, never guess a forward graph."""
    nodes=[dict(id='input',label='Model inputs — verify modalities',box=[300,620,600,70],status='unverified'),
           dict(id='pending',label='Architecture review required\nRead forward() / technical report\nExpand branches, gates, residuals and caches',box=[300,330,600,170],status='unverified'),
           dict(id='output',label='Model outputs — verify task / heads',box=[300,180,600,70],status='unverified')]
    for i,f in enumerate(facts['facts']):
        nodes.append(dict(id=f'fact_{i}',label=f'{f["scope"]}: {f["name"]} = {json.dumps(f["value"],ensure_ascii=False)}',box=[50,800+i*90,1100,70],status='verified',evidence=[dict(source=f['evidence']['source'],locator=f['evidence']['pointer'])]))
    return dict(version=1,title=(facts.get('model') or 'New model')+' — INCOMPLETE architecture scaffold',width=1200,height=max(1000,850+len(facts['facts'])*90),nodes=nodes,
                edges=[dict(source='input',target='pending',dashed=True),dict(source='pending',target='output',dashed=True)],sources=facts.get('sources',{}),
                limitations=['The three placeholder nodes and their edges are unverified, not a generated model architecture.','Config facts retain their nested scopes; review conflicts before replacing placeholders.'])

def svg(g, path):
    known=validate(g)
    r=ET.Element('svg',xmlns='http://www.w3.org/2000/svg',width=str(g['width']),height=str(g['height']),viewBox=f'0 0 {g["width"]} {g["height"]}')
    ET.SubElement(r,'title').text=g['title']
    defs=ET.SubElement(r,'defs');marker=ET.SubElement(defs,'marker',id='arrow',markerWidth='8',markerHeight='8',refX='7',refY='4',orient='auto')
    ET.SubElement(marker,'path',d='M0,0 L8,4 L0,8 Z',fill='#43546b')
    ET.SubElement(r,'rect',width='100%',height='100%',fill='white')
    # Backgrounds first, connectors next, foreground nodes last.
    def node(n):
        s=parse_style(n.get('style',DEFAULT_STYLE));x,y,w,h=n['box']
        if not n.get('style','').startswith('text;'):
            tag='ellipse' if s.get('shape')=='ellipse' else 'rect'
            a=dict(fill=s.get('fillColor','#eef4fb'),stroke=s.get('strokeColor','#6685a9'))
            if tag=='rect':a.update(x=str(x),y=str(y),width=str(w),height=str(h),rx='8')
            else:a.update(cx=str(x+w/2),cy=str(y+h/2),rx=str(w/2),ry=str(h/2))
            if s.get('dashed')=='1' or n.get('status')=='unverified':a['stroke-dasharray']='7 5'
            ET.SubElement(r,tag,**a)
        fs=float(s.get('fontSize',20)); lines=[]
        for line in n['label'].split('\n'):
            lines.extend(textwrap.wrap(line,max(1,int((w-12)/(fs*.56)))) or [''])
        for i,line in enumerate(lines):
            t=ET.SubElement(r,'text',x=str(x+w/2),y=str(y+h/2+(i-(len(lines)-1)/2)*fs*1.12+fs*.33),attrib={'text-anchor':'middle','font-family':'Arial, sans-serif','font-size':str(fs),'fill':s.get('fontColor','#152337')})
            t.text=line
    for n in g['nodes']:
        if n.get('kind')=='decoration':node(n)
    for e in g['edges']:
        a,b,c,d=e.get('ports',[.5,0,.5,1]);sn,tn=known[e['source']]['box'],known[e['target']]['box']
        sx,sy=sn[0]+sn[2]*a,sn[1]+sn[3]*b;tx,ty=tn[0]+tn[2]*c,tn[1]+tn[3]*d
        mid=e.get('points') or ([(sx,(sy+ty)/2),(tx,(sy+ty)/2)] if b in (0,1) and d in (0,1) else [((sx+tx)/2,sy),((sx+tx)/2,ty)])
        pts=[(sx,sy),*mid,(tx,ty)]
        attrs={'points':' '.join(f'{x},{y}' for x,y in pts),'fill':'none','stroke':'#43546b','stroke-width':'1.5','marker-end':'url(#arrow)'}
        if e.get('dashed'):attrs['stroke-dasharray']='7 5'
        ET.SubElement(r,'polyline',**attrs)
        if e.get('label'):
            ET.SubElement(r,'text',x=str((sx+tx)/2),y=str((sy+ty)/2-5),attrib={'font-size':'16','text-anchor':'middle'}).text=e['label']
    for n in g['nodes']:
        if n.get('kind')!='decoration':node(n)
    ET.indent(r);ET.ElementTree(r).write(path,encoding='utf-8',xml_declaration=True)

def render(g, out):
    validate(g);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    drawio(g,out/'architecture.drawio');svg(g,out/'architecture.svg')
    text=['# '+g['title'],'','This is a reviewed conceptual graph, not an executed model trace.','']
    for n in g['nodes']:
        if n.get('kind')=='decoration':continue
        text.append(f'- **{n["id"]}** [{n.get("status","unverified")}]: '+n['label'].replace('\n',' / '))
        for e in n.get('evidence',[]):text.append(f'  - {e["source"]}: {e["locator"]}')
    text+=['','## Sources','']+[f'- {k}: {v}' for k,v in g.get('sources',{}).items()]
    text+=['','## Limitations','']+['- '+s for s in g.get('limitations',[])]
    (out/'evidence.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    prompt='Authoritative architecture PNGs MUST be exported from architecture.drawio using export-png. Do not independently generate or edit their computational content with an image model. Image generation is permitted only for separate style references explicitly labelled non-authoritative.\n'
    (out/'image_prompt.txt').write_text(prompt,encoding='utf-8')

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('init');a.add_argument('model');a.add_argument('--revision',default='main');a.add_argument('--github');a.add_argument('--out',required=True)
    a=sub.add_parser('collect');a.add_argument('manifest');a.add_argument('--out',required=True)
    a=sub.add_parser('extract');a.add_argument('directory');a.add_argument('--out',required=True)
    a=sub.add_parser('validate');a.add_argument('graph')
    a=sub.add_parser('draft');a.add_argument('facts');a.add_argument('--out',required=True)
    a=sub.add_parser('render');a.add_argument('graph');a.add_argument('--out',required=True)
    a=sub.add_parser('export-png');a.add_argument('drawio');a.add_argument('--out',required=True);a.add_argument('--mxgraph',default='/workspace/.cache/model-architecture-renderer/node_modules/mxgraph/javascript/src');a.add_argument('--scale',type=float,default=2);a.add_argument('--browser',default='/usr/bin/chromium')
    a=sub.add_parser('verify-png');a.add_argument('drawio');a.add_argument('png');a.add_argument('manifest')
    a=p.parse_args()
    try:
        if a.command=='init':write(a.out,init_manifest(a.model,a.revision,a.github))
        elif a.command=='collect':return 0 if collect(read(a.manifest),a.out) else 2
        elif a.command=='extract':write(a.out,extract(a.directory))
        elif a.command=='draft':write(a.out,draft(read(a.facts)))
        elif a.command=='validate':validate(read(a.graph));print('Graph valid')
        elif a.command=='render':render(read(a.graph),a.out);print('Rendered draw.io, SVG, evidence report and illustration prompt')
        elif a.command=='export-png':
            from png_export import export
            print(json.dumps(export(a.drawio,a.out,mxgraph=a.mxgraph,scale=a.scale,browser=a.browser)))
        elif a.command=='verify-png':
            from png_export import verify
            verify(a.drawio,a.png,a.manifest);print('PNG and draw.io hashes match export manifest')
    except (OSError,ValueError,KeyError,TypeError,ImportError) as e:
        print(f'Error: {e}',file=sys.stderr);return 1
    return 0

if __name__=='__main__':sys.exit(main())
