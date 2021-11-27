

def find(collection, *args, **kwargs):
    return collection.find(*args, **kwargs)


def insert(collection, document):
    return collection.insert_one(document)


def update(collection, document):
    return collection.update_one(
        filter={'_id': document['_id']},
        update={'$set': document}
    )


def save(collection, document):
    _id = document.get('_id')
    if _id is None:
        return insert(collection, document)
    return update(collection, document)


def delete(collection, document):
    return collection.delete_one(
        filter={'_id': document['_id']}
    )
