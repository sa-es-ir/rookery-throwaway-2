# rookery-throwaway-2
Rookery live-test scratch repo

Licensed under MIT.

## textkit

Small text helpers (standard library only).

### slugify

```python
from textkit.slug import slugify

slugify("Café Corner — Menu!")  # -> 'cafe-corner-menu'
```

Rules: lowercase; accented Latin letters fold to ASCII (`café` -> `cafe`);
every run of characters that are not `a-z` or `0-9` becomes one `-`; no
leading or trailing `-`. Characters with no ASCII decomposition (`ß`, `æ`,
non-Latin scripts) collapse into `-` like any other non-alphanumeric run, so
`slugify("!!!")` and `slugify("")` both return `""`.
