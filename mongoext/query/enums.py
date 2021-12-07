from datetime import datetime
from decimal import Decimal
from enum import Enum

from bson import ObjectId, Decimal128, Int64, SON


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
    EXISTS = '$exists'
    TYPE = '$type'

    def __str__(self):
        return self.value


# https://docs.mongodb.com/manual/reference/bson-types/

class BSONType(int, Enum):
    DOUBLE = 1
    STRING = 2
    OBJECT = 3
    ARRAY = 4
    BIN_DATA = 5
    UNDEFINED = 6               # Deprecated
    OBJECT_ID = 7
    BOOL = 8
    DATE = 9
    NULL = 10
    REGEX = 11
    DB_POINTER = 12             # Deprecated
    JAVASCRIPT = 13
    SYMBOL = 14                 # Deprecated
    JAVASCRIPT_WITH_SCOPE = 15  # Deprecated
    INT = 16
    TIMESTAMP = 17
    LONG = 18
    DECIMAL = 19
    MIN_KEY = -1
    MAX_KEY = 127

    def __str__(self):
        return self.value


# https://pymongo.readthedocs.io/en/stable/api/bson/

PYTHON_BSON_MAPPING = {
    float: BSONType.DOUBLE,
    str: BSONType.STRING,
    dict: BSONType.OBJECT,
    SON: BSONType.OBJECT,
    list: BSONType.ARRAY, 
    bytes: BSONType.BIN_DATA,
    ObjectId: BSONType.OBJECT_ID,
    bool: BSONType.BOOL,
    datetime: BSONType.DATE,
    None: BSONType.NULL,
    type(None): BSONType.NULL,
    int: BSONType.INT,
    Int64: BSONType.INT,
    Decimal: BSONType.DECIMAL,
    Decimal128: BSONType.DECIMAL
}
