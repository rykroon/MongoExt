import unittest

from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from mongoext.collections import CollectionExt
from mongoext.exceptions import MissingIdException
from mongoext.fields import Field

"""
    Run 'coverage run -m unittest discover'
    Run 'coverage report -m'
"""


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


class TestCollectionExt(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient()
        self.db = self.client['test_db']
        self.db.drop_collection('test_mongoext')
        self.coll = CollectionExt(name='test_mongoext', database=self.db)
        
        self.doc = {'a': 1, 'b': 2, 'c': 3}
        self.coll.insert_one(self.doc)

    def test_get_by_id(self):
        result = self.coll.get_by_id(self.doc['_id'])
        assert result == self.doc

        obj_id = ObjectId()
        result = self.coll.get_by_id(obj_id)
        assert result is None

    def test_delete_by_id(self):
        result = self.coll.delete_by_id(self.doc['_id'])
        assert result.deleted_count == 1

        result = self.coll.delete_by_id(self.doc['_id'])
        assert result.deleted_count == 0

    def test_insert_document(self):
        with self.assertRaises(DuplicateKeyError):
            self.coll.insert_document(self.doc)

        doc = {'_id': None}
        self.coll.insert_document(doc)
        assert doc['_id'] is not None

        doc = {'_id': 123456}
        self.coll.insert_document(doc)
        assert doc['_id'] == 123456

    def test_update_document(self):
        self.doc['d'] = 4
        self.coll.update_document(self.doc)

        self.coll.get_by_id(self.doc['_id']) == self.doc

        with self.assertRaises(MissingIdException):
            doc_with_no_id = {}
            self.coll.update_document(doc_with_no_id)

    def test_delete_document(self):
        result = self.coll.delete_document(self.doc)
        assert result.deleted_count == 1

        assert self.coll.get_by_id(self.doc['_id']) is None

    def test_insert_object(self):
        class Foo:
            ...

        f = Foo()
        self.coll.insert_object(f)
        assert hasattr(f, '_id') == True
        assert f._id is not None

        assert self.coll.get_by_id(f._id)['_id'] == f._id

        with self.assertRaises(TypeError):
            self.coll.insert_object(5)

    def test_update_object(self):
        class Foo:
            ...

        f = Foo()
        f.name = 'Alice'
        self.coll.insert_object(f)
        f.name = 'Bob'
        self.coll.update_object(f)
        self.coll.get_by_id(f._id)['name'] == 'Bob'

        with self.assertRaises(TypeError):
            self.coll.update_object(5)

        with self.assertRaises(MissingIdException):
            self.coll.update_object(Foo())

    def test_delete_object(self):
        class Foo:
            ...

        f = Foo()
        self.coll.insert_object(f)
        result = self.coll.delete_object(f)
        assert result.deleted_count == 1
        assert self.coll.get_by_id(f._id) is None


if __name__ == '__main__':
    unittest.main()
