# Decisions — issue 10

- Task 1: `textkit/__init__.py` created as a genuinely empty file (0 bytes) — the plan calls it an "empty package marker" and nothing needs to re-export `slugify`, so no `__all__`/import was added.
- Task 1: ran `python -c` to sanity-check `slugify` rather than writing a scratch test file; deleted the `__pycache__` it created (repo has no `.gitignore`) so `git status --short` shows only `textkit/` and the pre-existing `agent-plans/10/`.
- Task 2: added an empty `tests/__init__.py` beyond the plan's four-file list. Without it, bare `python -m unittest` from the repo root discovers 0 tests and exits 5 (`unittest` discovery only recurses into packages in CPython 3.14; `discover -s tests` raises "Start directory is not importable"), so the plan's own verification step would have failed for task 4. Same rationale as `textkit/__init__.py` — a zero-byte package marker. 6 tests now run, exit 0.
