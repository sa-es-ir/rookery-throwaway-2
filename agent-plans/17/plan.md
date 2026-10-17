# Plan: G-d word-count CLI (`textkit/wc.py`)

Issue #17: add `textkit/wc.py` with a `count()` function and a
`python -m textkit.wc FILE` CLI, tests with stdlib `unittest` (including the
CLI exit code), and a README section documenting the command.

## Current state

- No `textkit/` package and no `tests/` directory exist yet; this change
  creates both.
- `README.md` is three lines (title, description, `Licensed under MIT.`).
- Python is CPython 3.14 (`python` on PATH, no `python3` alias). Stdlib only.

## Decisions (binding — implement exactly this)

- **Line semantics**: `lines = len(text.splitlines())`. So `"hello"` is 1
  line, `"a\nb"` is 2, `"a\nb\n"` is 2, `""` is 0. (Chosen over
  newline-counting `wc -l` semantics; documented in README.)
- `words = len(text.split())` (any whitespace), `chars = len(text)` (chars of
  the decoded string, not bytes).
- `count(text)` raises `ValueError` for non-`str` input (repo convention:
  library functions reject invalid input with `ValueError`).
- CLI reads the file as UTF-8 text (default universal newlines), so `\r\n`
  files count the same as `\n` files.
- Exit codes: 0 on success; **1** when the file is missing/unreadable
  (`OSError` caught, message to stderr, no traceback); 2 on wrong usage
  (usage line to stderr). Error format: `wc: {path}: {exc}`.
- Entry point uses `main(argv=None) -> int` with an
  `if __name__ == "__main__": sys.exit(main())` guard, so
  `python -m textkit.wc FILE` works and `main()` is testable.
- No new dependencies. No commits — leave the working tree ready.

## Files

1. **`textkit/__init__.py`** — new, empty. Required so
   `python -m textkit.wc` imports.
2. **`textkit/wc.py`** — new, exactly this:

   ```python
   """Count lines, words, and characters in a text file.

   Usage: python -m textkit.wc FILE
   """

   import sys


   def count(text: str) -> dict:
       """Return {'lines': L, 'words': W, 'chars': C} for *text*.

       Raises ValueError if *text* is not a str.
       """
       if not isinstance(text, str):
           raise ValueError("text must be a str")
       return {
           "lines": len(text.splitlines()),
           "words": len(text.split()),
           "chars": len(text),
       }


   def main(argv=None) -> int:
       argv = sys.argv[1:] if argv is None else list(argv)
       if len(argv) != 1:
           print("usage: python -m textkit.wc FILE", file=sys.stderr)
           return 2
       path = argv[0]
       try:
           with open(path, "r", encoding="utf-8") as handle:
               text = handle.read()
       except OSError as exc:
           print(f"wc: {path}: {exc}", file=sys.stderr)
           return 1
       totals = count(text)
       print(f"{totals['lines']} {totals['words']} {totals['chars']}")
       return 0


   if __name__ == "__main__":
       sys.exit(main())
   ```

3. **`tests/__init__.py`** — new, empty. Required: on CPython 3.14 bare
   `python -m unittest` discovers 0 tests and exits 5 without it.
4. **`tests/test_wc.py`** — new, exactly this:

   ```python
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
   ```

   Expected numbers (verified): `SAMPLE` is 24 chars (11 + 1 + 11 + 1),
   2 lines, 4 words. Reading back through universal newlines keeps the counts
   identical on Windows (`\r\n` on disk) and POSIX.
5. **`README.md`** — append the following after the `Licensed under MIT.`
   line (blank line between):

   ````markdown
   ## textkit

   `textkit.wc` counts lines, words, and characters in a UTF-8 text file:

       python -m textkit.wc FILE

   It prints the three counts (`lines words chars`) on one line and exits 0.
   A missing or unreadable file prints an error to stderr and exits 1; wrong
   usage prints a usage line to stderr and exits 2.

   The same counts are available as a function:

       from textkit.wc import count
       count("hello world\nsecond line\n")
       # {'lines': 2, 'words': 4, 'chars': 24}

   `count(text)` returns a dict with keys `lines`, `words`, and `chars`, and
   raises `ValueError` if `text` is not a string.
   ````

## Working rules (apply to every task)

- Work from the worktree root (this directory). Never commit or push.
- Run the suite from the repo root: `python -m unittest` — expect 6 tests,
  exit 0. A count of 0 with exit 5 means `tests/__init__.py` is missing.
- After finishing your task, append one line to
  `agent-plans/17/decisions.md` describing what you did and any deviation.
  Create it (header `# Decisions for issue 17`) only if it does not exist;
  never rewrite existing content.
- **`__pycache__` trap**: the repo has no `.gitignore`. Before finishing, run
  `find . -name '__pycache__' -not -path './.git/*' -type d -exec rm -rf {} +`
  and make sure no `.pyc` files appear in `git status --short`.
- Do not add a `.gitignore` as part of this change.
- `rk:smoke-check` was considered and explicitly skipped: it is a no-op
  deploy smoke walkthrough, not relevant to this code change.
- `agent-plans/17/plan.md` and `tasks.md` already exist from planning; the
  only new files are the four listed above plus `decisions.md` and the README
  edit.

## Verification (final task)

- `python -m unittest` from the repo root: 6 tests, exit 0.
- `python -m textkit.wc README.md` prints one line of three integers, exit 0.
- `python -m textkit.wc no-such-file.txt` prints `wc: ...` to stderr, exit 1.
- `git status --short` shows exactly: modified `README.md`, untracked
  `textkit/` (2 files), `tests/` (2 files), and `agent-plans/17/decisions.md`.
  No `__pycache__`, no `.pyc`.

Codeword: kestrel
