from bson import ObjectId
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorCollection

from mongoext.fields import Field


id_field = Field('_id')


class CollectionExt(Collection):

    def get(self, id):
        query = id_field == ObjectId(id)
        return self.find_one(query)

    def insert(self, document):
        return self.insert_one(document)

    def update(self, document):
        query = id_field == document['_id']
        return self.update_one(
            filter=query,
            update={'$set': document}
        )

    def save(self, document):
        _id = document.get('_id')
        if _id is None:
            return self.insert(document)
        return self.update(document)

    def delete(self, document):
        query = id_field == document['_id']
        return self.delete_one(filter=query)


class AsyncCollectionExt(AsyncIOMotorCollection):

    async def get(self, id):
        query = id_field == ObjectId(id)
        return await self.find_one(query)

    async def insert(self, document):
        return await self.insert_one(document)

    async def update(self, document):
        query = id_field == document['_id']
        return await self.update_one(
            filter=query,
            update={'$set': document}
        )

    async def save(self, document):
        _id = document.get('_id')
        if _id is None:
            return await self.insert(document)
        return await self.update(document)

    async def delete(self, document):
        query = id_field == document['_id']
        return await self.delete_one(filter=query)
