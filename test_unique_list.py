import pytest


''' unique_list is an unfinished class.

See the dosctring in the class file for more information. It will remain unfinished for now.
'''
pytest.skip('Skipping unique_list tests unless explicitly requested.', allow_module_level=True)

# --- Tests for append, insert, and extend ---
def test_append_unique_value():
    '''Appending a unique value adds it to the end and lookup_set.'''
    ls = unique_list(1, 2, 3)
    before = list(ls)
    ls.append(4)
    after = list(ls)
    assert after == [1, 2, 3, 4], (
        f'Append 4.\nBefore: {before}\nAfter: {after}\nExpected [1, 2, 3, 4], got {after}'
    )
    assert 4 in ls.lookup_set, (
        f'Append 4.\nExpected 4 in lookup_set, got {ls.lookup_set}'
    )

def test_append_duplicate_value():
    '''Appending a duplicate value does nothing.'''
    ls = unique_list(1, 2, 3)
    before = list(ls)
    ls.append(2)
    after = list(ls)
    assert after == before, (
        f'Append duplicate 2.\nBefore: {before}\nAfter: {after}\nExpected no change.'
    )

def test_insert_unique_value():
    '''Inserting a unique value at an index adds it and updates lookup_set.'''
    ls = unique_list(1, 2, 3)
    before = list(ls)
    ls.insert(1, 4)
    after = list(ls)
    assert after == [1, 4, 2, 3], (
        f'Insert 4 at 1.\nBefore: {before}\nAfter: {after}\nExpected [1, 4, 2, 3], got {after}'
    )
    assert 4 in ls.lookup_set, (
        f'Insert 4 at 1.\nExpected 4 in lookup_set, got {ls.lookup_set}'
    )

def test_insert_duplicate_value():
    '''Inserting a duplicate value does nothing.'''
    ls = unique_list(1, 2, 3)
    before = list(ls)
    ls.insert(1, 2)
    after = list(ls)
    assert after == before, (
        f'Insert duplicate 2 at 1.\nBefore: {before}\nAfter: {after}\nExpected no change.'
    )

def test_extend_with_all_unique():
    '''Extending with all unique values adds them to the end and updates lookup_set.'''
    ls = unique_list(1, 2)
    before = list(ls)
    ls.extend([3, 4])
    after = list(ls)
    assert after == [1, 2, 3, 4], (
        f'Extend with [3, 4].\nBefore: {before}\nAfter: {after}\nExpected [1, 2, 3, 4], got {after}'
    )
    assert set(ls.lookup_set) == {1, 2, 3, 4}, (
        f'Extend with [3, 4].\nExpected lookup_set {{1, 2, 3, 4}}, got {ls.lookup_set}'
    )

def test_extend_with_some_duplicates():
    '''Extending with some duplicates only adds new unique values.'''
    ls = unique_list(1, 2)
    before = list(ls)
    ls.extend([2, 3, 1, 4])
    after = list(ls)
    assert after == [1, 2, 3, 4], (
        f'Extend with [2, 3, 1, 4].\nBefore: {before}\nAfter: {after}\nExpected [1, 2, 3, 4], got {after}'
    )
    assert set(ls.lookup_set) == {1, 2, 3, 4}, (
        f'Extend with [2, 3, 1, 4].\nExpected lookup_set {{1, 2, 3, 4}}, got {ls.lookup_set}'
    )

def test_extend_with_all_duplicates():
    '''Extending with all duplicates does nothing.'''
    ls = unique_list(1, 2, 3)
    before = list(ls)
    ls.extend([2, 1, 3])
    after = list(ls)
    assert after == before, (
        f'Extend with [2, 1, 3] (all duplicates).\nBefore: {before}\nAfter: {after}\nExpected no change.'
    )
