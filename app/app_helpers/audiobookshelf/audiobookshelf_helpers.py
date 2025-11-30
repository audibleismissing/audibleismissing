from typing import Dict

from app.custom_objects.author import Author
from app.custom_objects.book import Book
from app.custom_objects.genre import Genre
from app.custom_objects.narrator import Narrator
from app.custom_objects.series import Series


def returnBookObj(abs_book:Dict) -> Book:
    """Converts a dictionary representation of a book into a Book object.

    Parameters:
        abs_book (Dict): Dictionary containing book metadata with nested
                         structures for media, metadata, tags, and authors.

    Returns:
        Book: A Book object populated with extracted title, authors, genres,
              and other metadata from the input dictionary.
    """

    book = Book()
    book.title = abs_book['media']['metadata']['title']
    book.subtitle = abs_book['media']['metadata']['subtitle']
    book.publisher = abs_book['media']['metadata']['publisher']
    book.copyright = None
    book.description = abs_book['media']['metadata']['description']

    if len(abs_book['media']['metadata']['authors']) > 0:
        authors_list = []
        for single_author in abs_book['media']['metadata']['authors']:
            authors_list.append(returnAuthorObj(single_author))
        book.authors = authors_list
    else:
        book.authors = None
    
    book.isbn = abs_book['media']['metadata']['isbn']
    book.bookAsin = abs_book['media']['metadata']['asin']
    book.region = None
    book.language = abs_book['media']['metadata']['language']
    book.explicit = abs_book['media']['metadata']['explicit']
    book.abridged = abs_book['media']['metadata']['abridged']
    book.releaseDate = abs_book['media']['metadata']['publishedYear']
    
    if len(abs_book['media']['tags']) > 0:
        genres_list = []
        for single_genre in abs_book['media']['tags']:
            genres_list.append(returnGenreObj(single_genre))
        book.genres = genres_list
    else:
        book.narrators = None

    book.link = None
    book.imageUrl = None

    if len(abs_book['media']['metadata']['series']) > 0:
        series_list = []
        for single_series in abs_book['media']['metadata']['series']:
            series_list.append(returnSeriesObj(single_series))
        book.series = series_list
    else:
        book.series = None

    book.owned = True
    book.audibleOverallAvgRating = None
    book.audiblePerformanceAvgRating = None
    book.audibleStoryAvgRating = None

    if len(abs_book['media']['metadata']['narrators']) > 0:
        narrators_list = []
        for single_narrator in abs_book['media']['metadata']['narrators']:
            narrators_list.append(returnNarratorObj(single_narrator))
        book.narrators = narrators_list
    else:
        book.narrators = None

    book.lengthMinutes = None
    book.audiobook = True
    return book


def returnSeriesObj(abs_series:Dict) -> Series:
    """Converts a dictionary representation of a series into a Series object.

    Parameters:
        abs_series (Dict): Dictionary containing series data with 'name' and 'sequence' keys.

    Returns:
        Series: A Series object populated with series name and sequence number.
    """

    series = Series()
    series.name = abs_series['name']
    series.seriesAsin = None
    series.sequence = abs_series['sequence']
    return series


def returnGenreObj(abs_genre:Dict) -> Genre:
    """Creates a Genre object using the input dictionary.

    Parameters:
        abs_genre (Dict): Dictionary representing genre information.

    Returns:
        Genre: A Genre object with the input dictionary assigned as its name.
    """

    genre = Genre()
    # Handle the case where abs_genre might be a string or dict
    if isinstance(abs_genre, dict):
        genre.name = abs_genre.get('name', str(abs_genre))
    else:
        genre.name = str(abs_genre)
    return genre


def returnAuthorObj(abs_author:Dict) -> Author:
    """Converts a dictionary representation of an author into an Author object.

    Parameters:
        abs_author (Dict): Dictionary containing author data with 'name' key.

    Returns:
        Author: An Author object with populated name and null authorAsin.
    """

    author = Author()
    author.name = abs_author['name']
    author.authorAsin = None
    return author


def returnNarratorObj(abs_narrator:Dict) -> Narrator:
    """Creates a Narrator object using the input dictionary.

    Parameters:
        abs_narrator (Dict): Dictionary representing narrator information.

    Returns:
        Narrator: A Narrator object with the input dictionary assigned as its name.
    """
    
    narrator = Narrator()
    # Handle the case where abs_narrator might be a string or dict
    if isinstance(abs_narrator, dict):
        narrator.name = abs_narrator.get('name', str(abs_narrator))
    else:
        narrator.name = str(abs_narrator)
    return narrator