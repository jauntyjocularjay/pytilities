import math as Math
from collections.abc import Sequence, Iterable



### ERRORS ###
### ### TYPE ERRORS ###
class InvalidSequenceError(TypeError):
    """Exception raised when an argument is not a valid sequence.

    Raised by statistical functions when the input is not a sequence type (e.g., list, tuple, set).

    Example:
        if not isinstance(data_list, Sequence):
            raise InvalidSequenceError
    """
    def __init__(self, message=f"expected a {Sequence}"):
        super().__init__(message)

class NotNumericSequenceError(TypeError):
    """Exception raised when a sequence contains non-numeric elements.

    Raised by statistical functions when the input sequence contains elements that are not real numbers.

    Example:
        if not sequence_are_numbers(data_list):
            raise NotNumericSequenceError
    """
    def __init__(self, message=f"expected a {Sequence} of {(int, float)} excluding {(Math.inf, Math.nan)}"):
        super().__init__(message)

class InvalidTypeError(TypeError):
    def __init__(self, data, expected_type):
        super().__init__(f'expected {data} of {type(data)} to be an instance of {expected_type}')

### ### VALUE ERRORS ###
class ProhibitedValueError(ValueError):
    def __init__(self, value, invalid_value_tuple):
        super().__init__(f'expected {value} not to be one of these {invalid_value_tuple}')

class DuplicateValueError(ValueError):
    def __init__(self, value):
        super().__init__(f'{value} is already represented')

### VALIDATION RAISES ###
# @TODO refactor for more consistency instead of returning true, check the individual case. This will break the class on change. Be mindful.
def sequence_are_numbers(data_list: Sequence):
    """ Checks that all elements in data_list are numeric (int or float), or that data_list is None.

    This function is intended to validate input for statistical analysis functions. If any element
    in the list is not an integer or float.

    Parameters:
        data_list (list or None): The input list to check.

    Raises:
        TypeError: If any element in data_list is not an int or float.

    Example:
        sequence_are_numbers([1, 2.5, 3])    # returns True
        sequence_are_numbers(['a', 2, 3])    # returns false
        sequence_are_numbers(None)            # raises TypeError
    """
    if not isinstance(data_list, Sequence) or isinstance(data_list, (str,bytes)):
        raise InvalidSequenceError

    for x in data_list:
        if not isinstance(x, (int, float)) or Math.isnan(x) or Math.isinf(x) or isinstance(x, bool):
            return False

    return True

def validate_as(arg, type):
    if not isinstance(arg, type): raise InvalidTypeError(arg, type)

def validate_against(subject, invalid_value_tuple):
    for x in invalid_value_tuple:
        if subject == x: raise ProhibitedValueError(subject, invalid_value_tuple)

def validate_float(value):
    if Math.isinf(value) or Math.isnan(value): raise ProhibitedValueError(value, (Math.inf, Math.nan))

def validate_uniqueness(sequence: Iterable, value):
    if value in sequence: raise DuplicateValueError(value)



