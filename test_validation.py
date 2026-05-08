"""
Test suite for validation.py using pytest, covering all validation utilities and custom exceptions.
Ensures correct error handling, type validation, and numeric sequence checks for all public validation utilities.
"""

import pytest
import math
from .validation import (
	InvalidSequenceError,
	NotNumericSequenceError,
	InvalidTypeError,
	ProhibitedValueError,
	ValueAboveBoundsError,
	ValueBelowBoundsError,
	sequence_are_numbers,
	validate_as,
	validate_against,
	validate_float,
	validate_is_greater_than,
	validate_is_less_than,
)


def assert_raises_expected(callable_obj, expected_exception_type, context_message):
	actual_exception = None
	try:
		callable_obj()
	except Exception as exc:
		actual_exception = exc
	assert isinstance(actual_exception, expected_exception_type), (
		f'{context_message}. Expected exception type: {expected_exception_type.__name__}, '
		f'Actual: {type(actual_exception).__name__ if actual_exception is not None else "No exception"}'
	)
	return actual_exception

def test_invalid_sequence_error_message():
	err = InvalidSequenceError()
	assert 'expected a' in str(err), f"Expected message to contain 'expected a', Actual: {str(err)}"

def test_not_numeric_sequence_error_message():
	err = NotNumericSequenceError()
	assert 'expected a' in str(err), f"Expected message to contain 'expected a', Actual: {str(err)}"

def test_invalid_type_error_message():
	err = InvalidTypeError(5, str)
	assert 'expected 5 of <class' in str(err), f"Expected message to contain 'expected 5 of <class', Actual: {str(err)}"
	assert 'str' in str(err), f"Expected message to contain 'str', Actual: {str(err)}"

def test_prohibited_value_error_message():
	err = ProhibitedValueError(42, (1, 2, 42))
	assert 'expected 42 not to be any of (1, 2, 42)' in str(err), f"Expected message to contain 'expected 42 not to be any of (1, 2, 42)', Actual: {str(err)}"

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
		assert sequence_are_numbers(data), f'Expected True for sequence_are_numbers({data}), Actual: {sequence_are_numbers(data)}'
	else:
		assert not sequence_are_numbers(data), f'Expected False for sequence_are_numbers({data}), Actual: {sequence_are_numbers(data)}'

@pytest.mark.parametrize("bad_input", [123, 'abc', None])
def test_sequence_are_numbers_invalid_type(bad_input):
	assert_raises_expected(
		lambda: sequence_are_numbers(bad_input),
		InvalidSequenceError,
		'sequence_are_numbers should raise for invalid input type',
	)

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
	assert_raises_expected(
		lambda: validate_as(value, typ),
		InvalidTypeError,
		'validate_as should raise for incorrect type',
	)

@pytest.mark.parametrize("subject,invalids", [
	(3, (1, 2, 3)),
	("a", ("a", "b")),
])
def test_validate_against_raises(subject, invalids):
	assert_raises_expected(
		lambda: validate_against(subject, invalids),
		ProhibitedValueError,
		'validate_against should raise for prohibited subject value',
	)

def test_validate_against_no_raise():
	validate_against(4, (1, 2, 3))
	validate_against("c", ("a", "b"))

@pytest.mark.parametrize("value", [float('nan'), float('inf')])
def test_validate_float_raises(value):
	assert_raises_expected(
		lambda: validate_float(value),
		ProhibitedValueError,
		'validate_float should raise for NaN or infinity',
	)

@pytest.mark.parametrize("value", [0.0, 1.23, -5.6])
def test_validate_float_no_raise(value):
	validate_float(value)

# --- New tests for ValueAboveBoundsError, ValueBelowBoundsError, validate_is_greater_than, validate_is_less_than ---
def test_value_above_bounds_error_message():
	# Test that the error message is descriptive
	err = ValueAboveBoundsError(10, 5)
	assert '10 is prohibited to be greater than 5' in str(err), f"ValueAboveBoundsError should describe the subject and target. Actual: {str(err)}"

def test_value_below_bounds_error_message():
	# Test that the error message is descriptive
	err = ValueBelowBoundsError(2, 7)
	assert '2 is prohibited to be less than 7' in str(err), f"ValueBelowBoundsError should describe the subject and target. Actual: {str(err)}"

# Updated tests for corrected logic
@pytest.mark.parametrize('value,target', [
	(5, 10),
	(-1, 0),
	(99, 100),
])
def test_validate_is_greater_than_raises(value, target):
	# Should raise ValueAboveBoundsError when value < target
	actual_exception = assert_raises_expected(
		lambda: validate_is_greater_than(value, target),
		ValueAboveBoundsError,
		'validate_is_greater_than should raise when value is below target',
	)
	assert str(actual_exception) == f'{value} is prohibited to be greater than {target}', f'Expected message: {value} is prohibited to be greater than {target}, Actual: {str(actual_exception)}'

@pytest.mark.parametrize('value,target', [
	(10, 5),
	(0, -1),
	(100, 99),
])
def test_validate_is_greater_than_no_raise(value, target):
	# Should not raise when value >= target
	try:
		validate_is_greater_than(value, target)
	except Exception as e:
		assert False, f'Expected no exception for validate_is_greater_than({value}, {target}), but got: {e}'

@pytest.mark.parametrize('value,target', [
	(7, 2),
	(0, -5),
	(1, 0),
])
def test_validate_is_less_than_raises(value, target):
	# Should raise ValueBelowBoundsError when value > target
	actual_exception = assert_raises_expected(
		lambda: validate_is_less_than(value, target),
		ValueBelowBoundsError,
		'validate_is_less_than should raise when value is above target',
	)
	assert str(actual_exception) == f'{value} is prohibited to be less than {target}', f'Expected message: {value} is prohibited to be less than {target}, Actual: {str(actual_exception)}'

@pytest.mark.parametrize('value,target', [
	(2, 7),
	(-5, 0),
	(0, 1),
])
def test_validate_is_less_than_no_raise(value, target):
	# Should not raise when value <= target
	try:
		validate_is_less_than(value, target)
	except Exception as e:
		assert False, f'Expected no exception for validate_is_less_than({value}, {target}), but got: {e}'
