
"""
Test suite for validation.py covering all validation utilities and custom exceptions.

This module ensures correct error handling, type validation, and numeric sequence checks
for all public validation utilities.
"""

import unittest
import math
import types
from .validation import *


class TestProhibitedValueError(unittest.TestCase):
    '''Unit tests for the ProhibitedValueError exception.'''

    def test_error_message(self):
        '''Should mention the value and invalid tuple.'''
        err = ProhibitedValueError(5, (1, 2, 5))
        self.assertIn('expected 5 not to be one of these (1, 2, 5)', str(err), 'ProhibitedValueError message should mention value and tuple')



class TestValidateAgainst(unittest.TestCase):
    '''Unit tests for the validate_against function.'''

    def assertNoException(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            self.fail(f'{func.__name__} raised {e} unexpectedly for args={args}, kwargs={kwargs}')

    def test_raises_on_prohibited_value(self):
        '''Should raise ProhibitedValueError if subject is in invalid_value_tuple.'''
        with self.assertRaises(ProhibitedValueError, msg='Should raise for prohibited value'):
            validate_against(3, (1, 2, 3))

    def test_no_raise_on_allowed_value(self):
        '''Should not raise if subject is not in invalid_value_tuple.'''
        self.assertNoException(validate_against, 4, (1, 2, 3))



class TestValidateFloat(unittest.TestCase):
    '''Unit tests for the validate_float function.'''

    def assertNoException(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            self.fail(f'{func.__name__} raised {e} unexpectedly for args={args}, kwargs={kwargs}')

    def test_raises_on_nan(self):
        '''Should raise ProhibitedValueError for NaN.'''
        with self.assertRaises(ProhibitedValueError, msg='Should raise for NaN'):
            validate_float(float('nan'))

    def test_raises_on_inf(self):
        '''Should raise ProhibitedValueError for infinity.'''
        with self.assertRaises(ProhibitedValueError, msg='Should raise for inf'):
            validate_float(float('inf'))

    def test_no_raise_on_valid_float(self):
        '''Should not raise for a valid float value.'''
        self.assertNoException(validate_float, 3.14)


class TestSequenceAreNumbers(unittest.TestCase):
    '''Unit tests for the sequence_are_numbers function.'''

    def assertSequenceTrue(self, seq, msg=None):
        self.assertTrue(sequence_are_numbers(seq), msg or f'Should return True for: {seq}')

    def assertSequenceFalse(self, seq, msg=None):
        self.assertFalse(sequence_are_numbers(seq), msg or f'Should return False for: {seq}')

    def test_valid_numeric_list(self):
        '''Should return True for lists of ints, floats, or mixed numeric types.'''
        valid_cases = [
            [1, 2, 3],
            [1.1, 2.2, 3.3],
            [1, 2.2, 3],
        ]
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertSequenceTrue(case)

    def test_invalid_non_numeric(self):
        '''Should return False for lists containing non-numeric types (str, bool, None).'''
        invalid_cases = [
            [1, 'a', 3],
            [1, True, 3],
            [1, None, 3],
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertSequenceFalse(case)

    def test_invalid_nan_inf(self):
        '''Should return False for lists containing NaN or infinity.'''
        invalid_cases = [
            [1, math.nan, 3],
            [1, math.inf, 3],
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertSequenceFalse(case)

    def test_invalid_sequence_type(self):
        '''Should raise InvalidSequenceError for non-sequence or string input.'''
        for bad_input in [123, 'abc']:
            with self.subTest(bad_input=bad_input):
                with self.assertRaises(InvalidSequenceError, msg=f'Should raise for {bad_input}'):
                    sequence_are_numbers(bad_input)



class TestInvalidSequenceError(unittest.TestCase):
    '''Unit tests for the InvalidSequenceError exception.'''

    def test_error_message(self):
        '''Should contain 'expected a' in the error message.'''
        self.assertIn('expected a', str(InvalidSequenceError()), 'InvalidSequenceError message should contain \'expected a\'')



class TestNotNumericSequenceError(unittest.TestCase):
    '''Unit tests for the NotNumericSequenceError exception.'''

    def test_error_message(self):
        '''Should contain 'expected a' in the error message.'''
        self.assertIn('expected a', str(NotNumericSequenceError()), 'NotNumericSequenceError message should contain \'expected a\'')



class TestValidateAsAndInvalidTypeError(unittest.TestCase):
    '''Unit tests for the validate_as function and InvalidTypeError exception.'''

    def assertNoException(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            self.fail(f'{func.__name__} raised {e} unexpectedly for args={args}, kwargs={kwargs}')

    def test_validate_as_correct_type(self):
        '''Should not raise for correct type.'''
        valid_cases = [
            (5, int),
            ('hello', str),
            ([1, 2, 3], list),
        ]
        for value, typ in valid_cases:
            with self.subTest(value=value, typ=typ):
                self.assertNoException(validate_as, value, typ)

    def test_validate_as_incorrect_type(self):
        '''Should raise InvalidTypeError for incorrect type.'''
        invalid_cases = [
            (5, str),
            ('hello', int),
            (3.14, list),
        ]
        for value, typ in invalid_cases:
            with self.subTest(value=value, typ=typ):
                with self.assertRaises(InvalidTypeError, msg=f'validate_as should raise for value={value}, type={typ}'):
                    validate_as(value, typ)

    def test_invalid_type_error_message(self):
        '''Should include the expected type in the error message.'''
        err = InvalidTypeError(5, str)
        self.assertIn('expected 5 of <class \'int\'> to be an instance of <class \'str\'', str(err), 'InvalidTypeError message should match the format')
