class Genre:
    def __init__(self):
        self.id = None
        self.name = None

    def __iter__(self):
        for series in self.name:
            yield series

    def serialize(self):
        """Serialize the Genre object to a dictionary."""
        return {"id": self.id, "name": self.name}


def jsonToGenre(data) -> Genre:
    genre = Genre()
    genre.name = data['name']
    return genre