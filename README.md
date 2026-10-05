# rookery-throwaway-2
Rookery live-test scratch repo

Licensed under MIT.

## textkit.roman

Library-only (`textkit/roman.py`, no CLI) — import `to_roman` / `from_roman`.

- `to_roman(n: int) -> str`: canonical Roman numeral for `n` in 1..3999; `ValueError` otherwise (non-ints too).
- `from_roman(s: str) -> int`: value of a canonical numeral, case-insensitive; `ValueError` for non-str, empty, or non-canonical input (e.g. `""`, `"IIII"`, `"VX"`).
