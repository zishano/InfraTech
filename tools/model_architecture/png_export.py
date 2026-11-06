"""Render native uncompressed draw.io XML with mxGraph, not a second diagram engine."""
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
import xml.etree.ElementTree as ET


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_layout(layout):
    """Reject measured text overflow/tight padding and unintended diagonal edges."""
    for key in ('text_overflow', 'tight_text', 'nonorthogonal_segments', 'edge_node_crossings'):
        if not isinstance(layout.get(key), list):
            raise ValueError(f'Missing or invalid layout measurements: {key}')
        if layout.get(key):
            names=', '.join(item['id'] for item in layout[key][:8])
            raise ValueError(f'Layout check failed ({key}): {names}')
    for key in ('edge_label_node_overlaps', 'edge_label_overlaps'):
        if layout.get(key):
            raise ValueError(f'Layout check failed ({key}): {layout[key][:8]}')


def inspect_drawio(path):
    data=Path(path).read_bytes()
    if len(data)>32*1024*1024 or b'<!DOCTYPE' in data or b'<!ENTITY' in data:
        raise ValueError('Unsupported or oversized XML')
    doc=ET.fromstring(data)
    model=doc if doc.tag=='mxGraphModel' else doc.find('./diagram/mxGraphModel')
    if model is None:
        raise ValueError('Expected native uncompressed draw.io XML; export an uncompressed XML page first')
    cells=model.findall('./root/mxCell')
    ids={c.get('id') for c in cells}
    if len(ids)!=len(cells):raise ValueError('Duplicate XML cell IDs')
    for c in cells:
        for key in ('source','target','parent'):
            if c.get(key) and c.get(key) not in ids:raise ValueError('Dangling XML reference')
        style=c.get('style','')
        if c.get('vertex')=='1' and ('shape=image' in style or 'image=' in style or style.startswith('image;')):
            raise ValueError('Embedded image nodes are not accepted as editable architecture source')
    return model, sum(c.get('vertex')=='1' for c in cells), sum(c.get('edge')=='1' for c in cells)


def verify(drawio_path,png_path,manifest_path):
    m=json.loads(Path(manifest_path).read_text())
    if m.get('version')!=1:raise ValueError('Unsupported export manifest')
    if m['drawio_sha256']!=digest(drawio_path):raise ValueError('draw.io changed after PNG export')
    if m['png_sha256']!=digest(png_path):raise ValueError('PNG changed after export')
    if m.get('layout_file'):
        if Path(m['layout_file']).name != m['layout_file']:raise ValueError('Invalid layout report filename')
        layout_path=Path(manifest_path).parent/m['layout_file']
        if digest(layout_path)!=m['layout_sha256']:raise ValueError('Layout report changed after export')
        layout=json.loads(layout_path.read_text())
        if layout['drawio_sha256']!=m['drawio_sha256']:raise ValueError('Layout report belongs to a different XML')
        validate_layout(layout)
    return m


