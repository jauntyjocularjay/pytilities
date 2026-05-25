import math as Math
from typing import Any, Union
from fractions import Fraction
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
        super().__init__(f'expected {value} not to be any of {invalid_value_tuple}')

class DuplicateValueError(ValueError):
    def __init__(self, value):
        super().__init__(f'{value} is already represented')

class ValueAboveBoundsError(ValueError):
    def __init__(self, subject, target) -> None:
        super().__init__(f'{subject} is prohibited to be greater than {target}')

class ValueBelowBoundsError(ValueError):
    def __init__(self, subject, target) -> None:
        super().__init__(f'{subject} is prohibited to be less than {target}')

### VALIDATION RAISES ###
# @TODO refactor for more consistency instead of returning true, check the individual case. This will break the boxplot class on change. Be mindful.
def sequence_are_numbers(data_list: Sequence) -> bool:
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

### ### VALIDATORS ###
def validate_as(arg: Any, type: type) -> None:
    """ Validate that arg is an instance of type.

    Parameters
    ----------
    arg : Any
        The value to validate.
    type : type | tuple[type, ...]
        Expected type or tuple of accepted types.

    Raises
    ------
    InvalidTypeError
        If arg is not an instance of type.
    """
    if not isinstance(arg, type): raise InvalidTypeError(arg, type)

def validate_against(subject: Any, invalid_value_tuple: Any) -> None:
    """ Validate that subject is not one of the prohibited values.

    Parameters
    ----------
    subject : Any
        The value to validate.
    invalid_value_tuple : tuple
        Values that are not allowed.

    Raises
    ------
    ProhibitedValueError
        If subject matches any prohibited value.
    """
    for x in invalid_value_tuple:
        if subject == x: raise ProhibitedValueError(subject, invalid_value_tuple)

def validate_float(value: float) -> None:
    """ Validate that value is a finite float-like number.

    Parameters
    ----------
    value : float
        Numeric value to validate.

    Raises
    ------
    ProhibitedValueError
        If value is NaN or infinite.
    """
    if Math.isinf(value) or Math.isnan(value): raise ProhibitedValueError(value, (Math.inf, Math.nan))

def validate_uniqueness(iterable: Iterable, value: Any) -> None:
    """ Validate that value is not already present in iterable.

    Parameters
    ----------
    iterable : Iterable
        Collection to check against.
    value : Any
        Value that must be unique within iterable.

    Raises
    ------
    DuplicateValueError
        If value already exists in iterable.
    """
    if value in iterable: raise DuplicateValueError(value)

def validate_is_greater_than(value: Union[int, float, Fraction], target: Union[int, float, Fraction]) -> None:
    """ Validate that value is strictly greater than target.

    Parameters
    ----------
    value : Any
        Value being compared.
    target : Any
        Lower strict bound.

    Raises
    ------
    ValueBelowBoundsError
        If value is less than or equal to target.
    """
    if value > target: return
    else: raise ValueBelowBoundsError(value, target)

def validate_igt(value: Union[int, float, Fraction], target: Union[int, float, Fraction]) -> None:
    """ Alias for validate_is_greater_than."""
    validate_is_greater_than(value, target)

def validate_is_greater_or_equal_to(value: Union[int, float, Fraction], target: Union[int, float, Fraction]) -> None:
    """ Validate that value is greater than or equal to target.

    Parameters
    ----------
    value : Any
        Value being compared.
    target : Any
        Lower inclusive bound.

    Raises
    ------
    ValueBelowBoundsError
        If value is less than target.
    """
    if value >= target: return
    else: raise ValueBelowBoundsError(value, target)
    
def validate_ige(value: Union[int, float, Fraction], target) -> None:
    """ Alias for validate_is_greater_or_equal_to."""
    validate_is_greater_or_equal_to(value, target)

def validate_is_less_than(value: Union[int, float, Fraction], target: Union[int, float, Fraction]) -> None:
    """ Validate that value is strictly less than target.

    Parameters
    ----------
    value : Any
        Value being compared.
    target : Any
        Upper strict bound.

    Raises
    ------
    ValueAboveBoundsError
        If value is greater than or equal to target.
    """
    if value < target: return 
    else: raise ValueAboveBoundsError(value, target)

def validate_ilt(value: Union[int, float, Fraction], target: Union[int, float, Fraction]) -> None:
    """ Alias for validate_is_less_than."""
    validate_is_less_than(value, target)

def validate_is_less_or_equal_to(value: Union[int, float, Fraction], target: Union[int, float, Fraction]) -> None:
    """ Validate that value is less than or equal to target.

    Parameters
    ----------
    value : Any
        Value being compared.
    target : Any
        Upper inclusive bound.

    Raises
    ------
    ValueAboveBoundsError
        If value is greater than target.
    """
    if value <= target: return 
    else: raise ValueAboveBoundsError(value, target)

def validate_ile(value: Union[int, float, Fraction], target: Union[int, float, Fraction]) -> None:
    """ Alias for validate_is_less_or_equal_to."""
    
    validate_is_less_or_equal_to(value, target)

def validate_safe_exponent(base: Union[int, float, Fraction], exponent: Union[int, float, Fraction], max_float: float = 709.78) -> None:
    """
    Validates that base**exponent will not overflow the floating-point range.

    For base > 1, raises ValueAboveBoundsError if exponent exceeds the safe bound:
        exponent > ln(max_float) / ln(base)
    For base <= 1, always passes (no overflow possible).

    Parameters
    ----------
    base : float or int
        The base of the exponentiation (must be positive).
    exponent : float or int
        The exponent value.
    max_float : float, optional
        The maximum float value to guard against (default: 709.78 for IEEE 754 double precision).

    Raises
    ------
    ValueAboveBoundsError
        If base > 1 and exponent is too large to safely compute base**exponent as a float.
    """
    exponent_bound = Math.log(max_float)/Math.log(base)
    if base > 1 and exponent > exponent_bound:
        raise ValueAboveBoundsError(exponent, exponent_bound)
    else:
        return
