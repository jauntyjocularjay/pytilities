
"""
Test suite for the original_sequence_type function in returns.py.

This module covers all supported sequence types, error cases, and edge cases for
the original_sequence_type utility, ensuring correct type preservation and conversion.
"""

import pytest
from .returns import original_sequence_type
from collections import deque, UserList
from array import array as Array


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

# --- List, Tuple, Set ---
def test_return_list():
    '''Test: returns a list when input_type is list.'''
    result = original_sequence_type(list, (1, 2, 3))
    assert isinstance(result, list), f'Should return a list for list input_type. Expected: list, Actual: {type(result).__name__}'
    assert result == [1, 2, 3], f'Should preserve elements for list input_type. Expected: [1, 2, 3], Actual: {result}'

def test_return_tuple():
    '''Test: returns a tuple when input_type is tuple.'''
    result = original_sequence_type(tuple, [1, 2, 3])
    assert isinstance(result, tuple), f'Should return a tuple for tuple input_type. Expected: tuple, Actual: {type(result).__name__}'
    assert result == (1, 2, 3), f'Should preserve elements for tuple input_type. Expected: (1, 2, 3), Actual: {result}'

def test_return_set():
    '''Test: returns a set when input_type is set.'''
    result = original_sequence_type(set, [1, 2, 3, 2])
    assert isinstance(result, set), f'Should return a set for set input_type. Expected: set, Actual: {type(result).__name__}'
    assert set(result) == {1, 2, 3}, f'Should preserve unique elements for set input_type. Expected: {{1, 2, 3}}, Actual: {set(result)}'

# --- String, Bytes, Bytearray ---
def test_return_str():
    '''Test: returns a string when input_type is str.'''
    result = original_sequence_type(str, ['a', 'b', 'c'])
    expected = str(['a', 'b', 'c'])
    assert result == expected, f'Should return string representation for str input_type. Expected: {expected}, Actual: {result}'

def test_return_bytes():
    '''Test: returns bytes when input_type is bytes.'''
    result = original_sequence_type(bytes, [65, 66, 67])
    assert isinstance(result, bytes), f'Should return bytes for bytes input_type. Expected: bytes, Actual: {type(result).__name__}'
    assert result == b'ABC', f'Should match bytes representation for ASCII values. Expected: b\'ABC\', Actual: {result}'

def test_return_bytearray():
    '''Test: returns bytearray when input_type is bytearray.'''
    result = original_sequence_type(bytearray, [65, 66, 67])
    assert isinstance(result, bytearray), f'Should return bytearray for bytearray input_type. Expected: bytearray, Actual: {type(result).__name__}'
    expected = bytearray(b'ABC')
    assert result == expected, f'Should match bytearray representation for ASCII values. Expected: {expected}, Actual: {result}'

# --- Range ---
def test_return_range():
    '''Test: raises NotImplementedError for any range input_type.'''
    assert_raises_expected(
        lambda: original_sequence_type(range, [5]),
        NotImplementedError,
        'original_sequence_type should raise for range input_type',
    )

# --- Deque ---
def test_return_deque():
    '''Test: returns a deque when input_type is deque.'''
    result = original_sequence_type(deque, [1, 2, 3])
    assert isinstance(result, deque), f'Should return a deque for deque input_type. Expected: deque, Actual: {type(result).__name__}'
    assert list(result) == [1, 2, 3], f'Should preserve elements for deque input_type. Expected: [1, 2, 3], Actual: {list(result)}'

# --- Array ---
def test_return_array():
    '''Test: returns an array when input_type is Array.'''
    result = original_sequence_type(Array, [1, 2, 3])
    assert isinstance(result, Array), f'Should return an array for Array input_type. Expected: Array, Actual: {type(result).__name__}'
    assert list(result) == [1, 2, 3], f'Should preserve elements for Array input_type. Expected: [1, 2, 3], Actual: {list(result)}'

# --- UserList ---
def test_return_userlist():
    '''Test: returns a UserList when input_type is UserList.'''
    result = original_sequence_type(UserList, [1, 2, 3])
    assert isinstance(result, UserList), f'Should return a UserList for UserList input_type. Expected: UserList, Actual: {type(result).__name__}'
    assert list(result) == [1, 2, 3], f'Should preserve elements for UserList input_type. Expected: [1, 2, 3], Actual: {list(result)}'

# --- Error Cases ---
def test_non_sequence_input():
    '''Test: raises TypeError if data_list is not a Sequence.'''
    assert_raises_expected(
        lambda: original_sequence_type(list, 123), # pyright: ignore[reportArgumentType]
        TypeError,
        'original_sequence_type should raise TypeError for non-sequence input',
    )

def test_fallthrough_branch():
    '''Test: returns data as a list if input_type is not handled.'''
    class Dummy: pass
    result = original_sequence_type(Dummy, [1, 2, 3])
    assert isinstance(result, list), f'Should return a list for unhandled input_type. Expected: list, Actual: {type(result).__name__}'
