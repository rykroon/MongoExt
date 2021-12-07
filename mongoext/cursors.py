

class DocumentIterator:
    def __init__(self, cursor, document_hook):
        self.cursor = cursor
        if not callable(document_hook):
            raise TypeError
        self.document_hook = document_hook

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.cursor)
        return self.document_hook(document)
