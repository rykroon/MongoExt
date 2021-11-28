


async def insert(collection, document):
    return await collection.insert_one(document)


async def update(collection, document):
    return await collection.update_one(
        filter={'_id': document['_id']},
        update={'$set': document}
    )


async def save(collection, document):
    _id = document.get('_id')
    if _id is None:
        return await insert(collection, document)
    return await update(collection, document)


async def delete(collection, document):
    return await collection.delete_one(
        filter={'_id': document['_id']}
    )
