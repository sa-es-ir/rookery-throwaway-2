# Tasks — issue #16 (read `agent-plans/16/plan.md` first; it holds all file contents and rules)

- [x] Task 1 — Create the `textkit` package per plan.md "Files to create / change" items 1–2: an empty `textkit/__init__.py` and `textkit/slug.py` with the exact `slugify()` implementation from the plan; sanity-check with the plan's `python -c` command (expect `cafe-corner-menu`), then follow plan.md "Repo rules" (`__pycache__` cleanup, `git status --short`, append a line to `agent-plans/16/decisions.md`, no commits).

- [x] Task 2 — Add the test suite per plan.md items 3–4: an empty `tests/__init__.py` (mandatory on CPython 3.14 or `python -m unittest` finds 0 tests and exits 5) and `tests/test_slug.py` with the exact `SlugifyTests` class from the plan; run `python -m unittest` from the worktree root and confirm 7 tests, `OK`, exit 0; then follow plan.md "Repo rules" (cleanup, status check, `decisions.md` line, no commits).

- [ ] Task 3 — Replace `README.md` with the exact final content from plan.md item 5 (adds the `## textkit` / `### slugify` usage section, keeps the MIT line); re-run `python -m unittest` to confirm the suite still passes, then follow plan.md "Repo rules": `__pycache__` cleanup, confirm `git status --short` shows only `README.md`, `textkit/`, `tests/` and `agent-plans/16/`, stage/commit nothing, append the final `decisions.md` line.
