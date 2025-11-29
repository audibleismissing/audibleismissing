from app.custom_objects.author import Author
from app.custom_objects.book import Book
from app.custom_objects.genre import Genre
from app.custom_objects.narrator import Narrator
from app.custom_objects.series import Series


def returnAuthorObj(api_author:dict) -> Author:
    author = Author()
    author.authorAsin = api_author.setdefault('asin', None)
    author.name = api_author.setdefault('name', None)
    return author


def returnNarratorObj(api_narrator) -> Narrator:
    narrator = Narrator()
    narrator.name = api_narrator.setdefault('name', None)
    return narrator


def returnGenreObj(api_genre) -> Genre:
    genre = Genre()
    genre.name = api_genre.setdefault('name', None)
    return genre


def returnSeriesObj(api_series) -> Series:
    series = Series()
    series.seriesAsin = api_series.setdefault('asin', None)
    series.name = api_series.setdefault('title', None)
    series.sequence = api_series.setdefault('position', None)
    return series


def returnBookObj(api_book:dict, isSeries:bool) -> Book:
    """
    Creates a book object from audimeta data
    """

    book = Book()

    # import json
    # print(json.dumps(api_book, indent=4))

    authors = []
    if api_book.get('authors'):
        for item in api_book.get('authors'):
            author = returnAuthorObj(item)
            authors.append(author)
    book.authors = authors

    narrators = []
    if api_book.get('narrators'):
        for item in api_book.get('narrators'):
            narrator = returnNarratorObj(item)
            narrators.append(narrator)
    book.narrators = narrators
    
    series = []
    if api_book.get('series'):
        for item in api_book.get('series'):
            single_series = returnSeriesObj(item)
            series.append(single_series)
    book.series = series
    
    book.title = api_book.setdefault('title', None)
    book.subtitle = api_book.setdefault('subtitle', None)

    genres = []
    if not isSeries:
        if api_book.get('genres'):
            for item in api_book.get('genres'):
                returnGenreObj(item)
    book.genres = set(genres)
    
    book.publisher = api_book.setdefault('publisher', None)
    book.copyright = api_book.setdefault('copyright', None)
    book.description = api_book.setdefault('description', None)
    book.summary = api_book.setdefault('summary', None)
    book.isbn = api_book.setdefault('isbn', None)
    book.bookAsin = api_book.setdefault('asin', None)
    book.region = 'us'
    book.language = api_book.setdefault('language', None)
    book.isExplicit = api_book.setdefault('explicit', None)

    if api_book('bookFormat') == 'unabridged':
        book.isAbridged = False
    else:
        book.isAbridged = True

    book.releaseDate = api_book.setdefault('releaseDate', None)
    # book.tags = api_book
    book.link = api_book.setdefault('link', None)
    book.imageUrl = api_book.setdefault('imageUrl', None)
    book.isOwned = False

    book.audibleOverallAvgRating = round(api_book.setdefault('rating', 0), 2)
    # book.audibleOverallAvgRating = round(api_book['rating']['overall_distribution'].setdefault('average_rating', None), 2)
    # book.audiblePerformanceAvgRating = round(api_book['rating']['performance_distribution'].setdefault('average_rating', None), 2)
    # book.audibleStoryAvgRating = round(api_book['rating']['story_distribution'].setdefault('average_rating', None), 2)
    
    book.lengthMinutes = api_book.setdefault('lengthMinutes', None)

    return book


def returnListofBookObjs(book_list: list) -> list:
    books = []
    for single_book in book_list:
        if single_book.get('series'):
            isSeries = True
        else:
            isSeries = False
        book = Book()
        book = returnBookObj(single_book, isSeries)
        books.append(book)
    return books