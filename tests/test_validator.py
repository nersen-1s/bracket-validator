import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from bracket_validator import find_wrong_positions, highlight, validate
from bracket_validator.cli import main


class TestFindWrongPositions(unittest.TestCase):
    def test_valid(self):
        for text in ("", "no brackets", "()", "{[(<>)]}", "(a)(b)", "<div><p>text</p></div>"):
            with self.subTest(text=text):
                self.assertEqual(find_wrong_positions(text), [])

    def test_extra_closing(self):
        self.assertEqual(find_wrong_positions("())"), [2])
        self.assertEqual(find_wrong_positions(")"), [0])

    def test_extra_opening(self):
        self.assertEqual(find_wrong_positions("(()"), [0])
        self.assertEqual(find_wrong_positions("(("), [0, 1])

    def test_wrong_type_of_bracket(self):
        self.assertEqual(find_wrong_positions("(]"), [0, 1])

    def test_example_from_task(self):
        self.assertEqual(find_wrong_positions("<div><p>{ test }}</p</div>"), [16, 17])

    def test_positions_are_sorted(self):
        self.assertEqual(find_wrong_positions("(a))(b"), [3, 4])

    def test_wrong_argument_type(self):
        for value in (None, 123, ["()"]):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    find_wrong_positions(value)


class TestValidate(unittest.TestCase):
    def test_valid_returns_none(self):
        self.assertIsNone(validate("(<{[]}>)"))

    def test_invalid_raises_value_error_with_positions(self):
        with self.assertRaises(ValueError) as ctx:
            validate("<div><p>{ test }}</p</div>")
        self.assertEqual(str(ctx.exception), "Дужки незбалансовані на позиціях [16, 17]")


class TestHighlight(unittest.TestCase):
    def test_carets_under_wrong_brackets(self):
        text = "<div><p>{ test }}</p</div>"
        expected = text + "\n" + " " * 16 + "^^"
        self.assertEqual(highlight(text, [16, 17]), expected)

    def test_no_positions(self):
        self.assertEqual(highlight("ab", []), "ab\n")


class TestCli(unittest.TestCase):
    def run_main(self, line):
        out = io.StringIO()
        with patch("builtins.input", return_value=line) as fake_input, redirect_stdout(out):
            try:
                main()
            except ValueError as error:
                return out.getvalue(), error, fake_input
        return out.getvalue(), None, fake_input

    def test_valid_string(self):
        out, error, fake_input = self.run_main("(a + b)")
        self.assertIsNone(error)
        self.assertIn("Строка валідна", out)
        fake_input.assert_called_once_with("Введіть строку: ")

    def test_invalid_string_prints_carets_and_raises(self):
        text = "<div><p>{ test }}</p</div>"
        out, error, _ = self.run_main(text)
        self.assertIn(text + "\n" + " " * 16 + "^^", out)
        self.assertIsInstance(error, ValueError)
        self.assertNotIn("Строка валідна", out)

    def test_run_as_module(self):
        """Пакет запускається командою python -m bracket_validator."""
        result = subprocess.run([sys.executable, "-m", "bracket_validator"], input="(]\n",
                                capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ValueError: Дужки незбалансовані на позиціях [0, 1]", result.stderr)


if __name__ == "__main__":
    unittest.main()
