# Tasks

- [x] Create `textkit/__init__.py` (empty package marker) and `textkit/roman.py` implementing `to_roman(n: int) -> str` and `from_roman(s: str) -> int` exactly as specified in `plan.md` (range 1..3999; `ValueError` on out-of-range or invalid input; case-insensitive `from_roman`; round-trip validation).
- [x] Create `test_roman.py` at the repo root with the stdlib `unittest` cases listed in `plan.md`, including the `from_roman(to_roman(n)) == n` round trip over 1..3999.
- [ ] From the repo root run `python -m unittest`; fix any failures until all tests pass, then commit the three new files (`textkit/__init__.py`, `textkit/roman.py`, `test_roman.py`).
