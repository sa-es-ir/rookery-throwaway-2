# Decisions — issue 12

- `to_roman` explicitly rejects `bool` (`isinstance(n, bool)`) even though
  `bool` is an `int` subclass: `to_roman(True)` returning `"I"` is a silent
  wrong answer, and the plan's contract is "raise `ValueError` if `n` is not
  an `int`" at a trust boundary. No test in the plan covers it, so this is an
  addition, not a change to the spec.
- `from_roman` uses the plan's round-trip check (`to_roman(total) != s`) as the
  only canonical-form validation — no separate regex/state machine. One check
  rejects `IIII`, `VX`, `IIV`, `MMMM`, etc.
- Non-canonical/out-of-charset input is reported through the same `ValueError`
  with the uppercased string in the message; the plan fixes the exception type
  but not the message text.
- Task 2 (`test_roman.py`) was left untouched. This task was verified with a
  throwaway `python -c` script covering the plan's known cases, the error
  cases, and the full 1..3999 round trip; it is not committed.
- `rk:smoke-check` considered and skipped (no-op deploy smoke walkthrough, does
  not match this code work) — matches the plan's skill note.
