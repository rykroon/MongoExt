from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from mongoext.exceptions import MissingIdException
from mongoext.fields import Field


id_field = Field('_id')


class AsyncCollectionExt(AsyncIOMotorCollection):

    async def get_by_id(self, id):
        query = id_field == ObjectId(id)
        return await self.find_one(query)

    async def delete_by_id(self, id):
        ...

    async def insert_document(self, document):
        return await self.insert_one(document)

    async def update_document(self, document):
        if '_id' not in document:
            raise MissingIdException("Cannot update a document that does not have an '_id' field.")
        
        query = id_field == document['_id']
        return await self.update_one(
            filter=query,
            update={'$set': document}
        )

    async def delete_document(self, document):
        if '_id' not in document:
            raise MissingIdException("Cannot delete a document that does not have an '_id' field.")
        
        query = id_field == document['_id']
        return await self.delete_one(filter=query)
