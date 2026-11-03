import unittest
from lab5 import validate_brackets, process_string

class TestBrackets(unittest.TestCase):

    def test_valid_brackets(self):
        is_valid, pos = validate_brackets("<div><p>{ test }</p></div>")
        self.assertTrue(is_valid)
        self.assertEqual(pos, [])

    def test_invalid_brackets_positions(self):
        s = "<div><p>{ test }}</p</div>"
        is_valid, pos = validate_brackets(s)
        self.assertFalse(is_valid)

        self.assertEqual(pos, [16, 17])

    def test_value_error_raised(self):
        with self.assertRaises(ValueError):
            process_string("({[<")

if __name__ == "__main__":
    unittest.main()