import unittest
import math
import types
from PyTils.validation import *

class TestSequenceAreNumbers(unittest.TestCase):
    def test_valid_numeric_list(self):
        # Should return True for a list of ints
        self.assertTrue(sequence_are_numbers([1, 2, 3]), "sequence_are_numbers should return True for a list of ints")
        # Should return True for a list of floats
        self.assertTrue(sequence_are_numbers([1.1, 2.2, 3.3]), "sequence_are_numbers should return True for a list of floats")
        # Should return True for a mixed list of ints and floats
        self.assertTrue(sequence_are_numbers([1, 2.2, 3]), "sequence_are_numbers should return True for a mixed list of ints and floats")

    def test_invalid_non_numeric(self):
        # Should return False for a list with a string
        self.assertFalse(sequence_are_numbers([1, 'a', 3]), "sequence_are_numbers should return False for a list containing a string")
        # Should return False for a list with a bool
        self.assertFalse(sequence_are_numbers([1, True, 3]), "sequence_are_numbers should return False for a list containing a bool")
        # Should return False for a list with None
        self.assertFalse(sequence_are_numbers([1, None, 3]), "sequence_are_numbers should return False for a list containing None")

    def test_invalid_nan_inf(self):
        # Should return False for a list with NaN
        self.assertFalse(sequence_are_numbers([1, math.nan, 3]), "sequence_are_numbers should return False for a list containing NaN")
        # Should return False for a list with inf
        self.assertFalse(sequence_are_numbers([1, math.inf, 3]), "sequence_are_numbers should return False for a list containing inf")

    def test_invalid_sequence_type(self):
        # Should raise InvalidSequenceError for non-sequence input
        with self.assertRaises(InvalidSequenceError, msg="sequence_are_numbers should raise InvalidSequenceError for non-sequence input"):
            sequence_are_numbers(123)
        with self.assertRaises(InvalidSequenceError, msg="sequence_are_numbers should raise InvalidSequenceError for string input"):
            sequence_are_numbers('abc')

class TestInvalidSequenceError(unittest.TestCase):
    def test_error_message(self):
        # Should contain 'expected a' in the message
        err = InvalidSequenceError()
        self.assertIn("expected a", str(err), "InvalidSequenceError message should contain 'expected a'")

class TestNotNumericSequenceError(unittest.TestCase):
    def test_error_message(self):
        # Should contain 'expected a' in the message
        err = NotNumericSequenceError()
        self.assertIn("expected a", str(err), "NotNumericSequenceError message should contain 'expected a'")

class TestValidateAsAndInvalidTypeError(unittest.TestCase):
    def test_validate_as_correct_type(self):
        # Should not raise for correct type
        try:
            validate_as(5, int)
            validate_as("hello", str)
            validate_as([1, 2, 3], list)
        except Exception as e:
            self.fail(f"validate_as raised {e} unexpectedly for correct type")

    def test_validate_as_incorrect_type(self):
        # Should raise InvalidTypeError for incorrect type
        with self.assertRaises(InvalidTypeError, msg="validate_as should raise InvalidTypeError for wrong type"):
            validate_as(5, str)
        with self.assertRaises(InvalidTypeError, msg="validate_as should raise InvalidTypeError for wrong type"):
            validate_as("hello", int)
        with self.assertRaises(InvalidTypeError, msg="validate_as should raise InvalidTypeError for wrong type"):
            validate_as(3.14, list)

    def test_invalid_type_error_message(self):
        # Should include the expected type in the error message
        err = InvalidTypeError(5, str)
        self.assertIn("expected 5 to be a", str(err), "InvalidTypeError message should mention the value")
        self.assertIn("str", str(err), "InvalidTypeError message should mention the expected type")
