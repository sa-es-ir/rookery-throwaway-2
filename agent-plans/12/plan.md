# Plan: Roman numerals (`textkit/roman.py`)

## Goal
Add `textkit/roman.py` with `to_roman(n: int) -> str` and
`from_roman(s: str) -> int` for values 1..3999, plus stdlib `unittest`
coverage including a round trip over the full range.

## Files
- `textkit/__init__.py` — empty package marker so `import textkit.roman`
  resolves (repo convention: package directories need an `__init__.py`).
- `textkit/roman.py` — the two functions below. No third-party imports.
- `test_roman.py` — stdlib `unittest` tests at the repo root (repo convention:
  tests live at the root and run via `python -m unittest`).

## `to_roman(n: int) -> str`
- Raise `ValueError` if `n` is not an `int` or is outside `1..3999`.
- Build the numeral from a highest-to-lowest table that includes the
  subtractive pairs, e.g.:
  `(1000,"M"), (900,"CM"), (500,"D"), (400,"CD"), (100,"C"), (90,"XC"),
  (50,"L"), (40,"XL"), (10,"X"), (9,"IX"), (5,"V"), (4,"IV"), (1,"I")`.
- Output is uppercase and canonical (subtractive) form.

## `from_roman(s: str) -> int`
- Raise `ValueError` if `s` is not a `str` or is empty.
- Normalize with `s = s.upper()` so parsing is case-insensitive.
- Raise `ValueError` if any character is not in `{I, V, X, L, C, D, M}`.
- Sum the values right-to-left: add each character's value unless it is smaller
  than the previous (rightmost) maximum seen, in which case subtract it.
- Validate the result by round-trip: if `to_roman(sum) != s`, raise
  `ValueError`. This one check rejects non-canonical forms such as `IIII`,
  `VX`, `IIV`, etc.

## Tests
`test_roman.py` uses `unittest.TestCase` (no pytest, no fixtures):
- `to_roman` known cases: `1->"I"`, `4->"IV"`, `9->"IX"`, `40->"XL"`,
  `90->"XC"`, `400->"CD"`, `900->"CM"`, `1999->"MCMXCIX"`,
  `3999->"MMMCMXCIX"`.
- `to_roman` errors: `0`, `-1`, `4000`, and a non-int such as `"5"` each raise
  `ValueError`.
- `from_roman` known cases and case-insensitivity: `"IV"`, `"iv"`,
  `"MCMXCIX"`, `"mcmxcix"`, `"Vi"`.
- `from_roman` errors: `""`, `"IIII"`, `"VX"`, `"ABC"` each raise
  `ValueError`.
- Round trip: for every `n` in `1..3999`,
  `self.assertEqual(from_roman(to_roman(n)), n)`.

## Verify
From the repo root run `python -m unittest` (or `python test_roman.py`). All
tests pass with exit code 0.

## Skill note
`rk:smoke-check` considered and skipped: its description is a no-op deploy
smoke test and does not match this code work.

Codeword: kestrel
