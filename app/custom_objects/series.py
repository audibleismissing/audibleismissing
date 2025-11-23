class Series:
    def __init__(self):
        self.id = None
        self.name = None
        self.seriesAsin = None
        self.sequence = None
        self.totalBooksInSeries = None
        self.totalBooksInLibrary = None

    def __iter__(self):
        for series in self.name:
            yield series

    def serialize(self):
        """Serialize the Series object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "seriesAsin": self.seriesAsin,
            "sequence": self.sequence,
            "totalBooksInSeries": self.totalBooksInSeries,
            "totalBooksInLibrary": self.totalBooksInLibrary,
        }


def jsonToSeries(data) -> Series:
    series = Series()
    series.name = data['name']
    series.seriesAsin = data['seriesAsin']
    series.sequence = data['sequence']
    series.totalBooksInSeries = data['totalBooksInSeries']
    series.totalBooksInLibrary = data['totalBooksInLibrary']
    return series