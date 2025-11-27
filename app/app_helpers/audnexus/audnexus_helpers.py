from datetime import datetime

from app.custom_objects.author import Author
from app.custom_objects.book import Book
from app.custom_objects.genre import Genre
from app.custom_objects.narrator import Narrator
from app.custom_objects.series import Series
from decimal import Decimal


def returnAuthorObj(api_author: dict) -> Author:
    author = Author()
    author.authorAsin = api_author.get('asin')
    author.name = api_author.get('name')
    return author


def returnNarratorObj(api_narrator: dict) -> Narrator:
    narrator = Narrator()
    narrator.name = api_narrator.get('name')
    return narrator


def returnGenreObj(api_genre: dict) -> Genre:
    genre = Genre()
    genre.name = api_genre.get('name')
    return genre


def returnSeriesObj(api_series: dict) -> Series:
    series = Series()
    series.seriesAsin = api_series.get('asin')
    series.name = api_series.get('name')
    series.sequence = api_series.get('position')
    return series


def returnBookObj(api_book: dict) -> Book:
    """
    Creates a Book object from audnexus data
    """
    book = Book()

    # Authors
    authors = []
    if api_book.get('authors'):
        for item in api_book['authors']:
            author = returnAuthorObj(item)
            authors.append(author)
    book.authors = authors

    # Narrators
    narrators = []
    if api_book.get('narrators'):
        for item in api_book['narrators']:
            narrator = returnNarratorObj(item)
            narrators.append(narrator)
    book.narrators = narrators

    # Genres
    genres = []
    if api_book.get('genres'):
        for item in api_book['genres']:
            genre = returnGenreObj(item)
            genres.append(genre)
    book.genres = genres

    # Series
    series = []
    if api_book.get('seriesPrimary'):
        single_series = returnSeriesObj(api_book['seriesPrimary'])
        series.append(single_series)
    book.series = series

    # Basic fields
    book.title = api_book.get('title')
    book.subtitle = api_book.get('subtitle')
    book.publisher = api_book.get('publisherName')
    book.copyright = api_book.get('copyright')
    book.description = api_book.get('description')
    book.summary = api_book.get('summary')
    book.isbn = api_book.get('isbn')
    book.bookAsin = api_book.get('asin')
    book.region = api_book.get('region')
    book.language = api_book.get('language')

    # converts releaseDate string to simple yyyy-mm-dd
    iso_ts = api_book.get('releaseDate').replace('Z', '+00:00')
    dt = datetime.fromisoformat(iso_ts)   # accepts the offset
    date_only = dt.date()
    book.releaseDate = date_only

    book.imageUrl = api_book.get('image')

    # Ratings
    if api_book.get('rating'):
        try:
            book.audibleOverallAvgRating = Decimal(str(api_book['rating']))
        except:
            book.audibleOverallAvgRating = None

    # Length
    if api_book.get('runtimeLengthMin'):
        book.lengthMinutes = str(api_book['runtimeLengthMin'])

    # Explicit/Adult content
    book.isExplicit = api_book.get('isAdult', False)

    # Abridged
    if api_book.get('formatType') == 'unabridged':
        book.isAbridged = False
    else:
        book.isAbridged = True

    # Other defaults
    # book.isOwned = False
    book.isAudiobook = True

    return book