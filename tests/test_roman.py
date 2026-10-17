"""Tests for textkit.roman."""

import unittest

from textkit.roman import from_roman, to_roman


class ToRomanTests(unittest.TestCase):
    def test_known_values(self):
        cases = [
            (1, "I"), (4, "IV"), (9, "IX"), (14, "XIV"), (40, "XL"),
            (90, "XC"), (400, "CD"), (900, "CM"), (1994, "MCMXCIV"),
            (3999, "MMMCMXCIX"),
        ]
        for n, expected in cases:
            with self.subTest(n=n):
                self.assertEqual(to_roman(n), expected)

    def test_invalid_numbers(self):
        for n in (0, -1, 4000):
            with self.subTest(n=n):
                with self.assertRaises(ValueError):
                    to_roman(n)

    def test_non_int_input(self):
        for n in ("5", None, 3.5):
            with self.subTest(n=n):
                with self.assertRaises(ValueError):
                    to_roman(n)


class FromRomanTests(unittest.TestCase):
    def test_known_values(self):
        cases = [
            ("I", 1), ("IV", 4), ("IX", 9), ("XIV", 14), ("XL", 40),
            ("XC", 90), ("CD", 400), ("CM", 900), ("MCMXCIV", 1994),
            ("MMMCMXCIX", 3999),
        ]
        for s, expected in cases:
            with self.subTest(s=s):
                self.assertEqual(from_roman(s), expected)

    def test_invalid_strings(self):
        for s in ("", "IIII", "VX", "IVIV", "ABC"):
            with self.subTest(s=s):
                with self.assertRaises(ValueError):
                    from_roman(s)

    def test_non_str_input(self):
        for s in (5, None, ["IV"]):
            with self.subTest(s=s):
                with self.assertRaises(ValueError):
                    from_roman(s)

    def test_case_insensitive(self):
        for s, expected in (("mcmxciv", 1994), ("iv", 4)):
            with self.subTest(s=s):
                self.assertEqual(from_roman(s), expected)


class RoundTripTests(unittest.TestCase):
    def test_round_trip_1_to_3999(self):
        for n in range(1, 4000):
            with self.subTest(n=n):
                self.assertEqual(from_roman(to_roman(n)), n)


if __name__ == "__main__":
    unittest.main()
