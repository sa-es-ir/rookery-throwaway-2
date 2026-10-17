# Plan: textkit.roman — Roman numerals (issue #18)

## Goal
Add `textkit/roman.py` exposing `to_roman(n: int) -> str` and `from_roman(s: str) -> int` for 1..3999, with stdlib `unittest` tests. The package `textkit/` does not exist yet — this change creates it.

## Contract (from the issue, plus repo conventions)
- `to_roman(n)`: the canonical Roman numeral for `n`. Raises `ValueError` if `n` is not an `int` or is outside 1..3999.
- `from_roman(s)`: the value of a canonical Roman numeral, case-insensitive. Raises `ValueError` for non-`str` input, the empty string, and any non-canonical form (`IIII`, `VX`, `IVIV`, `ABC`, …).
- Round trip: `from_roman(to_roman(n)) == n` for every n in 1..3999.
- Library-only module. No CLI / `__main__` block — the issue asks for none.
- Errors are `ValueError` with a clear message raised from the library functions; no tracebacks, no sentinels.

## Approach
- `to_roman`: greedy descent over the fixed table
  `[(1000,"M"), (900,"CM"), (500,"D"), (400,"CD"), (100,"C"), (90,"XC"), (50,"L"), (40,"XL"), (10,"X"), (9,"IX"), (5,"V"), (4,"IV"), (1,"I")]`.
- `from_roman`: reject non-`str`/empty input; `t = s.upper()`; validate with
  `re.fullmatch(r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})", t)`
  (this accepts exactly the canonical forms and bounds the result to 1..3999 by construction); then sum with the subtractive rule — subtract a letter whose value is less than the value of the letter after it, otherwise add.

## Files (complete list)
- `textkit/__init__.py` — new, empty. Package marker; required for `python -m textkit.roman` and normal imports.
- `textkit/roman.py` — new.
- `tests/__init__.py` — new, empty. **Required**: on CPython 3.14 `python -m unittest` discovers 0 tests and exits 5 without it.
- `tests/test_roman.py` — new.
- `README.md` — add a short section documenting the module (README is authoritative for documented behaviour).

## Tests (stdlib `unittest` only, no third-party deps)
- Known values: 1→I, 4→IV, 9→IX, 14→XIV, 40→XL, 90→XC, 400→CD, 900→CM, 1994→MCMXCIV, 3999→MMMCMXCIX.
- `to_roman` raises `ValueError` for 0, -1, 4000, and non-int input (e.g. `"5"`, `None`).
- `from_roman` raises `ValueError` for `""`, `"IIII"`, `"VX"`, `"IVIV"`, `"ABC"`, and non-str input.
- Case-insensitivity: `"mcmxciv"` → 1994, `"iv"` → 4.
- Round trip `from_roman(to_roman(n)) == n` for all n in 1..3999, using `subTest` inside one test method.

## Working rules (repo-specific — follow exactly)
- Work from this worktree root: `C:\Users\Saeed\source\repos\rookery\work\sa-es-ir_rookery-throwaway-2\issue-18`.
- Run tests from the repo root with `python -m unittest`. A good run prints a test count > 0 and exits 0. If it reports 0 tests and exits 5, `tests/__init__.py` is missing.
- **Do not commit or push.** The orchestrator owns commits; leave the working tree ready.
- After finishing a task, append one line to `agent-plans/18/decisions.md` (create the file if it does not exist; never rewrite existing contents) saying what was done and any deviation from this plan.
- The repo has no `.gitignore`: running anything creates `__pycache__` dirs that show up untracked. Before finishing, run `git status --short` and remove them with
  `find . -name '__pycache__' -not -path './.git/*' -type d -exec rm -rf {} +`.
- `rk:smoke-check` was considered and skipped: it is a self-described no-op deploy smoke walkthrough whose description does not fit ordinary code work.

Codeword: kestrel
