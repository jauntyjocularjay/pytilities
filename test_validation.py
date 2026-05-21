"""
Test suite for validation.py using pytest, covering all validation utilities and custom exceptions.
Ensures correct error handling, type validation, and numeric sequence checks for all public validation utilities.
"""

import math
import pytest
from .pytest_helpers import assert_no_exception, assert_raises_expected
from .validation import (
	InvalidSequenceError,
	NotNumericSequenceError,
	InvalidTypeError,
	ProhibitedValueError,
	DuplicateValueError,
	ValueAboveBoundsError,
	ValueBelowBoundsError,
	sequence_are_numbers,
	validate_as,
	validate_against,
	validate_float,
	validate_uniqueness,
	validate_is_greater_or_equal_to,
	validate_is_greater_than,
	validate_is_less_or_equal_to,
	validate_is_less_than,
	validate_igt,
	validate_ige,
	validate_ilt,
	validate_ile,
	validate_safe_exponent,
)

def test_invalid_sequence_error_message():
	err = InvalidSequenceError()
	assert isinstance(err, InvalidSequenceError), f'Expected InvalidSequenceError type, Actual: {type(err).__name__}'

def test_not_numeric_sequence_error_message():
	err = NotNumericSequenceError()
	assert isinstance(err, NotNumericSequenceError), f'Expected NotNumericSequenceError type, Actual: {type(err).__name__}'

def test_invalid_type_error_message():
	err = InvalidTypeError(5, str)
	assert isinstance(err, InvalidTypeError), f'Expected InvalidTypeError type, Actual: {type(err).__name__}'

def test_prohibited_value_error_message():
	err = ProhibitedValueError(42, (1, 2, 42))
	assert isinstance(err, ProhibitedValueError), f'Expected ProhibitedValueError type, Actual: {type(err).__name__}'

