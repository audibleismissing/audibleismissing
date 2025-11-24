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
        series_list = []
        authors_list = []
        genres_list = []
        narrators_list = []
        for item in self.series:
            series_list.append(item.serialize())
        for item in self.authors:
            authors_list.append(item.serialize())
        for item in self.genres:
            genres_list.append(item.serialize())
        for item in self.narrators:
            narrators_list.append(item.serialize())

        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            'authors': authors_list,
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
            'genres': genres_list,
            "link": self.link,
            "imageUrl": self.imageUrl,
            "series": series_list,
            "isOwned": self.isOwned,
            "audibleOverallAvgRating": self.audibleOverallAvgRating,
            "audiblePerformanceAvgRating": self.audiblePerformanceAvgRating,
            "audibleStoryAvgRating": self.audibleStoryAvgRating,
            'narrators': narrators_list,
            "lengthMinutes": self.lengthMinutes,
            "isAudiobook": self.isAudiobook,
        }

def jsonToBook(data) -> Book:
    book = Book()
    book.title = data['title']
    book.subtitle = data['subtitle']
    book.authors = []
    book.publisher = data['publisher']
    book.copyright = data['copyright']
    book.description = data['description']
    book.summary = data['summary']
    book.isbn = data['isbn']
    book.bookAsin = data['bookAsin']
    book.region = data['region']
    book.language = data['language']
    book.isExplicit = data['isExplicit']
    book.isAbridged = data['isAbridged']
    book.releaseDate = data['releaseDate']
    book.genres = []
    book.link = data['link']
    book.imageUrl = data['imageUrl']
    book.series = []
    book.isOwned = data['isOwned']
    book.audibleOverallAvgRating = data['audibleOverallAvgRating']
    book.audiblePerformanceAvgRating = data['audiblePerformanceAvgRating']
    book.audibleStoryAvgRating = data['audibleStoryAvgRating']
    book.narrators = []
    book.lengthMinutes = data['lengthMinutes']
    book.isAudiobook = True
    return book