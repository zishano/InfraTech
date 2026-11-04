import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as E

BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('arch',BASE/'model_architecture.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

class Response(io.BytesIO):
    headers={'x-repo-commit':'abc123'}
    def geturl(self):return 'https://example.org/config.json'

class WorkflowTests(unittest.TestCase):
    def test_collect_extract_nested_and_conflicting_facts(self):
        raw=(BASE/'tests/fixtures/config.json').read_bytes()
        manifest={'model':'test/model','sources':[{'id':'config','url':'https://example.org/config.json','kind':'config','required':True}]}
        with tempfile.TemporaryDirectory() as d, patch.object(a.urllib.request,'urlopen',return_value=Response(raw)):
            self.assertTrue(a.collect(manifest,d))
            inv=a.read(Path(d)/'inventory.json')['sources'][0]
            self.assertEqual(inv['resolved_revision'],'abc123')
            self.assertEqual(inv['sha256'],hashlib.sha256(raw).hexdigest())
            facts=a.extract(d)['facts']
            self.assertEqual([f['value'] for f in facts if f['name']=='hidden_size'],[4096,1024])
            self.assertEqual([f['value'] for f in facts if f['name']=='routed_experts'],[16,32])
            self.assertTrue(any(f['evidence']['pointer']=='/text_config/hidden_size' for f in facts))
            (Path(d)/'config.source').write_text('{}')
            with self.assertRaisesRegex(ValueError,'hash mismatch'):a.extract(d)

    def test_weight_index_names_are_not_shapes(self):
        raw=(BASE/'tests/fixtures/index.json').read_bytes()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'index.source').write_bytes(raw)
            a.write(p/'inventory.json',{'sources':[dict(id='index',kind='weight_index',status='downloaded',path='index.source',sha256=hashlib.sha256(raw).hexdigest())]})
            result=a.extract(d)['weight_indexes'][0]
            self.assertEqual(result['tensor_names'],3);self.assertEqual(result['shard_count'],2)
            self.assertIn('not shapes',result['limitation'])

    def test_reject_download_and_path_hazards(self):
        for url in ['http://example.org/config.json','https://token@example.org/config.json','https://example.org/model.safetensors','https://example.org/config.json?token=secret']:
            with self.assertRaises(ValueError):a.safe_url(url)
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):a.collect({'sources':[dict(id='../escape',url='https://example.org/config.json')]},d)

    def test_failure_is_retained_not_fake_success(self):
        m={'sources':[dict(id='config',url='https://example.org/config.json',kind='config',required=True)]}
        with tempfile.TemporaryDirectory() as d, patch.object(a.urllib.request,'urlopen',side_effect=OSError('sensitive diagnostic')):
            self.assertFalse(a.collect(m,d))
            result=a.read(Path(d)/'inventory.json')['sources'][0]
            self.assertEqual(result['status'],'failed');self.assertEqual(result['error'],'OSError')

    def test_graph_and_both_editable_exports(self):
        g=a.read(BASE/'examples/kimi_k3.graph.json')
        with tempfile.TemporaryDirectory() as d:
            a.render(g,d)
            cells=E.parse(Path(d)/'architecture.drawio').findall('.//mxCell')
            self.assertEqual(sum(c.get('vertex')=='1' for c in cells),len(g['nodes']))
            self.assertEqual(sum(c.get('edge')=='1' for c in cells),len(g['edges']))
            self.assertFalse(any('shape=image' in c.get('style','') for c in cells))
            E.parse(Path(d)/'architecture.svg')
            self.assertIn('unverified', (Path(d)/'evidence.md').read_text())
        for name in ['q','k','v','alpha','beta']:
            self.assertTrue(any(e['source']=='kda_port_'+name and e['target']=='kda_core' for e in g['edges']))
        self.assertFalse(any(e['source']=='moe_router' and e['target']=='moe_down' for e in g['edges']))
        self.assertFalse(any(e['target']=='ar_query' for e in g['edges']))

    def test_validation_rejects_missing_evidence_and_dangling_edge(self):
        g=a.read(BASE/'examples/kimi_k3.graph.json');g['edges'][0]['target']='absent'
        with self.assertRaisesRegex(ValueError,'Dangling'):a.validate(g)
        g=a.read(BASE/'examples/kimi_k3.graph.json');g['nodes'][0]['status']='verified';g['nodes'][0]['evidence']=[]
        with self.assertRaisesRegex(ValueError,'requires evidence'):a.validate(g)
        g=a.read(BASE/'examples/kimi_k3.graph.json');g['nodes'][0]['box'][2]=1e9
        with self.assertRaisesRegex(ValueError,'geometry'):a.validate(g)

    def test_new_model_scaffold_does_not_claim_unknown_topology(self):
        facts=a.extract(BASE/'tests/fixtures')
        g=a.draft(facts)
        a.validate(g)
        self.assertIn('INCOMPLETE',g['title'])
        self.assertEqual(g['nodes'][1]['status'],'unverified')
        self.assertTrue(all(e['dashed'] for e in g['edges']))
        self.assertEqual(sum(n['status']=='verified' for n in g['nodes']),len(facts['facts']))
        with tempfile.TemporaryDirectory() as d:
            a.render(g,d)
            self.assertIn('Architecture review required',(Path(d)/'evidence.md').read_text())

if __name__=='__main__':unittest.main()
