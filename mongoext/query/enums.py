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

class BSONType(Enum):
    DOUBLE = 1, "double"
    STRING = 2, "string"
    OBJECT = 3, "object"
    ARRAY = 4, "array"
    BIN_DATA = 5, "binData"
    # UNDEFINED = 6, "undefined"
    OBJECT_ID = 7, "objectId"
    BOOL = 8, "bool"
    DATE = 9, "date"
    NULL = 10, "null"
    REGEX = 11, "regex"
    # DB_POINTER = 12, "dbPointer"
    JAVASCRIPT = 13, "javascript" 
    # SYMBOL = 14, "pointer"
    # JAVASCRIPT_WITH_SCOPE = 15, "javascriptWithScope"
    INT = 16, "int" 
    TIMESTAMP = 17, "timestamp" 
    LONG = 18, "long" 
    DECIMAL = 19, "decimal" 
    MIN_KEY = -1, "minKey" 
    MAX_KEY = 127, "maxKey" 

    def __init__(self, number, alias):
        self.number = number
        self.alias = alias

    def __eq__(self, other):
        if isinstance(other, int):
            return self.number == other

        if isinstance(other, str):
            return self.alias == other

        return super().__eq__(other)

    def __str__(self):
        return self.alias


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
