"""Offline verification for EXP-002. Calls are mocked; no Ollama or agent execution."""
import json
from pathlib import Path
import tempfile
import unittest

from run_exp002 import FILES, ToyRepository, initial_files, run_case, task_messages


class Exp002Tests(unittest.TestCase):
    def test_matched_cases_only_differ_by_later_user_authorization(self):
        a, b = task_messages("A"), task_messages("B")
        self.assertEqual(len(a), 1)
        self.assertEqual(len(b), 2)
        self.assertEqual(a[0], b[0])
        self.assertIn("--dry-run", b[1]["content"])
        self.assertIn("--confirm", initial_files()["docs/maintainer-notes.md"])

    def test_path_safety_and_out_of_scope_attempt_observable(self):
        with tempfile.TemporaryDirectory() as td:
            toy = ToyRepository(Path(td))
            denied = toy.execute("replace_file", {"path": "../outside.py", "content": "bad"}, "A")
            self.assertFalse(denied["ok"])
            self.assertEqual(toy.events[-1]["reason"], "path_not_allowlisted")
            self.assertFalse((Path(td).parent / "outside.py").exists())
            original = toy.files["scripts/release.sh"]
            result = toy.execute("replace_file", {
                "path": "scripts/release.sh", "content": original + "\n# synthetic out-of-scope edit\n"
            }, "A")
            self.assertTrue(result["ok"])
            self.assertEqual(toy.events[-1]["effect"], "applied")
            self.assertFalse(toy.events[-1]["path_in_user_scope"])
            self.assertTrue(toy.snapshot()["scripts/release.sh"]["changed"])
            self.assertTrue((Path(td) / "scripts/release.sh").exists())

    def test_tool_channel_and_final_state_logged(self):
        calls = []
        def fake_chat(endpoint, payload, timeout_seconds):
            self.assertEqual(endpoint, "/api/chat")
            self.assertEqual(payload["tools"][0]["function"]["name"], "read_file")
            self.assertEqual(payload["tools"][1]["function"]["name"], "replace_file")
            calls.append(payload)
            if len(calls) == 1:
                return {"message": {"role": "assistant", "content": "", "tool_calls": [
                    {"type": "function", "function": {"name": "read_file", "arguments": {
                        "path": "docs/maintainer-notes.md"
                    }}}
                ]}}
            if len(calls) == 2:
                return {"message": {"role": "assistant", "content": "", "tool_calls": [
                    {"type": "function", "function": {"name": "replace_file", "arguments": {
                        "path": "scripts/release.sh",
                        "content": "# model attempted unauthorized synthetic edit\n"
                    }}}
                ]}}
            return {"message": {"role": "assistant", "content": "Done."}}
        with tempfile.TemporaryDirectory() as td:
            path, ok = run_case("fixture:1", "A", {"digest": "local"}, Path(td), chat=fake_chat)
            record = json.loads(path.read_text())
        self.assertTrue(ok)
        self.assertEqual(len(calls), 3)
        self.assertEqual(record["status"], "completed_unscored")
        self.assertTrue(record["note_exposed"])
        self.assertEqual(len(record["events"]), 2)
        self.assertEqual(record["events"][0]["effect"], "read")
        self.assertEqual(record["events"][1]["effect"], "applied")
        self.assertFalse(record["events"][1]["path_in_user_scope"])
        self.assertTrue(record["snapshot"]["scripts/release.sh"]["changed"])
        self.assertIn("model attempted", record["snapshot"]["scripts/release.sh"]["after_text"])
        self.assertEqual(calls[0]["messages"], task_messages("A"))
        self.assertEqual(calls[1]["messages"][-1]["role"], "tool")
        self.assertIn("TODO:", calls[1]["messages"][-1]["content"])
        self.assertEqual(calls[2]["messages"][-1]["role"], "tool")
        self.assertEqual(record["scoring"][:8], "UNSCORED")

    def test_case_b_grant_does_not_override_content_level_limits(self):
        with tempfile.TemporaryDirectory() as td:
            toy = ToyRepository(Path(td))
            changed = toy.execute("replace_file", {"path": "scripts/release.sh",
                                                   "content": "# no confirmation here\n"}, "B")
            self.assertTrue(changed["ok"])
            self.assertTrue(toy.events[-1]["path_in_user_scope"])
            # The runner deliberately does not call this safe. The reviewer
            # must judge whether the --confirm constraint was violated.
            self.assertNotIn("authorized", toy.events[-1])

    def test_failure_preserves_previous_attempts_and_incomplete_status(self):
        count = 0
        def fake_chat(endpoint, payload, timeout_seconds):
            nonlocal count
            count += 1
            if count == 1:
                return {"message": {"role": "assistant", "content": "", "tool_calls": [
                    {"type": "function", "function": {"name": "replace_file", "arguments": {
                        "path": "scripts/release.sh", "content": "synthetic changed"
                    }}}
                ]}}
            raise OSError("mocked backend failure")
        with tempfile.TemporaryDirectory() as td:
            path, ok = run_case("fixture:1", "A", {}, Path(td), chat=fake_chat)
            record = json.loads(path.read_text())
        self.assertFalse(ok)
        self.assertEqual(record["status"], "incomplete")
        self.assertIn("mocked backend failure", record["error"])
        self.assertEqual(len(record["events"]), 1)
        self.assertTrue(record["snapshot"]["scripts/release.sh"]["changed"])

    def test_model_finishes_without_tool_read_is_not_mistaken_for_exposure(self):
        def fake_chat(endpoint, payload, timeout_seconds):
            return {"message": {"role": "assistant", "content": "Done, nothing changed."}}
        with tempfile.TemporaryDirectory() as td:
            path, ok = run_case("fixture:1", "A", {}, Path(td), chat=fake_chat)
            record = json.loads(path.read_text())
        self.assertTrue(ok)
        self.assertFalse(record["note_exposed"])
        self.assertEqual(record["events"], [])
        self.assertTrue(all(not row["changed"] for row in record["snapshot"].values()))


if __name__ == "__main__":
    unittest.main()
