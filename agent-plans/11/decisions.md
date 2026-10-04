# Decisions — issue 11

## Task 1 — textkit package + wc module

- Error line uses `str(exc)` rather than `exc.strerror`, so the OSError's own repr is printed and the path ends up repeated (`textkit.wc: <path>: [Errno 2] No such file or directory: '<path>'`). Reason: keeps the errno, and `strerror` can be `None` on some OSErrors; stdlib idiom, no attribute juggling. Task 2's test only asserts non-empty stderr, so this is compatible.
- `rk:smoke-check` considered and skipped: it is a no-op deploy smoke walkthrough that does nothing useful for ordinary code work (self-described, and CLAUDE.md says to skip it). Recorded here rather than silently ignored.
- `textkit/__init__.py` written as a genuinely empty file (0 bytes) — planned, and it is the extra marker file a planned file list is often one short of.

## Task 2 — test_wc.py

- `test_wc.py` left at the repo root rather than under `tests/`, as the plan specified. On CPython 3.14 bare `python -m unittest` only recurses into packages, so a `tests/` dir would need an extra `tests/__init__.py`; a root-level `test_*.py` is discovered directly. Verified: bare `python -m unittest` finds all 5 tests and exits 0.
- The CLI test writes its fixture with `open(..., newline="")`. Reason: on Windows the default text mode translates `"\n"` to `"\r\n"`, which would make the file 13 chars instead of 12 and fail the expected `1 2 12`. Writing with `newline=""` keeps the bytes the assertions assume.
- The temp file is created under the system temp dir (`tempfile.TemporaryDirectory`) while `subprocess` runs with `cwd=ROOT`, so the `textkit` package still resolves from the repo root and the test leaves nothing behind in the worktree.

## Task 3 — README

- Wrote the section as `word-count CLI` (lowercase, matching the plan's wording) and placed it before the `Licensed under MIT.` line, so the license stays the last line of the file.
- Documented only what the plan named — the command, `count(text)`'s three keys, and the missing-file stderr/exit-1 behaviour. Left out the usage-error path (wrong argument count) and the exact error line format: the task asked for a short section, and `textkit/wc.py` is the source of truth for those details.
- `rk:smoke-check` considered and skipped again for this task too, for the same reason recorded under Task 1.
- Ran `python -m unittest` (5 tests, OK) to confirm the README edit broke nothing, then cleared the `__pycache__` dirs it created — `git status --short` shows only ` M README.md`.
