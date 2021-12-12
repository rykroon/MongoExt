import unittest

from mongoext.fields import Field


class TestOperators(unittest.TestCase):

    def setUp(self):
        self.foo = Field('foo')
        class Bar:
            baz = Field()

        self.Bar = Bar

    def test_eq(self):
        assert (self.foo == 'Hello World') == {
            'foo': {'$eq': 'Hello World'}
        }

        assert (self.Bar.baz == 10) == {
            'baz': {'$eq': 10}
        }

    def test_ne(self):
        assert (self.foo != 'Hello World') == {
            'foo': {'$ne': 'Hello World'}
        }

        assert (self.Bar.baz != 10) == {
            'baz': {'$ne': 10}
        }

    def test_lt(self):
        assert (self.foo < 'Hello World') == {
            'foo': {'$lt': 'Hello World'}
        }

        assert (self.Bar.baz < 10) == {
            'baz': {'$lt': 10}
        }

    def test_lte(self):
        assert (self.foo <= 'Hello World') == {
            'foo': {'$lte': 'Hello World'}
        }

        assert (self.Bar.baz <= 10) == {
            'baz': {'$lte': 10}
        }

    def test_gt(self):
        assert (self.foo > 'Hello World') == {
            'foo': {'$gt': 'Hello World'}
        }

        assert (self.Bar.baz > 10) == {
            'baz': {'$gt': 10}
        }

    def test_gte(self):
        assert (self.foo >= 'Hello World') == {
            'foo': {'$gte': 'Hello World'}
        }

        assert (self.Bar.baz >= 10) == {
            'baz': {'$gte': 10}
        }

    def test_in(self):
        assert (self.foo.in_(['Hello', 'World'])) == {
            'foo': {'$in': ['Hello', 'World']}
        }

        assert (self.Bar.baz.in_([10, 20, 30])) == {
            'baz': {'$in': [10, 20, 30]}
        }

    def test_not_in(self):
        assert (self.foo.nin(['Hello', 'World'])) == {
            'foo': {'$nin': ['Hello', 'World']}
        }

        assert (self.Bar.baz.nin([10, 20, 30])) == {
            'baz': {'$nin': [10, 20, 30]}
        }

    def test_exists(self):
        assert (self.foo.exists()) == {
            'foo': {'$exists': True}
        }

        assert (self.Bar.baz.exists(False)) == {
            'baz': {'$exists': False}
        }

    def test_exists(self):
        assert (self.foo.exists()) == {
            'foo': {'$exists': True}
        }

        assert (self.Bar.baz.exists(False)) == {
            'baz': {'$exists': False}
        }

    def test_type(self):
        assert (self.foo.type(str)) == {
            'foo': {'$type': 2}
        }

        assert (self.Bar.baz.type(int)) == {
            'baz': {'$type': 16}
        }

        assert (self.foo.type(None)) == {
            'foo': {'$type': 10}
        }

        assert (self.Bar.baz.type(float)) == {
            'baz': {'$type': 1}
        }

    


class TestLogicalExpressions(unittest.TestCase):

    def setUp(self):
        foo = Field('foo')
        self.a = foo == 'A'
        self.b = foo == 'B'
        self.c = foo == 'C'
        self.d = foo == 'D'

        self.anb = self.a & self.b
        self.aob = self.a | self.b

        self.cnd = self.c & self.d
        self.cod = self.c | self.d

    def test_logical_and(self):
        assert self.anb == --self.anb == {
            '$and': [
                {'foo': {'$eq': 'A'}}, 
                {'foo': {'$eq': 'B'}}
            ]
        }

    def test_logical_or(self):
        assert self.aob == --self.aob == {
            '$or': [
                {'foo': {'$eq': 'A'}}, 
                {'foo': {'$eq': 'B'}}
            ]
        }

    def test_many_logical_ands(self):
        assert self.anb & self.cnd == --(self.anb & self.cnd) == {
            '$and': [
                {'foo': {'$eq': 'A'}}, 
                {'foo': {'$eq': 'B'}},
                {'foo': {'$eq': 'C'}}, 
                {'foo': {'$eq': 'D'}}
            ]
        }

    def test_two_logical_ands_with_or(self):
        assert self.anb | self.cnd == --(self.anb | self.cnd) =={
            '$or': [
                {'$and': [
                    {'foo': {'$eq': 'A'}}, 
                    {'foo': {'$eq': 'B'}}
            ]}, 
                {'$and': [
                    {'foo': {'$eq': 'C'}}, 
                    {'foo': {'$eq': 'D'}}
                ]}
            ]
        }

    def test_many_logical_ors(self):
        assert self.aob | self.cod == --(self.aob | self.cod ) == {
            '$or': [
                {'foo': {'$eq': 'A'}}, 
                {'foo': {'$eq': 'B'}},
                {'foo': {'$eq': 'C'}}, 
                {'foo': {'$eq': 'D'}}
            ]
        }

    def test_two_logical_ors_with_and(self):
        assert self.aob & self.cod == --(self.aob & self.cod ) == {
            '$and': [
                {'$or': [
                    {'foo': {'$eq': 'A'}}, 
                    {'foo': {'$eq': 'B'}}
            ]}, 
                {'$or': [
                    {'foo': {'$eq': 'C'}}, 
                    {'foo': {'$eq': 'D'}}
                ]}
            ]
        }


if __name__ == '__main__':
    unittest.main()
