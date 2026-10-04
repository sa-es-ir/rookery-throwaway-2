# rookery-throwaway-2
Rookery live-test scratch repo

Licensed under MIT.

## Usage

### textkit.slug

`slugify(text)` lowercases text, folds accented letters to ASCII, and turns any
run of characters outside `a-z`/`0-9` into a single `-`:

    from textkit.slug import slugify

    slugify("Héllo, Wörld!")  # "hello-world"
