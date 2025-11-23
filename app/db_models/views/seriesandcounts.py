import sqlite3

def createSeriesAndCountsView(sqlite_db) -> None:
    try:
        with sqlite3.connect(sqlite_db) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                    CREATE VIEW IF NOT EXISTS seriesandcounts AS
                        SELECT
                            s.id          AS seriesId,
                            s.name        AS seriesname,
                            s.seriesAsin,

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
                            s.seriesAsin
                        ORDER BY
                            s.name;
                """)
            connection.commit()
    except sqlite3.Error as error:
        print('DB conneciton error occured -', error)
