"""Tests for textkit.wc."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from textkit.wc import count

ROOT = Path(__file__).resolve().parent


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "textkit.wc", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


class CountTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count(""), {"lines": 0, "words": 0, "chars": 0})

    def test_single_line(self):
        self.assertEqual(
            count("hello world\n"), {"lines": 1, "words": 2, "chars": 12}
        )

    def test_trailing_blanks(self):
        self.assertEqual(count("a\nb\n\n"), {"lines": 3, "words": 2, "chars": 5})


class CliTests(unittest.TestCase):
    def test_counts_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.txt"
            # newline="" so "\n" is not translated to "\r\n" on Windows.
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write("hello world\n")
            result = run_cli(str(path))
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "1 2 12")

    def test_missing_file(self):
        missing = str(ROOT / "no-such-file.txt")
        result = run_cli(missing)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.strip())


if __name__ == "__main__":
    unittest.main()
