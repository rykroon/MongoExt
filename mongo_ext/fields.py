from mongo_ext import operators
        


class Field:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, value):
        return operators.eq(self, value)

    def __ne__(self, value):
        return operators.ne(self, value)

    def __lt__(self, value):
        return operators.lt(self, value)

    def __le__(self, value):
        return operators.lte(self, value)

    def __gt__(self, value):
        return operators.gt(self, value)

    def __ge__(self, value):
        return operators.gte(self, value)
    