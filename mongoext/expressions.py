from mongoext.enums import Operator


class Expression(dict):

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self[self.lhs] = self.rhs


class ComparisonExpression(Expression):

    def __init__(self, field, op, value, negate=False):
        self.field = field
        self.op = op
        self.value = value
        self.negate = negate

        rhs = {self.op: self.value}
        if self.negate:
            rhs = {Operator.NOT: rhs}
        
        super().__init__(self.field, rhs)

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
        return ComparisonExpression(self.field, self.op, self.value, not self.negate)


class LogicalExpression(Expression):

    def __init__(self, op, *exprs):
        self.op = op
        self.exprs = list(exprs)
        super().__init__(self.op, self.exprs)

    def __and__(self, other):
        if not isinstance(other, Expression):
            raise TypeError

        exprs = []
        if self.op == Operator.AND:
            exprs.extend(self.exprs)
        else:
            exprs.append(self)

        if isinstance(other, LogicalExpression) and other.op == Operator.AND:
            exprs.extend(other.exprs)
        else:
            exprs.append(other)

        return and_(*exprs)

    def __or__(self, other):
        if not isinstance(other, Expression):
            raise TypeError
        
        exprs = []
        if self.op == Operator.OR:
            exprs.extend(self.exprs)
        else:
            exprs.append(self)

        if isinstance(other, LogicalExpression) and other.op == Operator.OR:
            exprs.extend(other.exprs)
        else:
            exprs.append(other)

        return or_(*exprs)

    def __neg__(self):
        if self.op == Operator.AND:
            op = Operator.OR
        elif self.op == Operator.OR:
            op = Operator.AND

        exprs = [-expr for expr in self.exprs]
        return LogicalExpression(op, *exprs)


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
    # Maybe deprecate this or simply return the negation of an expression.
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