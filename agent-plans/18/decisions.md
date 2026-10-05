# Decisions — from plan.md: "Plan: textkit.roman — Roman numerals (issue #18)"

- Task 1: created empty `textkit/__init__.py` and `textkit/roman.py` per plan (greedy table, canonical regex + subtractive sum); no `__main__` block. Sanity-checked via `python -B -c` (known values, error cases, full 1..3999 round trip); `-B` used so no `__pycache__` is left behind. Real test suite is task 2.
- Booleans are not special-cased in `to_roman`: `isinstance(True, int)` is True, so `to_roman(True)` returns `"I"`. The plan's contract keys on the isinstance check and its non-int examples are only `"5"`/`None`, so adding a bool guard would exceed the plan.
- `rk:smoke-check` considered and skipped — self-described no-op deploy walkthrough, doesn't fit code work (already noted in plan.md; repeated here for the record).
- Marked task 1's checkbox in `agent-plans/18/tasks.md`; left the other tasks untouched.
- Task 2: created empty `tests/__init__.py` and `tests/test_roman.py` with the full plan list (known values both directions, to_roman ValueError for 0/-1/4000/non-int, from_roman ValueError for ""/IIII/VX/IVIV/ABC/non-str, case-insensitivity, 1..3999 round trip with subTest). 8 tests, `python -m unittest` → OK, exit 0. `__pycache__` cleaned after.
- rk:smoke-check considered and skipped again — no-op deploy walkthrough, not relevant to writing tests.