# --- Edge case tests for unique_list ---
def test_setitem_slice_empty_sequence():
    '''Assigning an empty sequence to a slice removes the slice.'''
    ls = unique_list(1, 2, 3, 4)
    before = list(ls)
    ls[1:3] = []
    after = list(ls)
    assert after == [1, 4], (
        f'Set empty slice at 1:3.\nBefore: {before}\nAfter: {after}\nExpected [1, 4], got {after}'
    )
    assert ls.lookup_set == {1, 4}, (
        f'Set empty slice at 1:3.\nExpected lookup_set {{1, 4}}, got {ls.lookup_set}'
    )

def test_setitem_slice_all_duplicates():
    '''Assigning a slice of all duplicates moves those values to the new indices, maintaining uniqueness.'''
    ls = unique_list(1, 2, 3, 4)
    seq = [2, 3]
    before = list(ls)
    ls[1:3] = seq
    after = list(ls)
    assert after == [1, 2, 3, 4], (
        f'Set slice {seq} at 1:3 (all duplicates).\nBefore: {before}\nAfter: {after}\nExpected [1, 2, 3, 4], got {after}'
    )
    assert ls.count(2) == 1 and ls.count(3) == 1, (
        f'Set slice {seq} at 1:3 (all duplicates).\nExpected only one of each value.'
    )

def test_setitem_slice_at_start():
    '''Assigning a slice at the start of the list.'''
    ls = unique_list(1, 2, 3, 4)
    seq = [5, 6]
    before = list(ls)
    ls[:2] = seq
    after = list(ls)
    assert after == [5, 6, 3, 4], (
        f'Set slice {seq} at :2.\nBefore: {before}\nAfter: {after}\nExpected [5, 6, 3, 4], got {after}'
    )
    assert set(ls) == {3, 4, 5, 6}, (
        f'Set slice {seq} at :2.\nExpected set {{3, 4, 5, 6}}, got {set(ls)}'
    )

def test_setitem_slice_at_end():
    '''Assigning a slice at the end of the list.'''
    ls = unique_list(1, 2, 3, 4)
    seq = [7, 8]
    before = list(ls)
    ls[2:] = seq
    after = list(ls)
    assert after == [1, 2, 7, 8], (
        f'Set slice {seq} at 2:.\nBefore: {before}\nAfter: {after}\nExpected [1, 2, 7, 8], got {after}'
    )
    assert set(ls) == {1, 2, 7, 8}, (
        f'Set slice {seq} at 2:.\nExpected set {{1, 2, 7, 8}}, got {set(ls)}'
    )

def test_setitem_slice_replace_with_self():
    '''Assigning the same values to the same slice should not change the list.'''
    ls = unique_list(1, 2, 3, 4)
    before = list(ls)
    ls[1:3] = [2, 3]
    after = list(ls)
    assert after == before, (
        f'Set slice [2, 3] at 1:3 (replace with self).\nBefore: {before}\nAfter: {after}\nExpected no change.'
    )

def test_setitem_slice_insert_duplicate_at_start():
    '''Assigning a slice at the start with a duplicate value moves it to the start.'''
    ls = unique_list(1, 2, 3, 4)
    seq = [3, 5]
    before = list(ls)
    ls[:2] = seq
    after = list(ls)
    assert after == [3, 5, 1, 4], (
        f'Set slice {seq} at :2 (duplicate at start).\nBefore: {before}\nAfter: {after}\nExpected [3, 5, 1, 4], got {after}'
    )
    assert ls.count(3) == 1, (
        f'Set slice {seq} at :2 (duplicate at start).\nExpected only one 3.'
    )

# Tests for unique_list move-on-duplicate and uniqueness enforcement
from .unique_list import unique_list
from .validation import DuplicateValueError

