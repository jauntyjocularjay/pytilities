"""Behavior-focused tests for pytilities.validation."""

import math

import pytest

from .assert_helpers import assert_no_exception, assert_raises_expected
from .validation import (
    DuplicateValueError,
    InvalidSequenceError,
    InvalidTypeError,
    NotNumericSequenceError,
    ProhibitedValueError,
    ValueAboveBoundsError,
    ValueBelowBoundsError,
    sequence_are_numbers,
    validate_ige,
    validate_igt,
    validate_ile,
    validate_ilt,
    validate_as,
    validate_against,
    validate_float,
    validate_is_greater_or_equal_to,
    validate_is_greater_than,
    validate_is_less_or_equal_to,
    validate_is_less_than,
    validate_safe_exponent,
    validate_uniqueness,
)

# LLM-Generated: Reworked the validation suite to prefer clear, behavior-first assertions.


def test_invalid_sequence_error_is_exception_type():
    err = InvalidSequenceError()
    assert isinstance(err, InvalidSequenceError)


def test_not_numeric_sequence_error_is_exception_type():
    err = NotNumericSequenceError()
    assert isinstance(err, NotNumericSequenceError)


def test_invalid_type_error_is_exception_type():
    err = InvalidTypeError(5, str)
    assert isinstance(err, InvalidTypeError)


def test_prohibited_value_error_is_exception_type():
    err = ProhibitedValueError(42, (1, 2, 42))
    assert isinstance(err, ProhibitedValueError)


# LLM-Generated: Numeric-sequence checks stay focused on valid-vs-invalid values.
@pytest.mark.parametrize(
    "data, expected",
    [
        ([1, 2, 3], True),
        ([1.1, 2.2, 3.3], True),
        ([1, 2.2, 3], True),
        ([1, "a", 3], False),
        ([1, True, 3], False),
        ([1, None, 3], False),
        ([1, math.nan, 3], False),
        ([1, math.inf, 3], False),
    ],
)
def test_sequence_are_numbers_accepts_only_finite_numeric_values(data, expected):
    result = sequence_are_numbers(data)
    assert result is expected


@pytest.mark.parametrize("bad_input", [123, "abc", None])
def test_sequence_are_numbers_rejects_invalid_sequence_inputs(bad_input):
    assert_raises_expected(
        lambda: sequence_are_numbers(bad_input),
        InvalidSequenceError,
        "sequence_are_numbers should reject invalid input types",
    )


# LLM-Generated: Type checks are grouped by valid and invalid runtime-type behavior.
@pytest.mark.parametrize("value, expected_type", [(5, int), ("hello", str), ([1, 2, 3], list)])
def test_validate_as_accepts_matching_type(value, expected_type):
    validate_as(value, expected_type)


@pytest.mark.parametrize("value, expected_type", [(5, str), ("hello", int), (3.14, list)])
def test_validate_as_rejects_mismatched_type(value, expected_type):
    assert_raises_expected(
        lambda: validate_as(value, expected_type),
        InvalidTypeError,
        "validate_as should reject mismatched runtime types",
    )


@pytest.mark.parametrize("subject, invalids", [(3, (1, 2, 3)), ("a", ("a", "b"))])
def test_validate_against_rejects_forbidden_values(subject, invalids):
    assert_raises_expected(
        lambda: validate_against(subject, invalids),
        ProhibitedValueError,
        "validate_against should reject prohibited values",
    )


def test_validate_against_allows_non_forbidden_values():
    validate_against(4, (1, 2, 3))
    validate_against("c", ("a", "b"))


@pytest.mark.parametrize("value", [float("nan"), float("inf")])
def test_validate_float_rejects_non_finite_numbers(value):
    assert_raises_expected(
        lambda: validate_float(value),
        ProhibitedValueError,
        "validate_float should reject NaN and infinity",
    )


@pytest.mark.parametrize("value", [0.0, 1.23, -5.6])
def test_validate_float_accepts_finite_numbers(value):
    validate_float(value)


# LLM-Generated: Boundary validators are tested by contract, not by exact wording.
@pytest.mark.parametrize(
    "validator, value, target",
    [
        (validate_is_greater_than, 5, 10),
        (validate_is_greater_than, -1, 0),
        (validate_is_greater_than, 98, 100),
        (validate_is_greater_than, 5, 5),
        (validate_is_greater_or_equal_to, 4, 5),
        (validate_is_greater_or_equal_to, -2, 0),
        (validate_is_less_than, 7, 2),
        (validate_is_less_than, 0, -5),
        (validate_is_less_than, 2, 0),
        (validate_is_less_than, 0, 0),
        (validate_is_less_or_equal_to, 8, 2),
        (validate_is_less_or_equal_to, 1, 0),
    ],
)
def test_bound_validators_reject_out_of_range_values(validator, value, target):
    assert_raises_expected(
        lambda: validator(value, target),
        (ValueBelowBoundsError if validator in (validate_is_greater_than, validate_is_greater_or_equal_to) else ValueAboveBoundsError),
        f"{validator.__name__} should reject values outside its allowed range",
    )


