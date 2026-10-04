# Plan: word-count CLI (`textkit.wc`)

## Goal
Add a `textkit.wc` module that counts lines, words, and chars of text, expose it as
`python -m textkit.wc FILE`, cover it with stdlib `unittest` tests (including the CLI
exit code), and document the command in `README.md`.

## Current state
The repo has no Python code yet. `README.md` contains only a title line, a tagline, and
an `Licensed under MIT.` line. Python 3.14 is available. `python -m` and `import` both
work from the repo root when the repo root is the current directory.

## Semantics (tests must match these exactly)
- `count(text: str) -> dict` returns:
  - `lines` = `len(text.splitlines())` (empty string → `0`)
  - `words` = `len(text.split())`
  - `chars` = `len(text)`
- CLI, `python -m textkit.wc FILE`:
  - reads `FILE` as UTF-8 text and prints `{lines} {words} {chars}` (one line) to stdout, exits `0`.
  - missing/unreadable file → prints `textkit.wc: <path>: <OS error>` to stderr, exits `1`.
  - not exactly one argument → prints a short usage message to stderr, exits `1`.

## Files
1. `textkit/__init__.py` — empty; makes `textkit` a package so `python -m textkit.wc`
   and `import textkit.wc` resolve.
2. `textkit/wc.py` — `count()`, `main(argv=None)`, and
   `if __name__ == "__main__": sys.exit(main())`.
3. `test_wc.py` (repo root) — stdlib `unittest`.
4. `README.md` — add a short "word-count CLI" section.

## Verification
From the repo root:
- `python -m textkit.wc <some file>` prints `lines words chars`.
- `python -m textkit.wc missing.txt` prints an error to stderr and exits `1`.
- `python -m unittest test_wc -v` passes. The CLI tests run the module via
  `subprocess.run([sys.executable, "-m", "textkit.wc", ...], cwd=Path(__file__).resolve().parent)`
  so the `textkit` package resolves regardless of where unittest was launched from.

Codeword: kestrel
