from enum import Enum
from validation import validate_as


class Face(Enum):
    ACE = 'Ace'
    KNAVE = 'Knave'
    KNIGHT = 'Knight'
    QUEEN = 'Queen'
    KING = 'King'

class Suit(Enum):
    CUPS = 'Cups'
    PENTACLES = 'Pentacles'
    SWORDS = 'Swords'
    WANDS = 'Wands'
    DIAMONDS = 'Diamonds'
    HEARTS = 'Hearts'
    SPADES = 'Spades'
    CLUBS = 'Clubs'

class card:

    def __init__(self, value: int, suit: Suit):
        validate_as(value, int)
        validate_as(suit, Suit)

        self._value = value
        self._suit = suit

    @property
    def value(self):
        return self._value

    @property
    def suit(self):
        return self._suit


    def __str__(self):
        result = f':value of :suit'

        if self.value == 1:
            result = result.replace(':value', Face.ACE.value)
        elif self.value == 11:
            result = result.replace(':value', Face.KNAVE.value)
        elif self.value == 12:
            result = result.replace(':value', Face.KNIGHT.value)
        elif self.value == 13:
            result = result.replace(':value', Face.QUEEN.value)
        elif self.value == 14:
            result = result.replace(':value', Face.KING.value)
        else:
            result = result.replace(':value', str(self.value))

        result = result.replace(':suit', self._suit.value)

        return result
        
queen = card(13, Suit.HEARTS)

print(queen)