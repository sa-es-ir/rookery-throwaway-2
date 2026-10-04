import unittest

from textkit.slug import slugify


class SlugifyTests(unittest.TestCase):
    def test_lowercase(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_accent_folding(self):
        self.assertEqual(slugify("café"), "cafe")

    def test_non_alphanumeric_runs(self):
        self.assertEqual(slugify("a  b---c"), "a-b-c")
        self.assertEqual(slugify("hello, world!"), "hello-world")

    def test_no_leading_or_trailing_dash(self):
        self.assertEqual(slugify("  hello  "), "hello")
        self.assertEqual(slugify("-hello-world-"), "hello-world")

    def test_mixed(self):
        self.assertEqual(slugify("Héllo, Wörld!"), "hello-world")

    def test_empty(self):
        self.assertEqual(slugify(""), "")


if __name__ == "__main__":
    unittest.main()
