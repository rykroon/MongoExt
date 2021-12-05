from contextlib import contextmanager


class CursorExt:
    def __init__(self, cursor, hook, cache=False):
        self.cursor = cursor
        if not callable(hook):
            raise TypeError
        self.hook = hook
        self.cache = cache
        # add caching logic

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.cursor)
        return self.hook(document)

@contextmanager
def use_db(db_name, client):
    yield client[db_name]


@contextmanager
def use_collection(collection_name, db):
    yield db[collection_name]