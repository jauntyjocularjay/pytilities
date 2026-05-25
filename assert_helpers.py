"""Shared assertion helpers used across test modules."""

import math

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


def assert_no_exception(callable_obj, context_message):
	actual_exception = None
	try:
		callable_obj()
	except Exception as exc:
		actual_exception = exc
	assert actual_exception is None, (
		f'{context_message}. Expected no exception, '
		f'Actual: {type(actual_exception).__name__ if actual_exception is not None else "No exception"}: {actual_exception}'
	)


def assert_approx_equal(actual, expected, context_message, abs_tol=1e-9):
	is_close = math.isclose(actual, expected, rel_tol=0.0, abs_tol=abs_tol)
	assert is_close, (
		f'{context_message}. Expected approximately: {expected}, Actual: {actual}, Tolerance: {abs_tol}'
	)


def assert_mapping_has_keys(mapping_obj, required_keys, context_message):
	missing_keys = [key for key in required_keys if key not in mapping_obj]
	assert not missing_keys, (
		f'{context_message}. Missing keys: {missing_keys}, Actual keys: {list(mapping_obj.keys())}'
	)


def assert_starts_with(value, prefix, context_message):
	assert isinstance(value, str), (
		f'{context_message}. Expected a string to check prefix, Actual type: {type(value).__name__}'
	)
	assert value.startswith(prefix), (
		f'{context_message}. Expected prefix: {prefix}, Actual value: {value}'
	)

