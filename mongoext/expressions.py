from mongoext.enums import Operator


class Expression(dict):

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self[self.lhs] = self.rhs


class ComparisonExpression(Expression):

    def __init__(self, field, op, value):
        self.field = field
        self.op = op
        self.value = value
        super().__init__(self.field, {self.op: self.value})

    def __and__(self , other):
        if not isinstance(other, Expression):
            raise TypeError
        
        if isinstance(other, ComparisonExpression):
            return and_(self, other)

        if isinstance(other, LogicalExpression):
            if other.op == Operator.AND:
                return and_(self, *other.exprs)

            return and_(self, other)
        
    def __or__(self, other):
        if not isinstance(other, Expression):
            raise TypeError
        
        if isinstance(other, ComparisonExpression):
            return or_(self, other)

        if isinstance(other, LogicalExpression):
            if other.op == Operator.OR:
                return or_(self, *other.exprs)

            return or_(self, other)

    def __neg__(self):
        return not_(self.lhs, self.rhs)


class LogicalExpression(Expression):

    def __init__(self, op, *exprs):
        self.op = op
        self.exprs = list(exprs)
        super().__init__(self.op, self.exprs)

    def __and__(self, other):
        if not isinstance(other, Expression):
            raise TypeError

        if isinstance(other, ComparisonExpression):
            return and_(*self.exprs, other)

        if isinstance(other, LogicalExpression):
            if self.op == Operator.AND and other.op == Operator.AND:
                return and_(*self.exprs, *other.exprs)

            if self.op == Operator.AND:
                return and_(*self.exprs, other)

            if other.op == Operator.AND:
                return and_(self, *other.exprs)

            return and_(self, other)

    def __or__(self, other):
        if not isinstance(other, Expression):
            raise TypeError

        if isinstance(other, ComparisonExpression):
            return or_(*self.exprs, other)

        if isinstance(other, LogicalExpression):
            if self.op == Operator.OR and other.op == Operator.OR:
                return or_(*self.exprs, *other.exprs)

            if self.op == Operator.OR:
                return or_(*self.exprs, other)

            if other.op == Operator.OR:
                return or_(self, *other.exprs)

            return or_(self, other)


class ElementExpression(ComparisonExpression):
    pass


# Comparison operators

def eq(field, value):
    return ComparisonExpression(field, Operator.EQ, value)

def ne(field, value):
    return ComparisonExpression(field, Operator.NE, value)

def lt(field, value):
    return ComparisonExpression(field, Operator.LT, value)

def lte(field, value):
    return ComparisonExpression(field, Operator.LTE, value)

def gt(field, value):
    return ComparisonExpression(field, Operator.GT, value)

def gte(field, value):
    return ComparisonExpression(field, Operator.GTE, value)

def in_(field, value):
    return ComparisonExpression(field, Operator.IN, value)

def nin(field, value):
    return ComparisonExpression(field, Operator.NIN, value)


# logical operators

def and_(*exprs):
    return LogicalExpression(Operator.AND, *exprs)

def not_(field, expr):
    return ComparisonExpression(field, Operator.NOT, expr)

def nor(*exprs):
    return LogicalExpression(Operator.NOR, *exprs)

def or_(*exprs):
    return LogicalExpression(Operator.OR, *exprs)


# element operators

def exists(field, value):
    return ElementExpression(field, Operator.EXISTS, bool(value))

def type(field, value):
    return ElementExpression(field, Operator.TYPE, value)