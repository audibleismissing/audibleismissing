import sqlite3
import logging
from app.services.sqlite import SQLiteService

logger = logging.getLogger(__name__)


def createSeriesAndCountsView(sqlite_db) -> None:
    try:
        with sqlite3.connect(sqlite_db) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                    CREATE VIEW IF NOT EXISTS seriesandcounts AS
                        SELECT
                            s.id          AS seriesId,
                            s.name        AS seriesName,
                            s.seriesAsin,
                            s.rating,

                            /* How many books are part of this series */
                            COUNT(b.id)                                                                   
                                AS totalBooksInSeries,

                            /* How many of those books the library owns */
                            SUM(CASE WHEN b.isOwned THEN 1 ELSE 0 END)                                    
                                AS totalBooksInLibrary
                        FROM   series          AS s
                        JOIN   seriesmappings  AS sm  ON sm.seriesId = s.id
                        JOIN   books           AS b   ON b.id = sm.bookId
                        GROUP BY
                            s.id,
                            s.name,
                            s.seriesAsin,
                            s.rating
                        ORDER BY
                            s.name;
                """)
            connection.commit()
    except sqlite3.Error as error:
        logger.error(f"DB connection error occurred - {error}")


def getViewSeriesCounts(service: SQLiteService) -> list:
    with sqlite3.connect(service.db_path) as conn:
        """Get all books using the seriesandcounts view"""
        cur = conn.cursor()
        cur.execute("select * from seriesandcounts")
        results = cur.fetchall()
        if results:
            all_series = []
            columns = [desc[0] for desc in cur.description]
            for row in results:
                series_dict = dict(zip(columns, row))
                all_series.append(series_dict)
            return all_series
        return []


def getViewSeriesCountsBySeries(series_id, service: SQLiteService) -> list:
    """Get single series with series_id using the seriesandcounts view"""
    with sqlite3.connect(service.db_path) as conn:
        cur = conn.cursor()
        cur.execute("select * from seriesandcounts where seriesId = ?", (series_id,))
        results = cur.fetchall()
        if results:
            books = []
            columns = [desc[0] for desc in cur.description]
            for row in results:
                book_dict = dict(zip(columns, row))
                books.append(book_dict)
            return books
        return []


def getViewSeriesCountsSingleSeries(service: SQLiteService, series_id):
    """Get single series with series_id using the seriesandcounts view"""
    with sqlite3.connect(service.db_path) as conn:
        cur = conn.cursor()
        cur.execute("select * from seriesandcounts where seriesId = ?", (series_id,))
        results = cur.fetchone()
        if results:
            columns = [desc[0] for desc in cur.description]
            series_dict = dict(zip(columns, results))
            return series_dict
        return {}
