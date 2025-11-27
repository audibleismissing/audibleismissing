from decimal import Decimal
import uuid

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select, func, and_, delete
from app.custom_objects.series import Series
from app.db_models.tables import books
from app.db_models.tables.seriesmappings import SeriesMappingsTable



class SeriesTable(SQLModel, table=True):
    __tablename__ = "series"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(index=True)
    seriesAsin: str | None = Field(index=True)
    rating: Decimal | None = Field(default=0, max_digits=3, decimal_places=2)



def addSeries(engine: create_engine, series: Series) -> str:
    """Add series to db"""
    print(f"Adding series: {series.name}")

    row = SeriesTable(
        name=series.name,
        seriesAsin=series.seriesAsin,
        rating=series.rating
    )

    with Session(engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)

        return row.id
    return None


def getSeries(engine: create_engine, search_string):
    """Get series from db"""
    with Session(engine) as session:
        statement = select(SeriesTable).where(
            or_(SeriesTable.name == search_string, SeriesTable.id == search_string)
        )

        results = session.exec(statement).first()
        if results:
            return returnSeriesObj(results)
        return None


def updateSeries(engine: create_engine, series: Series) -> str:
    """Update series in db"""
    print(f"Updating series: {series.name}")
    with Session(engine) as session:
        statement = select(SeriesTable).where(SeriesTable.id == series.id)
        results = session.exec(statement).one()

        results.name = series.name
        results.seriesAsin = series.seriesAsin
        results.rating = series.rating

        session.add(results)
        session.commit()
        return results.id


def deleteSeries(engine: create_engine, series_id):
    """Delete series from db"""
    print(f"Deleting series: {series_id}")
    with Session(engine) as session:
        statement = select(SeriesTable).where(SeriesTable.id == series_id)
        results = session.exec(statement)
        row = results.one()
        session.delete(row)


def doesSeriesExist(engine: create_engine, search_string) -> bool:
    with Session(engine) as session:
        statement = select(SeriesTable).where(
            or_(SeriesTable.name == search_string, SeriesTable.id == search_string)
        )

        results = session.exec(statement)
        if len(results.all()) > 0:
            return True
        else:
            return False


def getBookSeries(engine: create_engine, book_id) -> list:
    """Get series object by book id"""
    with Session(engine) as session:
        # get the series related to a specific book id
        series_mappings_query = select(SeriesMappingsTable).where(
            SeriesMappingsTable.bookId == book_id
        )
        series_mappings_table = session.exec(series_mappings_query).all()

        series_list = []
        for series_mappings_row in series_mappings_table:
            series_query = select(SeriesTable).where(
                SeriesTable.id == series_mappings_row.seriesId
            )
            series_table = session.exec(series_query).one_or_none()

            series = Series()
            series.id = series_table.id
            series.name = series_table.name
            series.seriesAsin = series_table.seriesAsin
            series.sequence = series_mappings_row.sequence
            series_list.append(series)

        return series_list


def getSeriesByBook(engine: create_engine, search_string) -> list:
    """Get list of books in a series by book asin or title"""

    # import BooksTable and returnBookObj locally to avoid circular import
    from app.db_models.tables.books import BooksTable, returnBookObj

    with Session(engine) as session:
        # find the book row by asin
        book_row = session.exec(select(BooksTable).where(or_(BooksTable.bookAsin == search_string, BooksTable.title == search_string))).one_or_none()
        if not book_row:
            return []
        book_id = book_row.id

        # get series mappings for this book id
        series_mappings_results = session.exec(select(SeriesMappingsTable).where(SeriesMappingsTable.bookId == book_id)).all()
        if not series_mappings_results:
            return []
        series_id = series_mappings_results[0].seriesId

        # get all mappings for the series id
        mappings_in_series = session.exec(select(SeriesMappingsTable).where(SeriesMappingsTable.seriesId == series_id)).all()

        # build list of book objects in the series
        series_list = []
        for mapping in mappings_in_series:
            book_row = session.exec(select(BooksTable).where(BooksTable.id == mapping.bookId)).one_or_none()
            if book_row:
                series_list.append(returnBookObj(engine, book_row))

        return series_list


def getBooksInSeries(engine: create_engine, search_string) -> list:
    """Get list of books in a series by series id or name"""

    # import BooksTable and returnBookObj locally to avoid circular import
    from app.db_models.tables.books import BooksTable, returnBookObj

    with Session(engine) as session:
        # find the series id in case name is provided
        series_id = session.exec(select(SeriesTable.id).where(or_(SeriesTable.id == search_string, SeriesTable.name == search_string))).one_or_none()
        if not series_id:
            return []
        
        # get book ids for this series_id using the series mappings table
        series_mappings_results = session.exec(select(SeriesMappingsTable).where(SeriesMappingsTable.seriesId == series_id)).all()
        if not series_mappings_results:
            return []
        book_ids = []
        for mapping in series_mappings_results:
            book_ids.append(mapping.bookId)

        # build list of book objects in the series
        books_list = []
        for book_id in book_ids:
            book_results = session.exec(select(BooksTable).where(BooksTable.id == book_id)).all()
            if book_results:
                for book_row in book_results:
                    books_list.append(returnBookObj(engine, book_row))

        return books_list



def getAllSeries(engine) -> list:
    """Gets all series"""
    with Session(engine) as session:
        statement = select(SeriesTable).order_by(SeriesTable.name)
        results = session.exec(statement).all()

        series_list = []
        for single_series in results:
            series = returnSeriesObj(single_series)
            series_list.append(series)

        return series_list


def calculateSeriesRating(engine, series_id: str) -> Decimal:
    """Averages ratings of books in a series and updates the series table entry"""
    books_in_series = getBooksInSeries(engine, series_id)

    if books_in_series:
        total = 0
        for single_book in books_in_series:
            if single_book.audibleOverallAvgRating != 0:
                total += single_book.audibleOverallAvgRating

        rating = round(total / len(books_in_series), 2)
        
        return rating


def returnSeriesObj(sql_data) -> Series:
    series = Series()
    series.id = sql_data.id
    series.name = sql_data.name
    series.seriesAsin = sql_data.seriesAsin
    if hasattr(sql_data, "sequence"):
        series.sequence = sql_data.sequence
    series.rating = sql_data.rating
    return series


def cleanupDanglingSeries(engine: create_engine):
    """Deletes DB entries from the SeriesTable and SeriesMappingsTable that don't have a seriesAsin."""

    with Session(engine) as session:
        # Find series that don't have a seriesAsin
        statement = select(SeriesTable).where(SeriesTable.seriesAsin.is_(None))
        series_without_asin = session.exec(statement).all()

        for series in series_without_asin:
            print(f"Deleting series without seriesAsin: {series.name} (ID: {series.id})")
            # Delete mappings for this series
            session.exec(delete(SeriesMappingsTable).where(SeriesMappingsTable.seriesId == series.id))
            # Delete the series
            session.delete(series)

        session.commit()
