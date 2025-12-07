import sqlite3
from fastapi import Depends

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


# service: SQLiteService = Depends(get_db_service)):

def createBooksAndSeriesView(sqlite_db) -> None:
    try:
        with sqlite3.connect(sqlite_db) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                    CREATE VIEW IF NOT EXISTS booksandseries AS
                        SELECT
                            /* 1‑BOOK‑LEVEL data – same as before */
                            b.id           AS bookId,
                            b.title,
                            b.bookAsin,
                            b.isOwned,
                            b.releaseDate,
                            b.audibleOverallAvgRating,
                            b.imageUrl,
                            b.description,

                            /* sequence comes from the mapping */
                            sm.sequence,

                            /* SERIES‑LEVEL data – same as before */
                            s.id          AS seriesId,
                            s.name        AS seriesName,
                            s.seriesAsin,

                            /* NEW: counts calculated on the fly */
                            COUNT(*)                         OVER (PARTITION BY s.id)          AS totalBooksInSeries,
                            SUM(CASE WHEN b.isOwned THEN 1 ELSE 0 END)
                                            OVER (PARTITION BY s.id)                     AS totalBooksInLibrary

                        FROM books     AS b
                        JOIN seriesmappings AS sm
                            ON b.id = sm.bookId
                        JOIN series      AS s
                            ON sm.seriesId = s.id
                        ORDER BY
                            s.name,
                            CASE
                                WHEN sm.sequence IS NULL        THEN 9_999_999_999
                                WHEN sm.sequence LIKE '%[^0-9]%' THEN 9_999_999_998
                                ELSE CAST(sm.sequence AS INTEGER)
                            END;
                """)
            connection.commit()
    except sqlite3.Error as error:
        print("DB conneciton error occured -", error)


def getViewAllBooks(service: SQLiteService = Depends(get_db_service)) -> list:
    with sqlite3.connect(service.db_path) as conn:
        """Get all books using the booksandseries view"""
        cur = conn.cursor()
        cur.execute("select * from booksandseries")
        results = cur.fetchall()
        if results:
            all_books = []
            columns = [desc[0] for desc in cur.description]
            for row in results:
                book_dict = dict(zip(columns, row))
                all_books.append(book_dict)

            return all_books
        return []


def getViewSeriesDetails(series_id, service: SQLiteService = Depends(get_db_service)) -> list:
    """Get all books with series_id using the booksandseries view"""
    with sqlite3.connect(service.db_path) as conn:
        cur = conn.cursor()
        cur.execute("select * from booksandseries where seriesId = ?", (series_id,))
        results = cur.fetchall()
        if results:
            books = []
            columns = [desc[0] for desc in cur.description]
            for row in results:
                book_dict = dict(zip(columns, row))
                books.append(book_dict)
            return books
        return []


def getViewBookDetails(book_id, service: SQLiteService = Depends(get_db_service)):
    """Get book details from booksandseriesview."""
    with sqlite3.connect(service.db_path) as conn:
        cur = conn.cursor()
        cur.execute("select * from booksandseries where bookId = ?", (book_id,))
        results = cur.fetchone()
        if results:
            columns = [desc[0] for desc in cur.description]
            book_dict = dict(zip(columns, results))
            return book_dict
        return {}

#adfhasldfhaslkdjflkajshdflkjashdlfjhaslkdjfhlasdf
def getViewReleaseDates(time_window, service: SQLiteService = Depends(get_db_service)) -> list:
    """Get upcoming book releases using the booksandseries view"""
    from datetime import datetime

    current_date = datetime.now().strftime("%Y-%m-%d")

    with sqlite3.connect(service.db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "select * from booksandseries where releaseDate >= ? ORDER BY releaseDate ASC LIMIT ?",
            (current_date, time_window),
        )
        results = cur.fetchall()
        if results:
            books = []
            columns = [desc[0] for desc in cur.description]
            for row in results:
                book_dict = dict(zip(columns, row))
                books.append(book_dict)
            return books
        return []


def getViewWatchListReleaseDates(time_window, service: SQLiteService = Depends(get_db_service)) -> list:
    """Get upcoming book releases that are in series on the series watch list. Returns list."""
    from datetime import datetime

    current_date = datetime.now().strftime("%Y-%m-%d")

    with sqlite3.connect(service.db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM booksandseries
            WHERE releaseDate >= ?
            AND seriesId IN (SELECT seriesId FROM serieswatchlist)
            ORDER BY releaseDate ASC
            LIMIT ?
        """,
            (current_date, time_window),
        )
        results = cur.fetchall()
        if results:
            books = []
            columns = [desc[0] for desc in cur.description]
            for row in results:
                book_dict = dict(zip(columns, row))
                books.append(book_dict)
            return books
        return []
