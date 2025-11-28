class SeriesWatchListItem:
    def __init__(self):
        self.id = None
        self.seriesId = None

    def __iter__(self):
        for series in self.name:
            yield series

    def serialize(self):
        """Serialize the Series object to a dictionary."""
        return {
            "id": self.id,
            "seriesId": self.seriesId,
        }
