

class DocumentIterator:
    def __init__(self, cursor, document_hook):
        self.cursor = cursor
        if not callable(document_hook):
            raise TypeError
        self.document_hook = document_hook
        self.cache = []

    def __iter__(self):
        if self.cache:
            return self.cache
        return self

    def __next__(self):
        document = next(self.cursor)
        result = self.document_hook(document)
        self.cache.append(result)
        return result
