from dataclasses import asdict, fields, is_dataclass
from typing import Type

from bson import ObjectId
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorCollection

from mongoext.exceptions import MissingIdException
from mongoext.fields import Field


id_field = Field('_id')


class CollectionExt(Collection):

    def get(self, id):
        query = id_field == ObjectId(id)
        return self.find_one(query)

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

    def save_document(self, document):
        """
            If the document's '_id' field is set to a value that 
                evaluates to True, then execute an UPDATE.
            If the document's '_id' field is not set or if the UPDATE
                didn’t update anything then execute an INSERT.
        """
        has_id = bool(document.get('_id'))
        if has_id:
            result = self.update_document(document)
            if result.matched_count == 1:
                return result
        return self.insert_document(document)

    def delete_document(self, document):
        if '_id' not in document:
            raise MissingIdException("Cannot delete a document that does not have an '_id' field.")        
        return self.delete_by_id(document['_id'])

    def insert_dataclass(self, dc):
        if not is_dataclass(dc):
            raise TypeError

        if '_id' not in (f.name for f in fields(dc)):
            raise TypeError
        
        return self.insert_document(asdict(dc))

    def update_dataclass(self, dc):
        if not is_dataclass(dc):
            raise TypeError

        if '_id' not in (f.name for f in fields(dc)):
            raise TypeError

        return self.update_document(asdict(dc))

    def delete_dataclass(self, dc):
        if not is_dataclass(dc):
            raise TypeError
        
        if '_id' not in (f.name for f in fields(dc)):
            raise TypeError
        
        return self.delete_document(asdict(dc))

    def insert_object(self, obj):
        ...

    def update_object(self, obj):
        ...

    def delete_object(self, obj):
        ...

    def delete_by_id(self, id):
        query = id_field == ObjectId(id)
        return self.delete_one(filter=query)


class AsyncCollectionExt(AsyncIOMotorCollection):

    async def get(self, id):
        query = id_field == ObjectId(id)
        return await self.find_one(query)

    async def insert(self, document):
        return await self.insert_one(document)

    async def update(self, document):
        if '_id' not in document:
            raise MissingIdException("Cannot update a document that does not have an '_id' field.")
        
        query = id_field == document['_id']
        return await self.update_one(
            filter=query,
            update={'$set': document}
        )

    async def save(self, document):
        """
            If the document's '_id' field is set to a value that 
                evaluates to True, then execute an UPDATE.
            If the document's '_id' field is not set or if the UPDATE
                didn’t match anything then execute an INSERT.
        """
        has_id = bool(document.get('_id'))
        if has_id:
            result = await self.update(document)
            if result.matched_count == 1:
                return result
        return await self.insert(document)

    async def delete(self, document):
        if '_id' not in document:
            raise MissingIdException("Cannot delete a document that does not have an '_id' field.")
        
        query = id_field == document['_id']
        return await self.delete_one(filter=query)
