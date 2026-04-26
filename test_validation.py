"""
Test suite for validation.py using pytest, covering all validation utilities and custom exceptions.
Ensures correct error handling, type validation, and numeric sequence checks for all public validation utilities.
"""

import pytest
import math
from pytilities.validation import *

def test_invalid_sequence_error_message():
	err = InvalidSequenceError()
	assert 'expected a' in str(err)

def test_not_numeric_sequence_error_message():
	err = NotNumericSequenceError()
	assert 'expected a' in str(err)

def test_invalid_type_error_message():
	err = InvalidTypeError(5, str)
	assert 'expected 5 of <class' in str(err)
	assert 'str' in str(err)

def test_prohibited_value_error_message():
	err = ProhibitedValueError(42, (1, 2, 42))
	assert 'expected 42 not to be any of (1, 2, 42)' in str(err)

@pytest.mark.parametrize("data,expected", [
	([1, 2, 3], True),
	([1.1, 2.2, 3.3], True),
	([1, 2.2, 3], True),
	([1, 'a', 3], False),
	([1, True, 3], False),
	([1, None, 3], False),
	([1, math.nan, 3], False),
	([1, math.inf, 3], False),
])
def test_sequence_are_numbers(data, expected):
	if expected:
		assert sequence_are_numbers(data)
	else:
		assert not sequence_are_numbers(data)

@pytest.mark.parametrize("bad_input", [123, 'abc', None])
def test_sequence_are_numbers_invalid_type(bad_input):
	with pytest.raises(InvalidSequenceError):
		sequence_are_numbers(bad_input)

@pytest.mark.parametrize("value,typ", [
	(5, int),
	("hello", str),
	([1, 2, 3], list),
])
def test_validate_as_correct_type(value, typ):
	validate_as(value, typ)

@pytest.mark.parametrize("value,typ", [
	(5, str),
	("hello", int),
	(3.14, list),
])
def test_validate_as_incorrect_type(value, typ):
	with pytest.raises(InvalidTypeError):
		validate_as(value, typ)

@pytest.mark.parametrize("subject,invalids", [
	(3, (1, 2, 3)),
	("a", ("a", "b")),
])
def test_validate_against_raises(subject, invalids):
	with pytest.raises(ProhibitedValueError):
		validate_against(subject, invalids)

def test_validate_against_no_raise():
	validate_against(4, (1, 2, 3))
	validate_against("c", ("a", "b"))

@pytest.mark.parametrize("value", [float('nan'), float('inf')])
def test_validate_float_raises(value):
	with pytest.raises(ProhibitedValueError):
		validate_float(value)

@pytest.mark.parametrize("value", [0.0, 1.23, -5.6])
def test_validate_float_no_raise(value):
	validate_float(value)
