from enum import Enum


class Operator(str, Enum):
    EQ = '$eq'
    NE = '$ne'
    GT = '$gt'
    GTE = '$gte'
    LT = '$lt'
    LTE = '$lte'
    IN = '$in'
    NIN = '$nin'
    AND = '$and'
    OR = '$or'
    NOT = '$not'
    #NOR = '$nor'
    EXISTS = '$exists'
    TYPE = '$type'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value



class BsonType(Enum):
    DOUBLE = 1
    STRING = 2
    OBJECT = 3
    ARRAY = 4
    BIN_DATA = 5
    UNDEFINED = 6
    OBJECT_ID = 7
    BOOL = 8
    DATE = 9
    NULL = 10
    REGEX = 11
    DB_POINTER = 12
    JAVASCRIPT = 13
    SYMBOL = 14
    JAVASCRIPT_WITH_SCOPE = 15
    INT = 16
    TIMESTAMP = 17
    LONG = 18
    DECIMAL = 19
    MIN_KEY = -1
    MAX_KEY = 127