def test_setitem_assigns_new_unique_value():
    '''Assigning a new unique value at an index replaces the old value and updates lookup_set.'''
    ls = unique_list(1, 2, 3)
    before = list(ls)
    ls[0] = 4
    after = list(ls)
    # Assigning a new unique value replaces the old value
    assert ls[0] == 4, (
        f'Assign 4 at index 0.\nBefore: {before}\nAfter: {after}\nExpected ls[0] == 4, got {ls[0]}'
    )
    # The new value is in lookup_set
    assert 4 in ls.lookup_set, (
        f'Assign 4 at index 0.\nBefore: {before}\nAfter: {after}\nExpected 4 in lookup_set, got {ls.lookup_set}'
    )
    # The replaced value is removed from lookup_set
    assert 1 not in ls.lookup_set, (
        f'Assign 4 at index 0.\nBefore: {before}\nAfter: {after}\nExpected 1 not in lookup_set, got {ls.lookup_set}'
    )


def test_setitem_moves_existing_value_to_new_index():
    '''Assigning a value already present in the list moves it to the new index, maintaining uniqueness.'''
    ls = unique_list(1, 2, 3)
    before = list(ls)
    ls[0] = 2  # 2 already exists, should move 2 to index 0
    after = list(ls)
    # The moved value is now at the new index
    assert ls[0] == 2, (
        f'Move value 2 to index 0.\nBefore: {before}\nAfter: {after}\nExpected ls[0] == 2, got {ls[0]}'
    )
    # There is still only one instance of the value
    assert ls.count(2) == 1, (
        f'Move value 2 to index 0.\nBefore: {before}\nAfter: {after}\nExpected only one 2 in list, got {ls.count(2)}'
    )
    # The list contents remain unique and sorted order is preserved for comparison
    assert sorted(ls) == [1, 2, 3], (
        f'Move value 2 to index 0.\nBefore: {before}\nAfter: {after}\nExpected sorted(ls) == [1, 2, 3], got {sorted(ls)}'
    )


def test_setitem_slice_assigns_unique_values():
    '''Assigning a slice with all unique values replaces the slice and updates lookup_set accordingly.'''
    ls = unique_list(1, 2, 3, 4)
    before = list(ls)
    seq = [5, 6]
    ls[1:3] = seq
    after = list(ls)
    # The assigned values appear at the correct indices
    assert ls[1] == 5 and ls[2] == 6, (
        f'Set slice {seq} at index 1:3.\nBefore: {before}\nAfter: {after}\nExpected ls[1:3] == {seq}, got {ls[1:3]}'
    )
    # The new values are in lookup_set
    assert 5 in ls.lookup_set and 6 in ls.lookup_set, (
        f'Set slice {seq} at index 1:3.\nBefore: {before}\nAfter: {after}\nExpected 5 and 6 in lookup_set, got {ls.lookup_set}'
    )
    # The replaced values are removed from lookup_set
    assert 2 not in ls.lookup_set and 3 not in ls.lookup_set, (
        f'Set slice {seq} at index 1:3.\nBefore: {before}\nAfter: {after}\nExpected 2 and 3 not in lookup_set, got {ls.lookup_set}'
    )


def test_setitem_slice_moves_duplicate_value():
    '''Assigning a slice containing a value already present in the list moves that value to the new index, maintaining uniqueness.'''
    ls = unique_list(1, 2, 3, 4)
    seq = [2, 5]
    before = list(ls)
    ls[1:3] = seq  # 2 already exists, should move 2 to index 1
    after = list(ls)
    # The moved value appears at the correct index
    assert ls[1] == 2 and ls[2] == 5, (
        f'Set slice {seq} at index 1:3.\nBefore: {before}\nAfter: {after}\nExpected ls[1:3] == {seq}, got {ls[1:3]}'
    )
    # There is still only one instance of the moved value
    assert ls.count(2) == 1, (
        f'Set slice {seq} at index 1:3.\nBefore: {before}\nAfter: {after}\nExpected only one 2 in list after slice, got {ls.count(2)}'
    )
    # The list contents remain unique and sorted order is preserved for comparison
    assert sorted(ls) == [1, 2, 4, 5], (
        f'Set slice {seq} at index 1:3.\nBefore: {before}\nAfter: {after}\nExpected sorted(ls) == [1, 2, 4, 5], got {sorted(ls)}'
    )
