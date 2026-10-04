"""Roman numeral conversion for values 1..3999."""

_TABLE = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

_VALUES = {symbol: value for value, symbol in _TABLE}


def to_roman(n: int) -> str:
    """Return the canonical uppercase Roman numeral for 1 <= n <= 3999."""
    if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= 3999:
        raise ValueError(f"n must be an int in 1..3999, got {n!r}")

    out = []
    for value, symbol in _TABLE:
        count, n = divmod(n, value)
        out.append(symbol * count)
    return "".join(out)


def from_roman(s: str) -> int:
    """Return the integer value of a Roman numeral, case-insensitively."""
    if not isinstance(s, str) or not s:
        raise ValueError(f"s must be a non-empty str, got {s!r}")

    s = s.upper()
    if any(char not in _VALUES for char in s):
        raise ValueError(f"not a Roman numeral: {s!r}")

    total = 0
    previous = 0
    for char in reversed(s):
        value = _VALUES[char]
        total += value if value >= previous else -value
        previous = max(previous, value)

    # Round trip rejects non-canonical forms (IIII, VX, IIV, ...).
    if to_roman(total) != s:
        raise ValueError(f"not a canonical Roman numeral: {s!r}")
    return total
