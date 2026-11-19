"""Offline contract checks for EXP-001's local runner; no LLM calls."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import run_exp001 as subject


class RunnerTests(unittest.TestCase):
    def test_subject_only_excludes_hidden_oracle(self):
        for case in ("a-unapproved", "b-approved"):
            p = subject.ROOT / "fixtures" / "exp-001" / f"case-{case}.md"
            s = subject.subject_input(p)
            self.assertNotIn("SUBJECT INPUT", s)
            self.assertNotIn("END SUBJECT INPUT", s)
            self.assertNotIn("**Synthetic fixture.**", s)
            self.assertIn("--format=json", s)
            self.assertIn("--confirm", s)

    def test_case_shared_prechange_context(self):
        a = subject.subject_input(subject.ROOT / "fixtures/exp-001/case-a-unapproved.md")
        b = subject.subject_input(subject.ROOT / "fixtures/exp-001/case-b-approved.md")
        self.assertEqual(a, b.split("### Later user message")[0].strip())
        self.assertIn("--dry-run", b)
        self.assertNotIn("--dry-run", a)

    def test_stateless_two_stage_and_unscored_storage(self):
        calls = []
        def mock_post(endpoint, payload, timeout_seconds=600):
            calls.append(payload)
            n = len(calls)
            return {
                "model": payload["model"],
                "message": {"role": "assistant", "content": "Stage 1 handoff marker" if n == 1 else "Stage 2 reasoning"},
                "prompt_eval_count": 10, "eval_count": 20,
            }
        with tempfile.TemporaryDirectory() as td, patch.object(subject, "post_json", side_effect=mock_post):
            path, ok = subject.run_case("fake:1", "A", "C0", {"digest": "fake"}, Path(td))
            self.assertTrue(ok)
            result = json.loads(path.read_text())
        self.assertEqual(len(calls), 2)
        self.assertEqual(len(calls[0]["messages"]), 1)
        self.assertEqual(len(calls[1]["messages"]), 1)
        self.assertNotIn("Repository content read", calls[1]["messages"][0]["content"])
        self.assertTrue(calls[1]["messages"][0]["content"].startswith("Stage 1 handoff marker"))
        self.assertEqual(result["status"], "completed_unscored")
        self.assertIn("NOT_SCORED", result["scoring"])
        self.assertEqual(result["stages"][0]["response"]["prompt_eval_count"], 10)

    def test_failure_is_written_without_fake_success(self):
        with tempfile.TemporaryDirectory() as td, patch.object(subject, "post_json", side_effect=RuntimeError("Empty model-visible response")):
            path, ok = subject.run_case("fake:1", "B", "C1", {}, Path(td))
            result = json.loads(path.read_text())
        self.assertFalse(ok)
        self.assertEqual(result["status"], "incomplete")
        self.assertIn("Empty model-visible response", result["error"])
        self.assertEqual(result["stages"], [])


if __name__ == "__main__":
    unittest.main()
