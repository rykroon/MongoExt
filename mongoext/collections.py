from bson import ObjectId


class CollectionManager:

    def __init__(self, collection):
        self.collection = collection

    def get(self, id):
        return self.collection.find_one({'_id': ObjectId(id)})

    def insert(self, document):
        return self.collection.insert_one(document)

    def update(self, document):
        return self.collection.update_one(
            filter={'_id': document['_id']},
            update={'$set': document}
        )

    def save(self, document):
        _id = document.get('_id')
        if _id is None:
            return self.insert(document)
        return self.update(document)

    def delete(self, document):
        return self.collection.delete_one(
            filter={'_id': document['_id']}
        )


class AsyncCollectionManager:

    def __init__(self, collection):
        self.collection = collection

    async def get(self, id):
        return await self.collection.find_one({'_id': ObjectId(id)})

    async def insert(self, document):
        return await self.collection.insert_one(document)

    async def update(self, document):
        return await self.collection.update_one(
            filter={'_id': document['_id']},
            update={'$set': document}
        )

    async def save(self, document):
        _id = document.get('_id')
        if _id is None:
            return await self.insert(document)
        return await self.update(document)

    async def delete(self, document):
        return await self.collection.delete_one(
            filter={'_id': document['_id']}
        )
