"""New-model scaffolds must preserve uncertainty and existing user work."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
import model_architecture as a
from workflow import create_study

class StudyWorkflowTests(unittest.TestCase):
    def test_baseline_target_are_separate_and_no_topology_is_invented(self):
        target=a.init_manifest('example/NewModel','new-pinned-revision','example/NewRepo')
        baseline=a.init_manifest('example/OldModel','old-pinned-revision')
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)/'study'
            files=create_study(target,out,baseline)
            self.assertEqual(len(files),4)
            self.assertEqual(a.read(out/'sources.json'),target)
            self.assertEqual(a.read(out/'baseline.sources.json'),baseline)
            review=a.read(out/'review.json')
            self.assertEqual(review['status'],'pending')
            self.assertTrue(all(item['status']=='pending' and item['evidence']==[] for item in review['checks'].values()))
            self.assertIsNone(review['architecture']['main_layers'])
            self.assertEqual(review['architecture']['attention_paths'],[])
            self.assertEqual(review['version_diff']['additions'],[])
            self.assertEqual(review['optimization_claims'],[])
            self.assertFalse(review['source_policy']['execute_remote_code'])
            self.assertFalse(any(out.glob('*.png')))
            self.assertFalse(any(out.glob('*.drawio')))
            self.assertIn('未执行', (out/'architecture_review.md').read_text())

    def test_existing_review_is_preserved_before_any_other_file_is_written(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)
            (out/'review.json').write_text('existing human review')
            with self.assertRaises(FileExistsError):create_study(a.init_manifest('example/Model','main'),out)
            self.assertEqual((out/'review.json').read_text(),'existing human review')
            self.assertEqual({p.name for p in out.iterdir()},{'review.json'})

    def test_cli_wires_single_model_and_rejects_orphan_baseline_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)/'single'
            result=subprocess.run([sys.executable,str(BASE/'model_architecture.py'),'init-study','example/Model','--out',str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(a.read(out/'review.json')['requested_revision'],'main')
            self.assertIsNone(a.read(out/'review.json')['baseline'])
            review=a.read(out/'review.json')
            policy=review['drawing_policy']
            self.assertEqual(len(policy['rule_ids']),12)
            self.assertEqual(len(set(policy['rule_ids'])),12)
            markdown=(out/'architecture_review.md').read_text()
            for rule in policy['rule_ids']:
                key='drawing_'+rule
                self.assertEqual(review['checks'][key]['status'],'pending')
                self.assertEqual(review['checks'][key]['evidence'],[])
                self.assertIn('- [ ] `'+key+'`',markdown)
            presentation=review['presentation']
            self.assertEqual(presentation['background'],'#ffffff')
            self.assertEqual(presentation['group_fill'],'none')
            self.assertEqual(presentation['flow'],'bottom-up')
            self.assertIn('×N',presentation['repetition'])
            self.assertIn('native edge labels',presentation['edge_dimensions'])
            self.assertIn('compact',presentation['spacing'])
            self.assertIsNone(presentation['implementation_view'])
            self.assertFalse((out/'baseline.sources.json').exists())
            invalid=Path(directory)/'invalid'
            result=subprocess.run([sys.executable,str(BASE/'model_architecture.py'),'init-study','example/Model','--baseline-revision','old-revision','--out',str(invalid)],capture_output=True,text=True)
            self.assertEqual(result.returncode,1)
            self.assertIn('requires --baseline',result.stderr)
            self.assertFalse(invalid.exists())

if __name__=='__main__':unittest.main()
