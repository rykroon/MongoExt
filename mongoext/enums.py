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

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class BsonType(int, Enum):
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

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return self.value


PYTHON_BSON_MAPPING = {
    float: BsonType.DOUBLE,
    str: BsonType.STRING,
    dict: BsonType.OBJECT,
    SON: BsonType.OBJECT,
    list: BsonType.ARRAY, 
    bytes: BsonType.BIN_DATA,
    ObjectId: BsonType.OBJECT_ID,
    bool: BsonType.BOOL,
    datetime: BsonType.DATE,
    None: BsonType.NULL,
    type(None): BsonType.NULL,
    int: BsonType.INT,
    Int64: BsonType.INT,
    Decimal: BsonType.DECIMAL,
    Decimal128: BsonType.DECIMAL
}