def export(drawio_path,png_path,*,mxgraph,scale=2,browser='/usr/bin/chromium'):
    """Requires Playwright + a local mxgraph@4.2.2 npm install. Network-free rendering."""
    from playwright.sync_api import sync_playwright
    if scale<=0 or scale>4:raise ValueError('Scale must be in (0, 4]')
    model,vertices,edges=inspect_drawio(drawio_path)
    width=int(float(model.get('pageWidth','1200')));height=int(float(model.get('pageHeight','1600')))
    if not (1<=width<=10000 and 1<=height<=10000):raise ValueError('Unsupported page size')
    assets=Path(mxgraph).resolve()
    if not (assets/'js/mxClient.js').is_file():raise ValueError('mxgraph/javascript/src/js/mxClient.js not found; see README')
    package_path=assets.parents[1]/'package.json'
    package=json.loads(package_path.read_text())
    if package.get('name')!='mxgraph' or package.get('version')!='4.2.2':
        raise ValueError('Expected pinned mxgraph@4.2.2 assets')
    html=b'''<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:white}#graph{position:relative;background:white;overflow:hidden}</style>
<script>var mxBasePath='/mxgraph';var mxLoadResources=false;var mxLoadStylesheets=false;</script>
<script src="/mxgraph/js/mxClient.js"></script><div id="graph"></div>'''
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            if self.path=='/':
                data=html;kind='text/html; charset=utf-8'
            elif self.path.startswith('/mxgraph/') and '?' not in self.path:
                f=(assets/self.path[len('/mxgraph/'):]).resolve()
                if not f.is_relative_to(assets) or not f.is_file():self.send_error(404);return
                data=f.read_bytes();kind='text/javascript' if f.suffix=='.js' else 'application/octet-stream'
            else:self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    url=f'http://127.0.0.1:{server.server_port}'
    png_path=Path(png_path);png_path.parent.mkdir(parents=True,exist_ok=True)
    try:
        with sync_playwright() as p:
            b=p.chromium.launch(executable_path=browser,headless=True,args=['--no-sandbox'])
            browser_version=b.version
            try:
                page=b.new_page(viewport={'width':width,'height':height},device_scale_factor=scale)
                # Remote image/font/style references in a document cannot make requests.
                page.route('**/*',lambda route: route.continue_() if route.request.url.startswith(url+'/') else route.abort())
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(url+'/',wait_until='networkidle')
                page.wait_for_function("typeof mxGraph === 'function'")
                result=page.evaluate('''({xml,width,height})=>{
                    mxObjectCodec.allowEval=false;
                    const container=document.getElementById('graph');
                    container.style.width=width+'px';container.style.height=height+'px';
                    const graph=new mxGraph(container);graph.setEnabled(false);
                    const doc=mxUtils.parseXml(xml);new mxCodec(doc).decode(doc.documentElement,graph.getModel());
                    graph.refresh();window.renderedGraph=graph;
                    const cells=Object.values(graph.getModel().cells);
                    return {vertices:cells.filter(c=>c.vertex).length,edges:cells.filter(c=>c.edge).length};
                }''',dict(xml=ET.tostring(model,encoding='unicode'),width=width,height=height))
                if errors or result!=dict(vertices=vertices,edges=edges):
                    raise ValueError('mxGraph render failed or lost nodes/edges')
                page.evaluate('document.fonts.ready')
                layout=page.evaluate('''()=>{
                    const graph=window.renderedGraph, overflow=[], tight=[], routes=[], boxes=[], edgeLabels=[];
                    const base=document.getElementById('graph').getBoundingClientRect();
                    for(const cell of Object.values(graph.getModel().cells)){
                        const state=graph.view.getState(cell);
                        if(!state)continue;
                        if(cell.vertex && Number(state.style.architectureDecoration)!==1)boxes.push({id:cell.id,x:state.x,y:state.y,width:state.width,height:state.height});
                        if(cell.vertex && state.text && state.text.node && cell.value){
                            const b=state.text.node.getBoundingClientRect();
                            const r={x:b.x-base.x,y:b.y-base.y,width:b.width,height:b.height};
                            const excess=Math.max(state.x-r.x,state.y-r.y,r.x+r.width-state.x-state.width,r.y+r.height-state.y-state.height);
                            if(excess>1.5)overflow.push({id:cell.id,text:cell.value,box:{x:state.x,y:state.y,width:state.width,height:state.height},textBox:r,excess});
                            const margin=Math.min(r.x-state.x,r.y-state.y,state.x+state.width-r.x-r.width,state.y+state.height-r.y-r.height);
                            if(margin<2)tight.push({id:cell.id,margin,text:cell.value,box:{x:state.x,y:state.y,width:state.width,height:state.height},textBox:r});
                        }
                        if(cell.edge && state.absolutePoints){
                            if(cell.value && state.text && state.text.node){
                                const b=state.text.node.getBoundingClientRect();
                                edgeLabels.push({id:cell.id,text:cell.value,x:b.x-base.x,y:b.y-base.y,width:b.width,height:b.height});
                            }
                            const points=state.absolutePoints.filter(Boolean).map(p=>[p.x,p.y]);
                            routes.push({id:cell.id,source:cell.source.id,target:cell.target.id,points});
                        }
                    }
                    const nonorthogonal=[];
                    for(const route of routes)for(let i=1;i<route.points.length;i++){
                        const a=route.points[i-1],b=route.points[i];
                        if(Math.abs(a[0]-b[0])>0.05 && Math.abs(a[1]-b[1])>0.05)
                            nonorthogonal.push({id:route.id,source:route.source,target:route.target,segment:[a,b]});
                    }
                    const crossings=[];
                    for(const route of routes)for(let i=1;i<route.points.length;i++){
                        const a=route.points[i-1],b=route.points[i];
                        for(const box of boxes){
                            if(box.id===route.source || box.id===route.target)continue;
                            const left=box.x+1,right=box.x+box.width-1,top=box.y+1,bottom=box.y+box.height-1;
                            const vertical=Math.abs(a[0]-b[0])<0.05 && left<a[0] && a[0]<right && Math.max(Math.min(a[1],b[1]),top)<Math.min(Math.max(a[1],b[1]),bottom);
                            const horizontal=Math.abs(a[1]-b[1])<0.05 && top<a[1] && a[1]<bottom && Math.max(Math.min(a[0],b[0]),left)<Math.min(Math.max(a[0],b[0]),right);
                            if(vertical || horizontal)crossings.push({id:route.id,source:route.source,target:route.target,crossed_node:box.id});
                        }
                    }
                    const intersects=(a,b)=>Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x)>1 && Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y)>1;
                    const labelNodes=[],labelPairs=[];
                    for(const l of edgeLabels)for(const b of boxes)if(intersects(l,b))labelNodes.push({id:l.id,node:b.id});
                    for(let i=0;i<edgeLabels.length;i++)for(let j=i+1;j<edgeLabels.length;j++)if(intersects(edgeLabels[i],edgeLabels[j]))labelPairs.push({id:edgeLabels[i].id,other:edgeLabels[j].id});
                    return {text_overflow:overflow,tight_text:tight,nonorthogonal_segments:nonorthogonal,edge_node_crossings:crossings,edge_label_node_overlaps:labelNodes,edge_label_overlaps:labelPairs,edge_labels:edgeLabels,routes};
                }''')
                layout['drawio_sha256']=digest(drawio_path)
                png_path.with_suffix('.layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n')
                validate_layout(layout)
                page.locator('#graph').screenshot(path=str(png_path))
            finally:b.close()
    finally:
        server.shutdown();server.server_close();thread.join(timeout=5)
    # The next export verifies that a modified PNG or draw.io is never silently paired.
    manifest=dict(version=1,drawio_file=Path(drawio_path).name,png_file=png_path.name,
                  drawio_sha256=digest(drawio_path),png_sha256=digest(png_path),
                  renderer='mxGraph 4.2.2 / Chromium',browser_version=browser_version,scale=scale,width=width,height=height,
                  vertices=vertices,edges=edges)
    manifest.update(layout_file=png_path.with_suffix('.layout.json').name,
                    layout_sha256=digest(png_path.with_suffix('.layout.json')),
                    layout_check={'text_overflow':0,'tight_text':0,'nonorthogonal_segments':0,'edge_node_crossings':0,'edge_label_node_overlaps':0,'edge_label_overlaps':0})
    target=png_path.with_suffix('.export.json')
    target.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    verify(drawio_path,png_path,target)
    return manifest
