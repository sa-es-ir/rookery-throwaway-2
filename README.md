# rookery-throwaway-2
Rookery live-test scratch repo

Licensed under MIT.

## textkit

`textkit.wc` counts lines, words, and characters in a UTF-8 text file:

    python -m textkit.wc FILE

It prints the three counts (`lines words chars`) on one line and exits 0.
A missing or unreadable file prints an error to stderr and exits 1; wrong
usage prints a usage line to stderr and exits 2.

The same counts are available as a function:

    from textkit.wc import count
    count("hello world\nsecond line\n")
    # {'lines': 2, 'words': 4, 'chars': 24}

`count(text)` returns a dict with keys `lines`, `words`, and `chars`, and
raises `ValueError` if `text` is not a string.

## textkit.roman

Library-only (`textkit/roman.py`, no CLI) — import `to_roman` / `from_roman`.

- `to_roman(n: int) -> str`: canonical Roman numeral for `n` in 1..3999; `ValueError` otherwise (non-ints too).
- `from_roman(s: str) -> int`: value of a canonical numeral, case-insensitive; `ValueError` for non-str, empty, or non-canonical input (e.g. `""`, `"IIII"`, `"VX"`).
