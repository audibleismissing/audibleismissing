import uuid
from decimal import Decimal


from sqlmodel import Field, SQLModel, Session, create_engine, or_, select, and_

from app.custom_objects.book import Book

from app.db_models.tables.authors import getBookAuthors
from app.db_models.tables.genres import getBookGenres
# avoid circular import by importing series helper inside functions where needed
from app.db_models.tables.narrators import getBookNarrators



class BooksTable(SQLModel, table=True):
    __tablename__ = "books"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str | None = Field(index=True)
    subtitle: str | None
    publisher: str | None
    copyright: str | None
    description: str | None
    summary: str | None
    isbn: str | None
    bookAsin: str | None = Field(index=True)
    region: str | None
    language: str | None
    isExplicit: bool | None
    isAbridged: bool | None
    releaseDate: str | None
    link: str | None
    imageUrl: str | None
    isOwned: bool = Field(default=True)
    audibleOverallAvgRating: Decimal | None = Field(default=0, max_digits=3, decimal_places=2)
    audiblePerformanceAvgRating: Decimal | None = Field(default=0, max_digits=3, decimal_places=2)
    audibleStoryAvgRating: Decimal | None = Field(default=0, max_digits=3, decimal_places=2)
    lengthMinutes: float | None
    isAudiobook: bool = Field(default=True)


def addBook(engine, book:Book) -> str:
    """Add book to db"""
    from bs4 import BeautifulSoup
    print(f"Adding book: {book.title}")

    # strip html tags from desciption strings.
    if book.description:
        bs_description = BeautifulSoup(book.description, "html.parser")
        clean_description = bs_description.get_text()
    else:
        clean_description = "No desciption available."

    row = BooksTable(
        title=book.title,
        subtitle=book.subtitle,
        publisher=book.publisher,
        copyright=book.copyright,
        description=clean_description,
        summary=book.summary,
        isbn=book.isbn,
        bookAsin=book.bookAsin,
        region=book.region,
        language=book.language,
        isExplicit=book.isExplicit,
        isAbridged=book.isAbridged,
        releaseDate=book.releaseDate,
        link=book.link,
        imageUrl=book.imageUrl,
        isOwned=book.isOwned,
        audibleOverallAvgRating=book.audibleOverallAvgRating,
        audiblePerformanceAvgRating=book.audiblePerformanceAvgRating,
        audibleStoryAvgRating=book.audibleStoryAvgRating,
        lengthMinutes=book.lengthMinutes,
        isAudiobook=book.isAudiobook
    )

    with Session(engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id


def getBook(engine:create_engine, search_string) -> Book:
    """Get book from db"""
    with Session(engine) as session:
        statement = select(BooksTable).where(or_(BooksTable.title == search_string, BooksTable.bookAsin == search_string, BooksTable.id == search_string))

        results = session.exec(statement).first()
        if results:
            return returnBookObj(engine, results)
        return None
    

def updateBook(engine: create_engine, book: Book) -> str:
    """Update book in db"""
    print(f"Updating book: {book.title}")
    with Session(engine) as session:
        statement = select(BooksTable).where(BooksTable.id == book.id)
        results = session.exec(statement).one()

        results.title = book.title
        results.subtitle = book.subtitle
        results.publisher = book.publisher
        results.copyright = book.copyright
        results.description = book.description
        results.summary = book.summary
        results.isbn = book.isbn
        results.bookAsin = book.bookAsin
        results.region = book.region
        results.language = book.language
        results.isExplicit = book.isExplicit
        results.isAbridged = book.isAbridged
        results.releaseDate = book.releaseDate
        results.link = book.link
        results.imageUrl = book.imageUrl
        results.isOwned = book.isOwned
        results.audibleOverallAvgRating = book.audibleOverallAvgRating
        results.audiblePerformanceAvgRating = book.audiblePerformanceAvgRating
        results.audibleStoryAvgRating = book.audibleStoryAvgRating
        results.lengthMinutes = book.lengthMinutes
        results.isAudiobook = book.isAudiobook

        session.add(results)
        session.commit()
        session.refresh(results)
        return results.id


def deleteBook(engine: create_engine, search_string) -> None:
    """Delete book from db by book asin or id"""
    with Session(engine) as session:
        statement = select(BooksTable).where(or_(BooksTable.bookAsin == search_string, BooksTable.id == search_string))
        results = session.exec(statement).one()
        session.delete(results)


def doesBookExist(engine, search_string):
    with Session(engine) as session:
        statement = select(BooksTable).where(or_(BooksTable.title == search_string, BooksTable.bookAsin == search_string, BooksTable.id == search_string))
            
        results = session.exec(statement)
        if len(results.all()) > 0:
            return True
        else:
            return False


def getAllBooks(engine) -> list:
    with Session(engine) as session:
        statement = select(BooksTable).order_by(BooksTable.title)
        results = session.exec(statement).all()
        
        if results:
            all_books = []
            for item in results:
                book = returnBookObj(engine, item)
                all_books.append(book)

            return all_books
        return None
    

def getBooksToBeReleased(engine, time_window) -> list:
    from datetime import datetime
    current_date = datetime.now().strftime('%Y-%m-%d')
    with Session(engine) as session:
        statement = select(BooksTable).where(BooksTable.releaseDate > current_date).order_by(BooksTable.releaseDate.asc()).limit(time_window)
        results = session.exec(statement)

        if results:
            all_books = []
            for item in results:
                book = returnBookObj(engine, item)
                all_books.append(book)

            return all_books
        return None


def returnBookObj(engine, book_table) -> Book:
    """Convert a BooksTable object to a Book object"""
    book = Book()

    # Map the fields from BooksTable to Book
    book.id = book_table.id
    book.title = book_table.title
    book.subtitle = book_table.subtitle
    book.publisher = book_table.publisher
    book.copyright = book_table.copyright
    book.description = book_table.description
    book.summary = book_table.summary
    book.isbn = book_table.isbn
    book.bookAsin = book_table.bookAsin
    book.region = book_table.region
    book.language = book_table.language
    book.isExplicit = book_table.isExplicit
    book.isAbridged = book_table.isAbridged
    book.releaseDate = book_table.releaseDate
    book.link = book_table.link
    book.imageUrl = book_table.imageUrl
    book.isOwned = book_table.isOwned
    book.audibleOverallAvgRating = book_table.audibleOverallAvgRating
    book.audiblePerformanceAvgRating = book_table.audiblePerformanceAvgRating
    book.audibleStoryAvgRating = book_table.audibleStoryAvgRating
    book.lengthMinutes = book_table.lengthMinutes
    book.isAudiobook = book_table.isAudiobook
    
    book.authors = getBookAuthors(engine, book_table.id)
    book.genres = getBookGenres(engine, book_table.id)
    # import here to avoid circular import at module import time
    from app.db_models.tables.series import getBookSeries
    book.series = getBookSeries(engine, book_table.id)
    book.narrators = getBookNarrators(engine, book_table.id)
    
    return book