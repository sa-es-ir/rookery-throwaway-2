# Plan: Add `slugify()` helper to `textkit.slug`

## Goal
Add a stdlib-only `slugify(text: str) -> str` helper in a new `textkit` package,
a stdlib `unittest` test file, and a short README usage section. Change nothing
else, and do not commit or push.

## New/changed files
- `textkit/__init__.py` — empty package marker (required so `textkit.slug` is
  importable, including via `python -m textkit.slug`).
- `textkit/slug.py` — the helper.
- `tests/test_slug.py` — stdlib `unittest` tests, run from the repo root with
  `python -m unittest`.
- `README.md` — append a short usage section; keep all existing lines intact.

## `slugify` contract and implementation
Use exactly this stdlib-only implementation (target CPython 3.14):

```python
import re
import unicodedata


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")
```

Step by step, matching the issue:
1. `text.lower()` — lowercase.
2. `unicodedata.normalize("NFKD", ...)` then `.encode("ascii", "ignore")` —
   folds accented letters to ASCII (`café` -> `cafe`).
3. `re.sub(r"[^a-z0-9]+", "-", ...)` — every run of characters outside `a-z`/`0-9`
   becomes a single `-` (covers spaces, punctuation, underscores, and runs of
   existing dashes).
4. `.strip("-")` — removes any leading/trailing `-`.

Empty input yields `""`. No `__main__`/CLI entry point is added; the issue only
asks for the `slugify()` function.

## Tests
`tests/test_slug.py` imports `from textkit.slug import slugify`. Use a class
`SlugifyTests(unittest.TestCase)` and include `if __name__ == "__main__": unittest.main()`.
Assert these cases:

- lowercase: `"Hello World"` -> `"hello-world"`
- accent folding: `"café"` -> `"cafe"`
- non-alphanumeric runs: `"a  b---c"` -> `"a-b-c"`, and `"hello, world!"` -> `"hello-world"`
- no leading/trailing `-`: `"  hello  "` -> `"hello"`, and `"-hello-world-"` -> `"hello-world"`
- mixed: `"Héllo, Wörld!"` -> `"hello-world"`
- empty: `""` -> `""`

## README usage section
Append a short section (keep the existing heading, description, and MIT line
intact). The appended section is:

    ## Usage

    ### textkit.slug

    `slugify(text)` lowercases text, folds accented letters to ASCII, and turns any
    run of characters outside `a-z`/`0-9` into a single `-`:

        from textkit.slug import slugify

        slugify("Héllo, Wörld!")  # "hello-world"

## Verification
From the repo root:
- `python -m unittest` — passes (test count reported, exit 0).
- `git status --short` — only the four files above show. This repo has no
  `.gitignore`, so running tests creates `__pycache__`/`*.pyc`; delete any that
  appear (including any staged ones, via `git rm -r --cached <paths>` if needed)
  before finishing.
- Do not commit or push.

## Notes
- `rk:smoke-check` considered and skipped: its description is a no-op deploy
  walkthrough that does not fit ordinary code work.

Codeword: kestrel
