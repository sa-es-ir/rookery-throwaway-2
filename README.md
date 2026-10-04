# rookery-throwaway-2
Rookery live-test scratch repo

## word-count CLI

Count the lines, words, and characters of a UTF-8 text file:

```
python -m textkit.wc FILE
```

It prints `lines words chars` on one line to stdout and exits `0`.
A missing or unreadable file prints an error to stderr and exits `1`.

The same counts are available from Python via `textkit.wc.count(text)`, which
returns a dict with the keys `lines`, `words`, and `chars`.

Licensed under MIT.
