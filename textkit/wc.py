"""Count lines, words, and characters in a UTF-8 text file."""

import sys


def count(text):
    """Return {"lines", "words", "chars"} counts for `text`."""
    return {
        "lines": len(text.splitlines()),
        "words": len(text.split()),
        "chars": len(text),
    }


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 1:
        print("usage: python -m textkit.wc FILE", file=sys.stderr)
        return 1
    path = argv[0]
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        print(f"textkit.wc: {path}: {exc}", file=sys.stderr)
        return 1
    counts = count(text)
    print(f"{counts['lines']} {counts['words']} {counts['chars']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
