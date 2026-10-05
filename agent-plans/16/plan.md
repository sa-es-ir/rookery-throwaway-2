# Plan: issue #16 — add a `slugify()` helper

## Goal

Add `textkit/slug.py` exporting `slugify(text: str) -> str`, a stdlib-only test
suite `tests/test_slug.py` that runs with `python -m unittest`, and a short
usage section in `README.md`. Nothing else changes.

## Current state

The repo root contains only `README.md` (4 lines), `CLAUDE.md`, `.claude/`,
`.rookery/`, and `agent-plans/1/`. **There is no `textkit/` package and no
`tests/` directory yet** — both are created by this plan. Python is CPython
3.14 on PATH as `python` (no `python3` alias). Run everything from the
worktree root.

## Decisions

- **Accent folding**: `unicodedata.normalize("NFKD", text)` then drop
  combining marks (`unicodedata.combining(c) == 0`). Standard library only.
- **Behaviour follows the issue literally**: after folding, every run of
  characters outside `[a-z0-9]` becomes one `-`, then leading/trailing `-`
  are stripped. So characters with no ASCII decomposition (`ß`, `æ`, `ø`,
  CJK, …) collapse into `-` (e.g. `"Straße"` -> `"stra-e"`), and input that
  folds to nothing (`"!!!"`, `""`) returns `""`. This is intended, not a bug.
- **No CLI / `__main__` block in `slug.py`** — the issue asks for a library
  helper only. README documents the Python API.
- **Do not commit or push.** The orchestrator owns commits. Leave the working
  tree ready and report via `STATUS:` line.
- **`rk:smoke-check` skill: considered and skipped** — it is a no-op deploy
  smoke walkthrough whose description does not match this work.
- Files are written as UTF-8 (the Write tool does this; if scripting in
  Python, pass `encoding="utf-8"` explicitly).

## Files to create / change

### 1. `textkit/__init__.py` — new, empty file

Empty (zero bytes). Package marker so `textkit.slug` imports cleanly.

### 2. `textkit/slug.py` — new

```python
"""textkit.slug - turn arbitrary text into URL-friendly slugs."""

import re
import unicodedata

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Return the URL slug for *text*.

    Lowercases; folds accented Latin letters to ASCII ("cafe" from "café");
    collapses every run of characters outside [a-z0-9] into a single "-";
    strips leading and trailing "-". Input that folds to nothing (e.g. "!!!")
    returns "".
    """
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_only = "".join(c for c in decomposed if not unicodedata.combining(c))
    return _NON_ALNUM.sub("-", ascii_only.lower()).strip("-")
```

(Note: the docstring may contain the literal character `é` instead of the
`é` escape — either is fine, just keep the file UTF-8.)

### 3. `tests/__init__.py` — new, empty file

Empty (zero bytes). **Required**: on CPython 3.14, bare `python -m unittest`
discovers 0 tests and exits 5 without it.

### 4. `tests/test_slug.py` — new

```python
"""Tests for textkit.slug.slugify."""

import unittest

from textkit.slug import slugify


class SlugifyTests(unittest.TestCase):
    def test_lowercases_plain_words(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_folds_accents_to_ascii(self):
        self.assertEqual(slugify("café"), "cafe")
        self.assertEqual(slugify("ÀÉÎÕÜ"), "aeiou")
        self.assertEqual(slugify("Naïve—Tête"), "naive-tete")

    def test_collapses_runs_of_non_alnum_to_one_dash(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")
        self.assertEqual(slugify("a  --  b"), "a-b")
        self.assertEqual(slugify("Version 2.3"), "version-2-3")

    def test_strips_leading_and_trailing_dashes(self):
        self.assertEqual(slugify("--hello--"), "hello")
        self.assertEqual(slugify("  Many   spaces -- and  dashes "), "many-spaces-and-dashes")

    def test_keeps_digits(self):
        self.assertEqual(slugify("CamelCase 42"), "camelcase-42")

    def test_empty_and_all_symbol_inputs_return_empty(self):
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify("!!!"), "")

    def test_combined_example(self):
        self.assertEqual(slugify("  Café Corner — Menu (5)  "), "cafe-corner-menu-5")


if __name__ == "__main__":
    unittest.main()
```

Keep test inputs inside the Latin-1 range (as above): the console on this box
is cp1252, and while slug *outputs* are always ASCII, printing non-cp1252
*inputs* in a failure message would raise `UnicodeEncodeError`. Do not add CJK
test inputs.

### 5. `README.md` — replace with exactly this content

````
# rookery-throwaway-2
Rookery live-test scratch repo

Licensed under MIT.

## textkit

Small text helpers (standard library only).

### slugify

```python
from textkit.slug import slugify

slugify("Café Corner — Menu!")  # -> 'cafe-corner-menu'
```

Rules: lowercase; accented Latin letters fold to ASCII (`café` -> `cafe`);
every run of characters that are not `a-z` or `0-9` becomes one `-`; no
leading or trailing `-`. Characters with no ASCII decomposition (`ß`, `æ`,
non-Latin scripts) collapse into `-` like any other non-alphanumeric run, so
`slugify("!!!")` and `slugify("")` both return `""`.
````

## Verified behaviour (checked on this box, CPython 3.14)

| input | output |
|---|---|
| `"café"` | `"cafe"` |
| `"Hello, World!"` | `"hello-world"` |
| `"  Many   spaces -- and  dashes "` | `"many-spaces-and-dashes"` |
| `"Naïve—Tête"` | `"naive-tete"` |
| `"ÀÉÎÕÜ"` | `"aeiou"` |
| `"Version 2.3"` | `"version-2-3"` |
| `"CamelCase 42"` | `"camelcase-42"` |
| `"123"` | `"123"` |
| `"--hello--"` | `"hello"` |
| `"!!!"` | `""` |
| `""` | `""` |
| `"Straße"` | `"stra-e"` (known: `ß` has no ASCII decomposition) |
| `"  Café Corner — Menu (5)  "` | `"cafe-corner-menu-5"` |
| `"日本語"` | `""` |

## Commands

From the worktree root:

- Sanity check a single value:
  `python -c "from textkit.slug import slugify; print(slugify('Café Corner — Menu!'))"`
  (prints `cafe-corner-menu`).
- Run the suite: `python -m unittest` — expect `Ran 7 tests` (one per method
  above), `OK`, exit 0. `python -m unittest discover -s tests -t . -v` also
  works. **0 tests + exit 5 means `tests/__init__.py` is missing.**
- Clean bytecode afterwards (the repo has no `.gitignore`; `__pycache__`
  shows up untracked and must not be left behind or committed):
  `find . -name '__pycache__' -not -path './.git/*' -type d -exec rm -rf {} +`

## Repo rules for every task

- After each task, run the `__pycache__` cleanup above, then check
  `git status --short`: the only changes should be the files listed in this
  plan (plus `agent-plans/16/`).
- Append one line to `agent-plans/16/decisions.md` per task (create the file
  with that line if it does not exist; never rewrite existing contents)
  recording what was done and any deviation from this plan.
- Do not commit, push, or stage anything.
- Out of scope, leave untouched: `sentry-was-here.txt` if present,
  `.rookery/NOTES.md`, `agent-plans/<other numbers>/`.
- Report status with a `STATUS:` first line.

Codeword: kestrel
