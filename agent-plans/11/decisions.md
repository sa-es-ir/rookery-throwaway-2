# Decisions — issue 11

## Task 1 — textkit package + wc module

- Error line uses `str(exc)` rather than `exc.strerror`, so the OSError's own repr is printed and the path ends up repeated (`textkit.wc: <path>: [Errno 2] No such file or directory: '<path>'`). Reason: keeps the errno, and `strerror` can be `None` on some OSErrors; stdlib idiom, no attribute juggling. Task 2's test only asserts non-empty stderr, so this is compatible.
- `rk:smoke-check` considered and skipped: it is a no-op deploy smoke walkthrough that does nothing useful for ordinary code work (self-described, and CLAUDE.md says to skip it). Recorded here rather than silently ignored.
- `textkit/__init__.py` written as a genuinely empty file (0 bytes) — planned, and it is the extra marker file a planned file list is often one short of.
