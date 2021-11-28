from mongoext import expressions
        

class Field:
    def __init__(self, name=None):
        self.owner = None
        self.name = name

    def __set_name__(self, owner, name):
        self.owner = owner
        if self.name is None:
            self.name = name

    def __hash__(self):
        if self.owner:
            return hash((self.owner, self.name))
        return hash(self.name)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, value):
        return expressions.eq(self, value)

    def __ne__(self, value):
        return expressions.ne(self, value)

    def __lt__(self, value):
        return expressions.lt(self, value)

    def __le__(self, value):
        return expressions.lte(self, value)

    def __gt__(self, value):
        return expressions.gt(self, value)

    def __ge__(self, value):
        return expressions.gte(self, value)
    