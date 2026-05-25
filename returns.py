from collections import deque, UserList
from collections.abc import Sequence
from array import array as Array
from .validation import *



def original_sequence_type(input_type: type, data_list: Sequence = []) -> Sequence:
    ''' Return a sequence of the same type as input_type, populated with data_list's elements.

    Converts the provided data_list into a set, tuple, or list, matching the type of input_type.
    If input_type is set, returns a set, if tuple, returns a tuple, otherwise, returns a list.
    
    Ranges are not supported due to the complexity of reliable reconstruction from arbitrary 
    sequences. If range support is required, users should handle this case explicitly.

    Parameters:
        input_type: The type to match (set, tuple, or list).
        data_list: The data to convert.

    Returns:
        A new sequence (set, tuple, or list) containing the elements of data_list.

    Example:
        basic_sequence(list, [1, 2, 3])   # returns [1, 2, 3]
        basic_sequence(tuple, [1, 2, 3])  # returns (1, 2, 3)
        basic_sequence(set, [1, 2, 3])    # returns {1, 2, 3}
    '''
    if not isinstance(data_list, Sequence):
        raise TypeError(f'{input_type} must be a sequence.')
    elif input_type is str:
        return str(data_list)
    elif input_type is tuple:
        return tuple(data_list)
    elif input_type is bytes:
        return bytes(data_list)
    elif input_type is bytearray:
        return bytearray(data_list)
    elif input_type is deque:
        return deque(data_list)
    elif input_type is Array:
        return Array('i', (x for x in data_list))
    elif input_type is UserList:
        return UserList(data_list)
    elif input_type is range:
        raise NotImplementedError(f'range is not supported as range needs to be handled explicitly.')
    else:
        return list(data_list)

