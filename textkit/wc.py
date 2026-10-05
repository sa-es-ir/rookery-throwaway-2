"""Count lines, words, and characters in a text file.

Usage: python -m textkit.wc FILE
"""

import sys


def count(text: str) -> dict:
    """Return {'lines': L, 'words': W, 'chars': C} for *text*.

    Raises ValueError if *text* is not a str.
    """
    if not isinstance(text, str):
        raise ValueError("text must be a str")
    return {
        "lines": len(text.splitlines()),
        "words": len(text.split()),
        "chars": len(text),
    }


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else list(argv)
    if len(argv) != 1:
        print("usage: python -m textkit.wc FILE", file=sys.stderr)
        return 2
    path = argv[0]
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        print(f"wc: {path}: {exc}", file=sys.stderr)
        return 1
    totals = count(text)
    print(f"{totals['lines']} {totals['words']} {totals['chars']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
