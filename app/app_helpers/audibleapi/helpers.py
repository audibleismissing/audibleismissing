from app.custom_objects.author import Author
from app.custom_objects.book import Book
from app.custom_objects.genre import Genre
from app.custom_objects.narrator import Narrator
from app.custom_objects.series import Series


def returnAuthorObj(api_author:dict) -> Author:
    author = Author()
    author.authorAsin = api_author.setdefault('authorAsin', None)
    author.name = api_author.setdefault('name', None)
    return author


def returnNarratorObj(api_narrator) -> Narrator:
    narrator = Narrator()
    narrator.name = api_narrator.setdefault('name', None)
    return narrator


def returnGenreObj(api_genre) -> Genre:
    genre = Genre()
    genre.name = api_genre
    return genre


def returnSeriesObj(api_series) -> Series:
    series = Series()
    series.seriesAsin = api_series.setdefault('asin', None)
    series.name = api_series.setdefault('title', None)
    series.sequence = api_series.setdefault('sequence', None)
    # series.totalBooksInSeries = None
    # series.totalBooksInLibrary = None
    return series


def returnBookObj(api_book:dict, isSeries:bool) -> Book:
    """
    Creates a Book object by extracting and mapping data from an API response dictionary.

    Parameters:
        api_book (dict): Dictionary containing raw book data from the API.
        isSeries (bool): Flag indicating if the book is part of a series to determine genre handling.

    Returns:
        Book: A fully populated Book object with authors, narrators, metadata, and ratings.

    Raises:
        KeyError: If required keys are missing in the api_book or nested dictionaries.
        TypeError: If api_book isn't a dictionary or contains unexpected data types.
    """
    book = Book()
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
        if api_book.get('category_ladders'):
            for ladder in api_book.get('category_ladders'):
                for item in ladder.get('ladder'):
                    returnGenreObj(ladder)
    book.genres = set(genres)
    
    book.publisher = api_book.setdefault('publisher_name', None)
    book.copyright = api_book.setdefault('copyright', None)
    book.description = api_book.setdefault('extended_product_description', None)
    # book.summary = api_book
    book.isbn = api_book.setdefault('isbn', None)
    book.bookAsin = api_book.setdefault('asin', None)
    book.region = 'us'
    # book.language = api_book
    # book.isExplicit = api_book
    # book.isAbridged = api_book
    book.releaseDate = api_book.setdefault('date_first_available', None)
    # book.tags = api_book
    # book.link = api_book
    # book.imageUrl = api_book
    book.isOwned = False
    book.audibleOverallAvgRating = api_book['rating']['overall_distribution'].setdefault('average_rating', None)
    book.audiblePerformanceAvgRating = api_book['rating']['performance_distribution'].setdefault('average_rating', None)
    book.audibleStoryAvgRating = api_book['rating']['story_distribution'].setdefault('average_rating', None)
    # book.lengthMinutes = api_book

    return book


def returnListofBookObjs(book_list: list) -> list:
    books = []
    for single_book in book_list['similar_products']:
        if single_book.get('series'):
            isSeries = True
        else:
            isSeries = False
        book = Book()
        book = returnBookObj(single_book, isSeries)
        books.append(book)
    return books