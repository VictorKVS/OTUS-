import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TRACE_MODULE=ROOT/"agents"/"runtime"/"telegram-voice-bridge"/"tracing.py"
spec=importlib.util.spec_from_file_location('voice_bridge_tracing',TRACE_MODULE)
module=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

class TraceWriterTest(unittest.TestCase):
    def test_text_is_redacted_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'trace.jsonl'
            writer=module.TraceWriter(path,capture_content=False)
            meta=writer.text_meta('секретный тест')
            self.assertNotIn('text',meta)
            self.assertTrue(meta['content_redacted'])
            self.assertEqual(meta['text_chars'],len('секретный тест'))

    def test_event_contract_has_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'trace.jsonl'
            writer=module.TraceWriter(path,capture_content=False)
            trace_id=writer.new_trace_id()
            writer.event(trace_id,'unit.test','PASS',metadata={'x':1})
            item=json.loads(path.read_text(encoding='utf-8').strip())
            for field in ('trace_id','event_id','timestamp','agent_id','event','status','metadata'):
                self.assertIn(field,item)
            self.assertEqual(item['trace_id'],trace_id)
            self.assertEqual(item['agent_id'],'FTH-AG-VBR-001')

if __name__=='__main__':
    unittest.main()