@pytest.mark.parametrize(
    "validator, value, target",
    [
        (validate_is_greater_than, 10, 5),
        (validate_is_greater_than, 0, -1),
        (validate_is_greater_than, 100, 99),
        (validate_is_greater_or_equal_to, 5, 5),
        (validate_is_greater_or_equal_to, 10, 5),
        (validate_is_greater_or_equal_to, 0, -1),
        (validate_is_less_than, 2, 7),
        (validate_is_less_than, -5, 0),
        (validate_is_less_than, 0, 1),
        (validate_is_less_or_equal_to, 5, 5),
        (validate_is_less_or_equal_to, 2, 7),
        (validate_is_less_or_equal_to, -5, 0),
    ],
)
def test_bound_validators_accept_in_range_values(validator, value, target):
    assert_no_exception(
        lambda: validator(value, target),
        f"{validator.__name__} should accept values within range",
    )


def test_value_above_bounds_error_is_exception_type():
    err = ValueAboveBoundsError(10, 5)
    assert isinstance(err, ValueAboveBoundsError)


def test_value_below_bounds_error_is_exception_type():
    err = ValueBelowBoundsError(2, 7)
    assert isinstance(err, ValueBelowBoundsError)


def test_duplicate_value_error_is_exception_type():
    err = DuplicateValueError("alpha")
    assert isinstance(err, DuplicateValueError)


@pytest.mark.parametrize(
    "iterable_obj, value",
    [
        ([1, 2, 3], 2),
        (("a", "b", "c"), "a"),
        ({"x", "y"}, "y"),
    ],
)
def test_validate_uniqueness_rejects_duplicates(iterable_obj, value):
    actual_exception = assert_raises_expected(
        lambda: validate_uniqueness(iterable_obj, value),
        DuplicateValueError,
        "validate_uniqueness should reject duplicate values",
    )
    assert isinstance(actual_exception, DuplicateValueError)


@pytest.mark.parametrize(
    "iterable_obj, value",
    [
        ([1, 2, 3], 4),
        (("a", "b", "c"), "z"),
        ({"x", "y"}, "q"),
    ],
)
def test_validate_uniqueness_accepts_unique_values(iterable_obj, value):
    assert_no_exception(
        lambda: validate_uniqueness(iterable_obj, value),
        "validate_uniqueness should accept new values",
    )


@pytest.mark.parametrize(
    "validator, value, target",
    [
        (validate_igt, 5, 5),
        (validate_ige, 4, 5),
        (validate_ilt, 6, 5),
        (validate_ile, 7, 5),
    ],
)
def test_alias_validators_reject_invalid_bounds(validator, value, target):
    expected_error = ValueBelowBoundsError if validator in (validate_igt, validate_ige) else ValueAboveBoundsError
    assert_raises_expected(
        lambda: validator(value, target),
        expected_error,
        f"{validator.__name__} should reject invalid bounds",
    )


@pytest.mark.parametrize(
    "validator, value, target",
    [
        (validate_igt, 6, 5),
        (validate_ige, 5, 5),
        (validate_ilt, 4, 5),
        (validate_ile, 5, 5),
    ],
)
def test_alias_validators_accept_valid_bounds(validator, value, target):
    assert_no_exception(
        lambda: validator(value, target),
        f"{validator.__name__} should accept valid bounds",
    )


@pytest.mark.parametrize(
    "base, exponent",
    [
        (2, 9),
        (10, 2),
        (1.1, 10),
        (1, 100),
        (0, 0),
        (0, 3),
    ],
)
def test_validate_safe_exponent_allows_safe_boundaries(base, exponent):
    assert_no_exception(
        lambda: validate_safe_exponent(base, exponent),
        f"validate_safe_exponent should allow safe inputs for base={base}, exponent={exponent}",
    )


def test_validate_safe_exponent_rejects_unsafe_base_gt_one():
    assert_raises_expected(
        lambda: validate_safe_exponent(2, 2000),
        ValueAboveBoundsError,
        "validate_safe_exponent should reject overflow for unsafe exponent values",
    )


def test_validate_safe_exponent_rejects_zero_to_negative_exponent():
    assert_raises_expected(
        lambda: validate_safe_exponent(0, -1),
        ValueBelowBoundsError,
        "validate_safe_exponent should reject 0 raised to a negative exponent",
    )
