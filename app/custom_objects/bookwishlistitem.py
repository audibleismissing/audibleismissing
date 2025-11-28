class BookWishListItem:
    def __init__(self):
        self.id = None
        self.bookId = None

    def __iter__(self):
        for book in self.name:
            yield book

    def serialize(self):
        """Serialize the Series object to a dictionary."""
        return {
            "id": self.id,
            "bookId": self.bookId,
        }
