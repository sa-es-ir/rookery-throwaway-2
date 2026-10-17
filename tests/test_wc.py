"""Tests for textkit.wc."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from textkit.wc import count

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE = "hello world\nsecond line\n"


class CountTests(unittest.TestCase):
    def test_counts_basic(self):
        self.assertEqual(count(SAMPLE), {"lines": 2, "words": 4, "chars": 24})

    def test_counts_empty(self):
        self.assertEqual(count(""), {"lines": 0, "words": 0, "chars": 0})

    def test_no_trailing_newline_still_one_line(self):
        self.assertEqual(count("hello"), {"lines": 1, "words": 1, "chars": 5})

    def test_non_string_rejected(self):
        with self.assertRaises(ValueError):
            count(123)


class CliTests(unittest.TestCase):
    def run_wc(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "textkit.wc", *args],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )

    def test_file_prints_counts_and_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.txt"
            path.write_text(SAMPLE, encoding="utf-8")
            proc = self.run_wc(str(path))
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "2 4 24")

    def test_missing_file_exits_one_with_stderr(self):
        proc = self.run_wc("definitely-missing-file.txt")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("definitely-missing-file.txt", proc.stderr)


if __name__ == "__main__":
    unittest.main()
