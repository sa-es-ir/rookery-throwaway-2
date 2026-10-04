"""Tests for textkit.roman."""

import unittest

from textkit.roman import from_roman, to_roman


class ToRomanTests(unittest.TestCase):
    def test_known_values(self):
        cases = {
            1: "I",
            4: "IV",
            9: "IX",
            40: "XL",
            90: "XC",
            400: "CD",
            900: "CM",
            1999: "MCMXCIX",
            3999: "MMMCMXCIX",
        }
        for n, expected in cases.items():
            with self.subTest(n=n):
                self.assertEqual(to_roman(n), expected)

    def test_out_of_range_and_non_int_raise(self):
        for bad in (0, -1, 4000, "5"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    to_roman(bad)


class FromRomanTests(unittest.TestCase):
    def test_known_values_and_case_insensitivity(self):
        cases = {
            "IV": 4,
            "iv": 4,
            "MCMXCIX": 1999,
            "mcmxcix": 1999,
            "Vi": 6,
        }
        for s, expected in cases.items():
            with self.subTest(s=s):
                self.assertEqual(from_roman(s), expected)

    def test_invalid_raise(self):
        for bad in ("", "IIII", "VX", "ABC"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    from_roman(bad)


class RoundTripTests(unittest.TestCase):
    def test_round_trip_over_full_range(self):
        for n in range(1, 4000):
            with self.subTest(n=n):
                self.assertEqual(from_roman(to_roman(n)), n)


if __name__ == "__main__":
    unittest.main()
