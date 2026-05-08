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
- [`card.py`](#cardpy)
  - [`Face`](#face)
  - [`Suit`](#suit)
  - [`card`](#card)
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
|---|---|---|
| `InvalidSequenceError` | `TypeError` | Raised when an argument is not a valid `Sequence`. |
| `NotNumericSequenceError` | `TypeError` | Raised when a sequence contains non-numeric elements. |
| `InvalidTypeError` | `TypeError` | Raised when an argument is not an instance of the expected type. |
| `ProhibitedValueError` | `ValueError` | Raised when a value matches a prohibited value. |
| `DuplicateValueError` | `ValueError` | Raised when a value is already present in an iterable. |
| `ValueAboveBoundsError` | `ValueError` | Raised when a value is less than a required minimum. |
| `ValueBelowBoundsError` | `ValueError` | Raised when a value is greater than a required maximum. |

### Validators

| Function | Description |
|---|---|
| `sequence_are_numbers(data_list)` | Returns `True` if all elements are finite `int` or `float`; raises `InvalidSequenceError` if not a sequence. |
| `validate_as(arg, type)` | Raises `InvalidTypeError` if `arg` is not an instance of `type`. |
| `validate_against(subject, invalid_value_tuple)` | Raises `ProhibitedValueError` if `subject` matches any value in `invalid_value_tuple`. |
| `validate_float(value)` | Raises `ProhibitedValueError` if `value` is `inf` or `nan`. |
| `validate_uniqueness(iterable, value)` | Raises `DuplicateValueError` if `value` is already in `iterable`. |
| `validate_is_greater_than(value, target)` | Raises `ValueAboveBoundsError` if `value < target`. |
| `validate_is_less_than(value, target)` | Raises `ValueBelowBoundsError` if `value > target`. |

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

## `card.py`

### `Face`

Enum of named card face values: `ACE`, `KNAVE`, `KNIGHT`, `QUEEN`, `KING`.

### `Suit`

Enum of card suits supporting both tarot and standard playing card decks:
`CUPS`, `PENTACLES`, `SWORDS`, `WANDS`, `DIAMONDS`, `HEARTS`, `SPADES`, `CLUBS`.

### `card`

Represents a single playing card with an integer `value` and a `Suit`. Face values 1, 11–14 are rendered as their `Face` name in `__str__`; all others render as the integer.

```python
from pytilities.card import card, Suit
c = card(13, Suit.HEARTS)
str(c)  # 'Queen of Hearts'
```

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
