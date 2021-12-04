from contextlib import contextmanager


@contextmanager
def use_db(db_name, client):
    yield client[db_name]


@contextmanager
def use_collection(collection_name, db):
    yield db[collection_name]