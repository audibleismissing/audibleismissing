import sqlite3

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
        print('DB conneciton error occured -', error)


def getViewSeriesCounts(sqlite_path) -> list:
    with sqlite3.connect(sqlite_path) as conn:
        """Get all books using the seriesandcounts view"""
        cur = conn.cursor()
        cur.execute('select * from seriesandcounts')
        results = cur.fetchall()
        if results:
            all_series = []
            columns = [desc[0] for desc in cur.description]
            for row in results:
                series_dict = dict(zip(columns, row))
                all_series.append(series_dict)
            return all_series
        return []
    

def getViewSeriesCountsBySeries(sqlite_path, series_id) -> list:
    """Get single series with series_id using the seriesandcounts view"""
    with sqlite3.connect(sqlite_path) as conn:
        cur = conn.cursor()
        cur.execute('select * from seriesandcounts where seriesId = ?', (series_id,))
        results = cur.fetchall()
        if results:
            books = []
            columns = [desc[0] for desc in cur.description]
            for row in results:
                book_dict = dict(zip(columns, row))
                books.append(book_dict)
            return books
        return []


def getViewSeriesCountsSingleSeries(sqlite_path, series_id):
    """Get single series with series_id using the seriesandcounts view"""
    with sqlite3.connect(sqlite_path) as conn:
        cur = conn.cursor()
        cur.execute('select * from seriesandcounts where seriesId = ?', (series_id,))
        results = cur.fetchone()
        if results:
            columns = [desc[0] for desc in cur.description]
            series_dict = dict(zip(columns, results))
            return series_dict
        return {}
        