# pytilities

A collection of Python utility modules for input validation, sequence handling, console control, and card representation.

## LLM Disclosure

All working base code is written by an actual human, [@jauntyjocularjay](https://github.com/jauntyjocularjay). LLM @Copilot is used to author documentation, docstrings, and unit tests with editing and fine tuning by @jauntyjocularjay.

## Table of Contents

- [LLM Disclosure](#llm-disclosure)
- [`console.py`](#consolepy)
  - [`console.clear()`](#consoleclear)
- [`validation.py`](#validationpy)
  - [Errors](#errors)
  - [Validators](#validators)
- [`returns.py`](#returnspy)
  - [`original_sequence_type`](#original_sequence_type)
- [`pytest_helpers.py`](#pytest_helperspy)
  - [Shared Test Assertions](#shared-test-assertions)
- [Test Runner](#test-runner)
  - [Bash](#bash)
  - [PowerShell](#powershell)

---

## `console.py`

### `console.clear()`

Clears the terminal. Uses `clear` on POSIX systems and `cls` on Windows. Prints two blank lines after clearing to prevent terminal overhang on some terminals.

```python
from pytilities import console
console.clear()
```

---

## `validation.py`

### Errors

| Class | Type | Description |
| --- | --- | --- |
| `InvalidSequenceError` | `TypeError` | Raised when an argument is not a valid `Sequence`. |
| `NotNumericSequenceError` | `TypeError` | Raised when a sequence contains non-numeric elements. |
| `InvalidTypeError` | `TypeError` | Raised when an argument is not an instance of the expected type. |
| `ProhibitedValueError` | `ValueError` | Raised when a value matches a prohibited value. |
| `DuplicateValueError` | `ValueError` | Raised when a value is already present in an iterable. |
| `ValueAboveBoundsError` | `ValueError` | Raised when a value is greater than an allowed upper bound. |
| `ValueBelowBoundsError` | `ValueError` | Raised when a value is less than a required lower bound. |

### Validators

| Function | Description |
| --- | --- |
| `sequence_are_numbers(data_list)` | Returns `True` if all elements are finite `int` or `float`; raises `InvalidSequenceError` if not a sequence. |
| `validate_as(arg, type)` | Raises `InvalidTypeError` if `arg` is not an instance of `type`. |
| `validate_against(subject, invalid_value_tuple)` | Raises `ProhibitedValueError` if `subject` matches any value in `invalid_value_tuple`. |
| `validate_float(value)` | Raises `ProhibitedValueError` if `value` is `inf` or `nan`. |
| `validate_uniqueness(iterable, value)` | Raises `DuplicateValueError` if `value` is already in `iterable`. |
| `validate_is_greater_than(value, target)` | Strict lower-bound check (`value > target`), else raises `ValueBelowBoundsError`. |
| `validate_igt(value, target)` | Alias for `validate_is_greater_than`. |
| `validate_is_greater_or_equal_to(value, target)` | Inclusive lower-bound check (`value >= target`), else raises `ValueBelowBoundsError`. |
| `validate_ige(value, target)` | Alias for `validate_is_greater_or_equal_to`. |
| `validate_is_less_than(value, target)` | Strict upper-bound check (`value < target`), else raises `ValueAboveBoundsError`. |
| `validate_ilt(value, target)` | Alias for `validate_is_less_than`. |
| `validate_is_less_or_equal_to(value, target)` | Inclusive upper-bound check (`value <= target`), else raises `ValueAboveBoundsError`. |
| `validate_ile(value, target)` | Alias for `validate_is_less_or_equal_to`. |
| `validate_safe_exponent(base, exponent, max_float=709.78)` | Raises `ValueAboveBoundsError` when `base > 1` and `base**exponent` would exceed safe float limits. |

---

## `returns.py`

### `original_sequence_type`

Returns a new sequence of the same type as `input_type`, populated with the elements of `data_list`. Supports `list`, `tuple`, `set`, `str`, `bytes`, `bytearray`, `deque`, `array`, and `UserList`. Raises `NotImplementedError` for `range`.

```python
from pytilities.returns import original_sequence_type
original_sequence_type(tuple, [1, 2, 3])  # returns (1, 2, 3)
original_sequence_type(set, [1, 2, 3])    # returns {1, 2, 3}
original_sequence_type(list, [1, 2, 3])   # returns [1, 2, 3]
```

---

## `pytest_helpers.py`

### Shared Test Assertions

Reusable pytest assertion helpers for clearer, DRYer tests across projects.

This section and helper design were created with Github_CoPilot.

| Function | Description |
| --- | --- |
| `assert_raises_expected(callable_obj, expected_exception_type, context_message)` | Executes `callable_obj` and asserts that it raises `expected_exception_type`; returns the captured exception for optional message checks. |
| `assert_no_exception(callable_obj, context_message)` | Executes `callable_obj` and asserts that no exception is raised. |
| `assert_approx_equal(actual, expected, context_message, abs_tol=1e-9)` | Asserts numeric approximate equality using `pytest.approx` with absolute tolerance. |
| `assert_mapping_has_keys(mapping_obj, required_keys, context_message)` | Asserts that all `required_keys` exist in a mapping, with missing-key diagnostics. |
| `assert_starts_with(value, prefix, context_message)` | Asserts that a string starts with the expected prefix, with type and value diagnostics. |

---

## Test Runner

### Bash

```bash
# Run from the project root (the parent of pytilities)
$ cd path/to/module/parent

# Run a specific test file
$ poetry run pytest -v pytilities/test_validation.py
$ poetry run pytest -v pytilities/test_returns.py

# Run tests with coverage report
$ poetry run pytest --cov=pytilities --cov-report=term -v pytilities/
```

### PowerShell

```powershell
# Run from the project root (the parent of pytilities)
cd path\to\module\parent

# Run a specific test file
poetry run pytest -v pytilities/test_validation.py
poetry run pytest -v pytilities/test_returns.py

# Run tests with coverage report
poetry run pytest --cov=pytilities --cov-report=term -v pytilities/
```

All tests are DRY, readable, and use the latest API. See `test_validation.py` and `test_returns.py` for examples.
