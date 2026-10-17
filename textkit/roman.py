"""Roman numeral conversion for 1..3999 (canonical forms only)."""

import re

# Greedy value table: each entry consumes the largest possible chunk,
# subtractive pairs included so no special-casing is needed.
_VALUE_TABLE = (
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
)

_LETTER_VALUES = {
    "I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000,
}

# Accepts exactly the canonical forms; bounds the value to 1..3999 by
# construction (max MMMCMXCIX = 3999).
_CANONICAL = re.compile(
    r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})"
)


def to_roman(n: int) -> str:
    """Return the canonical Roman numeral for ``n`` (1..3999)."""
    if not isinstance(n, int) or not 1 <= n <= 3999:
        raise ValueError(f"expected an int in 1..3999, got {n!r}")
    parts = []
    for value, numeral in _VALUE_TABLE:
        count, n = divmod(n, value)
        if count:
            parts.append(numeral * count)
    return "".join(parts)


def from_roman(s: str) -> int:
    """Return the value of a canonical Roman numeral, case-insensitive."""
    if not isinstance(s, str) or not s:
        raise ValueError(f"expected a non-empty Roman numeral string, got {s!r}")
    t = s.upper()
    if not _CANONICAL.fullmatch(t):
        raise ValueError(f"not a canonical Roman numeral: {s!r}")
    values = [_LETTER_VALUES[ch] for ch in t]
    total = 0
    for i, value in enumerate(values):
        if i + 1 < len(values) and value < values[i + 1]:
            total -= value  # subtractive pair, e.g. the I in IV
        else:
            total += value
    return total
