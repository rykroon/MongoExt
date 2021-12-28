import unittest

from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from mongoext.collections import CollectionExt
from mongoext.exceptions import MissingIdException


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