@pytest.mark.parametrize('data,expected', [
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
	# Numeric-only finite sequences should pass; mixed/non-finite values should fail.
	result = sequence_are_numbers(data)
	if expected:
		assert result, f'Expected True for sequence_are_numbers({data}), Actual: {result}'
	else:
		assert not result, f'Expected False for sequence_are_numbers({data}), Actual: {result}'

@pytest.mark.parametrize('bad_input', [123, 'abc', None])
def test_sequence_are_numbers_invalid_type(bad_input):
	# Non-sequence and disallowed sequence-like inputs should raise InvalidSequenceError.
	assert_raises_expected(
		lambda: sequence_are_numbers(bad_input),
		InvalidSequenceError,
		'sequence_are_numbers should raise for invalid input type',
	)

@pytest.mark.parametrize('value,typ', [
	(5, int),
	('hello', str),
	([1, 2, 3], list),
])
def test_validate_as_correct_type(value, typ):
	# Matching runtime types should pass validation.
	validate_as(value, typ)

@pytest.mark.parametrize('value,typ', [
	(5, str),
	('hello', int),
	(3.14, list),
])
def test_validate_as_incorrect_type(value, typ):
	# Mismatched runtime types should raise InvalidTypeError.
	assert_raises_expected(
		lambda: validate_as(value, typ),
		InvalidTypeError,
		'validate_as should raise for incorrect type',
	)

@pytest.mark.parametrize('subject,invalids', [
	(3, (1, 2, 3)),
	('a', ('a', 'b')),
])
def test_validate_against_raises(subject, invalids):
	# Prohibited values should raise ProhibitedValueError.
	assert_raises_expected(
		lambda: validate_against(subject, invalids),
		ProhibitedValueError,
		'validate_against should raise for prohibited subject value',
	)

def test_validate_against_no_raise():
	# Non-prohibited values should pass validation.
	validate_against(4, (1, 2, 3))
	validate_against('c', ('a', 'b'))

@pytest.mark.parametrize('value', [float('nan'), float('inf')])
def test_validate_float_raises(value):
	# Non-finite float values should raise ProhibitedValueError.
	assert_raises_expected(
		lambda: validate_float(value),
		ProhibitedValueError,
		'validate_float should raise for NaN or infinity',
	)

@pytest.mark.parametrize('value', [0.0, 1.23, -5.6])
def test_validate_float_no_raise(value):
	# Finite float values should pass validation.
	validate_float(value)

# --- New tests for ValueAboveBoundsError, ValueBelowBoundsError, validate_is_greater_than, validate_is_less_than ---
def test_value_above_bounds_error_message():
	# Test that ValueAboveBoundsError can be constructed.
	err = ValueAboveBoundsError(10, 5)
	assert isinstance(err, ValueAboveBoundsError), f'Expected ValueAboveBoundsError type, Actual: {type(err).__name__}'

def test_value_below_bounds_error_message():
	# Test that ValueBelowBoundsError can be constructed.
	err = ValueBelowBoundsError(2, 7)
	assert isinstance(err, ValueBelowBoundsError), f'Expected ValueBelowBoundsError type, Actual: {type(err).__name__}'

# Updated tests for corrected logic
@pytest.mark.parametrize('value,target', [
	(5, 10),
	(-1, 0),
	(98, 100),
	(5, 5),
])
def test_validate_is_greater_than_raises(value, target):
	# Should raise ValueBelowBoundsError when value is less than or equal to target.
	assert_raises_expected(
		lambda: validate_is_greater_than(value, target),
		ValueBelowBoundsError,
		'validate_is_greater_than should raise when value is below target',
	)

@pytest.mark.parametrize('value,target', [
	(10, 5),
	(0, -1),
	(100, 99),
])
def test_validate_is_greater_than_no_raise(value, target):
	# Should not raise when value is strictly greater than target.
	assert_no_exception(
		lambda: validate_is_greater_than(value, target),
		f'Expected no exception for validate_is_greater_than({value}, {target})',
	)

@pytest.mark.parametrize('value,target', [
	(5, 5),
	(10, 5),
	(0, -1),
])
def test_validate_is_greater_or_equal_to_no_raise(value, target):
	# Should not raise when value is greater than or equal to target.
	assert_no_exception(
		lambda: validate_is_greater_or_equal_to(value, target),
		f'Expected no exception for validate_is_greater_or_equal_to({value}, {target})',
	)

@pytest.mark.parametrize('value,target', [
	(4, 5),
	(-2, 0),
])
def test_validate_is_greater_or_equal_to_raises(value, target):
	# Should raise ValueBelowBoundsError when value is below target.
	assert_raises_expected(
		lambda: validate_is_greater_or_equal_to(value, target),
		ValueBelowBoundsError,
		'validate_is_greater_or_equal_to should raise when value is below target',
	)

@pytest.mark.parametrize('value,target', [
	(7, 2),
	(0, -5),
	(2, 0),
	(0, 0),
])
def test_validate_is_less_than_raises(value, target):
	# Should raise ValueAboveBoundsError when value is greater than or equal to target.
	assert_raises_expected(
		lambda: validate_is_less_than(value, target),
		ValueAboveBoundsError,
		'validate_is_less_than should raise when value is above target',
	)

@pytest.mark.parametrize('value,target', [
	(2, 7),
	(-5, 0),
	(0, 1),
])
def test_validate_is_less_than_no_raise(value, target):
	# Should not raise when value is strictly less than target.
	assert_no_exception(
		lambda: validate_is_less_than(value, target),
		f'Expected no exception for validate_is_less_than({value}, {target})',
	)

@pytest.mark.parametrize('value,target', [
	(5, 5),
	(2, 7),
	(-5, 0),
])
def test_validate_is_less_or_equal_to_no_raise(value, target):
	# Should not raise when value is less than or equal to target.
	assert_no_exception(
		lambda: validate_is_less_or_equal_to(value, target),
		f'Expected no exception for validate_is_less_or_equal_to({value}, {target})',
	)

@pytest.mark.parametrize('value,target', [
	(8, 2),
	(1, 0),
])
def test_validate_is_less_or_equal_to_raises(value, target):
	# Should raise ValueAboveBoundsError when value is above target.
	assert_raises_expected(
		lambda: validate_is_less_or_equal_to(value, target),
		ValueAboveBoundsError,
		'validate_is_less_or_equal_to should raise when value is above target',
	)


def test_duplicate_value_error_message():
	# Constructing DuplicateValueError should produce the correct exception type.
	err = DuplicateValueError('alpha')
	assert isinstance(err, DuplicateValueError), (
		f'Expected DuplicateValueError type, Actual: {type(err).__name__}'
	)


@pytest.mark.parametrize('iterable,value', [
	([1, 2, 3], 2),
	(('a', 'b', 'c'), 'a'),
	({'x', 'y'}, 'y'),
])
def test_validate_uniqueness_raises_duplicate(iterable, value):
	# Duplicate values in the iterable should raise DuplicateValueError.
	actual_exception = assert_raises_expected(
		lambda: validate_uniqueness(iterable, value),
		DuplicateValueError,
		'validate_uniqueness should raise DuplicateValueError when value already exists',
	)
	assert str(actual_exception) == f'{value} is already represented', (
		f'Expected duplicate message for {value}, Actual: {str(actual_exception)}'
	)


@pytest.mark.parametrize('iterable,value', [
	([1, 2, 3], 4),
	(('a', 'b', 'c'), 'z'),
	({'x', 'y'}, 'q'),
])
def test_validate_uniqueness_allows_new_values(iterable, value):
	# Values not present in iterable should pass uniqueness validation.
	assert_no_exception(
		lambda: validate_uniqueness(iterable, value),
		f'Expected no exception for validate_uniqueness({iterable}, {value})',
	)


@pytest.mark.parametrize('validator,value,target', [
	(validate_igt, 5, 5),
	(validate_ige, 4, 5),
	(validate_ilt, 6, 5),
	(validate_ile, 7, 5),
])
def test_alias_validators_raise_same_bounds_errors(validator, value, target):
	# Aliases should raise the same bounds errors as their base validators.
	if validator in (validate_igt, validate_ige):
		expected_error = ValueBelowBoundsError
	else:
		expected_error = ValueAboveBoundsError
	assert_raises_expected(
		lambda: validator(value, target),
		expected_error,
		f'{validator.__name__} should raise the corresponding bounds error for invalid bounds',
	)


@pytest.mark.parametrize('validator,value,target', [
	(validate_igt, 6, 5),
	(validate_ige, 5, 5),
	(validate_ilt, 4, 5),
	(validate_ile, 5, 5),
])
def test_alias_validators_pass_with_valid_bounds(validator, value, target):
	# Aliases should pass when input satisfies their boundary rules.
	assert_no_exception(
		lambda: validator(value, target),
		f'Expected no exception for {validator.__name__}({value}, {target})',
	)


def test_validate_safe_exponent_raises_when_exponent_exceeds_bound():
	# Exponents above the computed safe bound should raise ValueAboveBoundsError.
	actual_exception = assert_raises_expected(
		lambda: validate_safe_exponent(2, 2000),
		ValueAboveBoundsError,
		'validate_safe_exponent should raise ValueAboveBoundsError when exponent is unsafe',
	)
	assert 'prohibited to be greater' in str(actual_exception), (
		'Expected overflow bounds message to mention greater-than prohibition, '
		f'Actual: {str(actual_exception)}'
	)


@pytest.mark.parametrize('base,exponent', [
	(2, 9),
	(10, 2),
	(1.1, 10),
])
def test_validate_safe_exponent_allows_safe_inputs(base, exponent):
	# Safe exponent pairs should not raise any overflow bounds error.
	assert_no_exception(
		lambda: validate_safe_exponent(base, exponent),
		f'Expected no exception for validate_safe_exponent({base}, {exponent})',
	)


def test_validate_safe_exponent_base_one_raises_zero_division_error():
	# Base of 1 currently triggers a division-by-zero during bound computation.
	actual_exception = assert_raises_expected(
		lambda: validate_safe_exponent(1, 100),
		ZeroDivisionError,
		'validate_safe_exponent should raise ZeroDivisionError for base equal to 1 in current implementation',
	)
	assert 'division by zero' in str(actual_exception), (
		'Expected base=1 failure message to contain division-by-zero details, '
		f'Actual: {str(actual_exception)}'
	)
