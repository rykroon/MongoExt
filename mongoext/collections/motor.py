from motor.motor_asyncio import AsyncIOMotorCollection

from mongoext.exceptions import MissingIdException
from mongoext.query import Field
from mongoext.collections.utils import check_object, check_dataclass, \
    dataclass_to_dict, object_to_dict


id_field = Field('_id')


class AsyncCollectionExt(AsyncIOMotorCollection):

    async def get_by_id(self, id):
        query = id_field == id
        return await self.find_one(query)

    async def delete_by_id(self, id):
        query = id_field == id
        return await self.delete_one(filter=query)

    async def insert_document(self, document):
        if '_id' in document and bool(document['_id']) is False:
            del document['_id']
        return await self.insert_one(document)

    async def update_document(self, document):
        if '_id' not in document:
            raise MissingIdException(
                "Cannot update a document that does not have an '_id' field."
            )

        query = id_field == document['_id']
        return await self.update_one(
            filter=query,
            update={'$set': document}
        )

    async def delete_document(self, document):
        if '_id' not in document:
            raise MissingIdException(
                "Cannot delete a document that does not have an '_id' field."
            )
        return await self.delete_by_id(document['_id'])

    def insert_object(self, obj):
        check_object(obj)
        document = object_to_dict(obj)
        result = self.insert_document(document)
        setattr(obj, '_id', result.inserted_id)
        return result

    async def update_object(self, obj):
        check_object(obj)
        if not hasattr(obj, '_id'):
            raise MissingIdException(
                "Cannot update an object that does not have an '_id' attribute."
            )
        document = object_to_dict(obj)
        return await self.update_document(document)

    async def delete_object(self, obj):
        check_object(obj)
        if not hasattr(obj, '_id'):
            raise MissingIdException(
                "Cannot delete an object that does not have an '_id' attribute."
            )
        return await self.delete_by_id(obj._id)

    async def insert_dataclass(self, obj):
        check_dataclass(obj)
        document = dataclass_to_dict(obj)
        result = await self.insert_document(document)
        setattr(obj, '_id', result.inserted_id)
        return result

    async def update_dataclass(self, obj):
        check_dataclass(obj)
        document = await dataclass_to_dict(obj)
        return self.update_document(document)

    async def delete_dataclass(self, obj):
        check_dataclass(obj)
        return await self.delete_by_id(obj._id)
