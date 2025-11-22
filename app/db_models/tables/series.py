import uuid

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select, func
from app.custom_objects.series import Series
from app.db_models.tables.seriesmappings import SeriesMappingsTable



class SeriesTable(SQLModel, table=True):
    __tablename__ = "series"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    seriesAsin: str | None = None
    totalBooksInSeries: int | None = None
    totalBooksInLibrary: int | None = None


def addSeries(engine: create_engine, series: Series) -> str:
    """Add series to db"""
    # check if series already exists
    if not doesSeriesExist(engine, series.name):
        row = SeriesTable(
            name=series.name,
            totalBooksInLibrary=0,
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


def updateSeries(engine: create_engine, series: Series) -> None:
    """Update series in db"""
    with Session(engine) as session:
        statement = select(SeriesTable).where(SeriesTable.id == series.id)
        results = session.exec(statement).one()

        results.name = series.name
        results.seriesAsin = series.seriesAsin
        results.totalBooksInSeries = series.totalBooksInSeries

        # Calculate totalBooksInLibrary as count of books in this series
        count_statement = select(func.count()).select_from(SeriesMappingsTable).where(SeriesMappingsTable.seriesId == series.id)
        results.totalBooksInLibrary = session.exec(count_statement).one()

        session.add(results)
        session.commit()


def updateTotalBooksInLibrary(engine: create_engine, series_id: str) -> None:
    """Update the totalBooksInLibrary for a specific series"""
    with Session(engine) as session:
        statement = select(SeriesTable).where(SeriesTable.id == series_id)
        results = session.exec(statement).one()

        # Calculate totalBooksInLibrary as count of books in this series
        count_statement = select(func.count()).select_from(SeriesMappingsTable).where(SeriesMappingsTable.seriesId == series_id)
        results.totalBooksInLibrary = session.exec(count_statement).one()

        session.add(results)
        session.commit()


def deleteSeries():
    """Delete series from db"""


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
        statement = select(SeriesTable)
        results = session.exec(statement).all()

        series_list = []
        for single_series in results:
            series = returnSeriesObj(single_series)
            series_list.append(series)

        return series_list
    


def returnSeriesObj(sql_data) -> Series:
    series = Series()
    series.id = sql_data.id
    series.name = sql_data.name
    series.seriesAsin = sql_data.seriesAsin
    series.totalBooksInSeries = sql_data.totalBooksInSeries
    series.totalBooksInLibrary = sql_data.totalBooksInLibrary
    if hasattr(sql_data, "sequence"):
        series.sequence = sql_data.sequence
    return series
