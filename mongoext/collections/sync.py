from bson import ObjectId
from pymongo.collection import Collection

from mongoext.exceptions import MissingIdException
from mongoext.fields import Field
from mongoext.collections.utils import check_dataclass, check_object, dataclass_to_dict, object_to_dict


id_field = Field('_id')


class CollectionExt(Collection):

    def get_by_id(self, id):
        query = id_field == id
        return self.find_one(query)

    def delete_by_id(self, id):
        query = id_field == id
        return self.delete_one(filter=query)

    def insert_document(self, document):
        if '_id' in document and bool(document['_id']) == False:
            del document['_id']
        return self.insert_one(document)

    def update_document(self, document):
        if '_id' not in document:
            raise MissingIdException("Cannot update a document that does not have an '_id' field.")
        
        query = id_field == document['_id']
        return self.update_one(
            filter=query,
            update={'$set': document}
        )

    def delete_document(self, document):
        if '_id' not in document:
            raise MissingIdException("Cannot delete a document that does not have an '_id' field.")
        return self.delete_by_id(document['_id'])

    def insert_object(self, obj):
        check_object(obj)
        document = object_to_dict(obj)
        result = self.insert_document(document)
        setattr(obj, '_id', result.inserted_id)
        return result

    def update_object(self, obj):
        check_object(obj)
        if not hasattr(obj, '_id'):
            raise MissingIdException("Cannot update an object that does not have an '_id' attribute.")
        document = object_to_dict(obj)
        return self.update_document(document)

    def delete_object(self, obj):
        check_object(obj)
        if not hasattr(obj, '_id'):
            raise MissingIdException("Cannot delete an object that does not have an '_id' attribute.")
        return self.delete_by_id(obj._id)

    def insert_dataclass(self, obj):
        check_dataclass(obj)
        document = dataclass_to_dict(obj)
        result = self.insert_document(document)
        setattr(obj, '_id', result.inserted_id)
        return result

    def update_dataclass(self, obj):
        check_dataclass(obj)
        document = dataclass_to_dict(obj)
        return self.update_document(document)

    def delete_dataclass(self, obj):
        check_dataclass(obj)
        return self.delete_by_id(obj._id)
