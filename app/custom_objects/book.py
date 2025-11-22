class Book:
    def __init__(self):
        self.id: str = None
        self.title: str = None
        self.subtitle: str = None
        self.authors = []
        self.publisher: str = None
        self.copyright: str = None
        self.description: str = None
        self.summary: str = None
        self.isbn: str = None
        self.bookAsin: str = None
        self.region: str = None
        self.language: str = None
        self.isExplicit: str = None
        self.isAbridged: str = None
        self.releaseDate: str = None
        # self.launchDate: str = None # amazon product_site_launch_date
        self.genres = []
        self.link: str = None
        self.imageUrl: str = None
        self.series = []
        self.isOwned: str = None
        self.audibleOverallAvgRating: str = None
        self.audiblePerformanceAvgRating: str = None
        self.audibleStoryAvgRating: str = None
        self.narrators = []
        self.lengthMinutes: str = None
        self.isAudiobook = True

    def __iter__(self):
        for book in self.title:
            yield book
    
    def __dict__(self):
        return self.serialize()

    def serialize(self):
        """Serialize the Book object to a dictionary."""
        series = []
        authors = []
        genre = []
        narrators = []
        for item in self.series:
            series.append(item.serialize())
        for item in self.authors:
            series.append(item.serialize())
        for item in self.genre:
            series.append(item.serialize())
        for item in self.narrators:
            series.append(item.serialize())
            
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            'authors': authors,
            "publisher": self.publisher,
            "copyright": self.copyright,
            "description": self.description,
            "summary": self.summary,
            "isbn": self.isbn,
            "bookAsin": self.bookAsin,
            "region": self.region,
            "language": self.language,
            "isExplicit": self.isExplicit,
            "isAbridged": self.isAbridged,
            "releaseDate": self.releaseDate,
            'genres': genre,
            "link": self.link,
            "imageUrl": self.imageUrl,
            "series": series,
            "isOwned": self.isOwned,
            "audibleOverallAvgRating": self.audibleOverallAvgRating,
            "audiblePerformanceAvgRating": self.audiblePerformanceAvgRating,
            "audibleStoryAvgRating": self.audibleStoryAvgRating,
            'narrators': narrators,
            "lengthMinutes": self.lengthMinutes,
            "isAudiobook": self.isAudiobook,
        }
