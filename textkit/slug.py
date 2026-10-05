"""textkit.slug - turn arbitrary text into URL-friendly slugs."""

import re
import unicodedata

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Return the URL slug for *text*.

    Lowercases; folds accented Latin letters to ASCII ("cafe" from "café");
    collapses every run of characters outside [a-z0-9] into a single "-";
    strips leading and trailing "-". Input that folds to nothing (e.g. "!!!")
    returns "".
    """
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_only = "".join(c for c in decomposed if not unicodedata.combining(c))
    return _NON_ALNUM.sub("-", ascii_only.lower()).strip("-")
