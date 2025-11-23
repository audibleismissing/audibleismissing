import sqlite3


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

                            /* sequence comes from the mapping */
                            sm.sequence,

                            /* SERIES‑LEVEL data – same as before */
                            s.id          AS seriesId,
                            s.name        AS seriesname,
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
        print('DB conneciton error occured -', error)


def getViewAllBooks(engine, sqlite_path) -> list:
    with sqlite3.connect(sqlite_path) as conn:
        """Get all books using the booksandseries view"""
        cur = conn.cursor()
        cur.execute('select * from booksandseries')
        results = cur.fetchall()
        if results:
            all_books = []
            for item in results:
                # book = returnBookObj(engine, item)
                all_books.append(item)
                print(item.sequence)

            return all_books
        return []


def getViewSeriesDetails(sqlite_path, series_id) -> list:
    """Get all books with series_id using the booksandseries view"""
    with sqlite3.connect(sqlite_path) as conn:
        cur = conn.cursor()
        cur.execute('select * from booksandseries where seriesId = ?', (series_id,))
        results = cur.fetchall()
        if results:
            books = []
            columns = [desc[0] for desc in cur.description]
            for row in results:
                book_dict = dict(zip(columns, row))
                books.append(book_dict)
            return books
        return []