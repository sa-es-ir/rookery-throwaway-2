"""Tests for textkit.slug.slugify."""

import unittest

from textkit.slug import slugify


class SlugifyTests(unittest.TestCase):
    def test_lowercases_plain_words(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_folds_accents_to_ascii(self):
        self.assertEqual(slugify("café"), "cafe")
        self.assertEqual(slugify("ÀÉÎÕÜ"), "aeiou")
        self.assertEqual(slugify("Naïve—Tête"), "naive-tete")

    def test_collapses_runs_of_non_alnum_to_one_dash(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")
        self.assertEqual(slugify("a  --  b"), "a-b")
        self.assertEqual(slugify("Version 2.3"), "version-2-3")

    def test_strips_leading_and_trailing_dashes(self):
        self.assertEqual(slugify("--hello--"), "hello")
        self.assertEqual(slugify("  Many   spaces -- and  dashes "), "many-spaces-and-dashes")

    def test_keeps_digits(self):
        self.assertEqual(slugify("CamelCase 42"), "camelcase-42")

    def test_empty_and_all_symbol_inputs_return_empty(self):
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify("!!!"), "")

    def test_combined_example(self):
        self.assertEqual(slugify("  Café Corner — Menu (5)  "), "cafe-corner-menu-5")


if __name__ == "__main__":
    unittest.main()
