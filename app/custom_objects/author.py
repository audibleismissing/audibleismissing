class Author:
    def __init__(self):
        self.id = None
        self.name = None
        self.authorAsin = None

    def __iter__(self):
        for series in self.name:
            yield series

    def serialize(self):
        """Serialize the Author object to a dictionary."""
        return {"id": self.id, "name": self.name, "authorAsin": self.authorAsin}
