class Narrator:
    def __init__(self):
        self.id = None
        self.name = None

    def __iter__(self):
        for series in self.name:
            yield series

    def serialize(self):
        """Serialize the Narrator object to a dictionary."""
        return {"id": self.id, "name": self.name}
