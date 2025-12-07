import uuid
from decimal import Decimal


from sqlmodel import Field, SQLModel, Session, create_engine, or_, select, and_
from fastapi import Depends

from app.custom_objects.book import Book

from app.db_models.tables.helpers import returnAuthorObj, returnBookObj, returnGenreObj, returnNarratorObj, returnSeriesObj


from app.services.sqlite import SQLiteService
from app.services.task_manager import BackgroundTaskManagerService

# setup global services
db_service = None
background_manager = None

def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service

def get_background_manager() -> BackgroundTaskManagerService:
    """Get the background task manager instance."""
    global background_manager
    if background_manager is None:
        background_manager = BackgroundTaskManagerService()
    return background_manager


# service: SQLiteService = Depends(get_db_service)


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
    audibleOverallAvgRating: Decimal | None = Field(
        default=0, max_digits=3, decimal_places=2
    )
    audiblePerformanceAvgRating: Decimal | None = Field(
        default=0, max_digits=3, decimal_places=2
    )
    audibleStoryAvgRating: Decimal | None = Field(
        default=0, max_digits=3, decimal_places=2
    )
    lengthMinutes: float | None
    isAudiobook: bool = Field(default=True)


def addBook(book: Book, service: SQLiteService = Depends(get_db_service)) -> str:
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
        isAudiobook=book.isAudiobook,
    )

    with Session(service.engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id


def getBook(search_string, service: SQLiteService = Depends(get_db_service)) -> Book:
    """Get book from db"""
    with Session(service.engine) as session:
        statement = select(BooksTable).where(
            or_(
                BooksTable.title == search_string,
                BooksTable.bookAsin == search_string,
                BooksTable.id == search_string,
            )
        )

        results = session.exec(statement).first()
        if results:
            return returnBookObj(results, service)
        return None


def updateBook(book: Book, service: SQLiteService = Depends(get_db_service)) -> str:
    """Update book in db"""
    from bs4 import BeautifulSoup

    # strip html tags from desciption strings.
    if book.description:
        bs_description = BeautifulSoup(book.description, "html.parser")
        clean_description = bs_description.get_text()
    else:
        clean_description = "No desciption available."

    print(f"Updating book: {book.title}")
    with Session(service.engine) as session:
        statement = select(BooksTable).where(BooksTable.id == book.id)
        results = session.exec(statement).one()

        results.title = book.title
        results.subtitle = book.subtitle
        results.publisher = book.publisher
        results.copyright = book.copyright
        results.description = clean_description
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


def deleteBook(search_string, service: SQLiteService = Depends(get_db_service)) -> None:
    """Delete book from db by book asin or id"""
    with Session(service.engine) as session:
        statement = select(BooksTable).where(
            or_(BooksTable.bookAsin == search_string, BooksTable.id == search_string)
        )
        results = session.exec(statement).one()
        session.delete(results)


def doesBookExist(search_string, service: SQLiteService = Depends(get_db_service)):
    with Session(service.engine) as session:
        statement = select(BooksTable).where(
            or_(
                BooksTable.title == search_string,
                BooksTable.bookAsin == search_string,
                BooksTable.id == search_string,
            )
        )

        results = session.exec(statement)
        if len(results.all()) > 0:
            return True
        else:
            return False


def getAllBooks(service: SQLiteService = Depends(get_db_service)) -> list:
    with Session(service.engine) as session:
        statement = select(BooksTable).order_by(BooksTable.title)
        results = session.exec(statement).all()

        if results:
            all_books = []
            for item in results:
                book = returnBookObj(item, service)
                all_books.append(book)

            return all_books
        return None


def getBooksToBeReleased(time_window, service: SQLiteService = Depends(get_db_service)) -> list:
    from datetime import datetime

    current_date = datetime.now().strftime("%Y-%m-%d")
    with Session(service.engine) as session:
        statement = (
            select(BooksTable)
            .where(BooksTable.releaseDate > current_date)
            .order_by(BooksTable.releaseDate.asc())
            .limit(time_window)
        )
        results = session.exec(statement)

        if results:
            all_books = []
            for item in results:
                book = returnBookObj(item, service)
                all_books.append(book)

            return all_books
        return None


