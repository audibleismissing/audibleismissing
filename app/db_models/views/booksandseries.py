import sqlite3


def createBooksAndSeriesView(sqlite_db) -> None:
    try:
        with sqlite3.connect(sqlite_db) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                    CREATE VIEW IF NOT EXISTS booksandseries AS
                    SELECT
                        books.id AS bookId,
                        books.title,
                        books.bookAsin,
                        books.isOwned,
                        books.releaseDate,
                        books.audibleOverallAvgRating,
                        seriesmappings.sequence,
                        series.id AS seriesId,
                        series.name AS seriesname,
                        series.seriesAsin,
                        series.totalBooksInSeries,
                        series.totalBooksInLibrary
                    FROM books
                    INNER JOIN seriesmappings ON books.id = seriesmappings.bookId
                    INNER JOIN series ON seriesmappings.seriesId = series.id
                    ORDER BY 
                        seriesname,
                        CASE 
                            WHEN seriesmappings.sequence IS NULL THEN 999999999
                            WHEN seriesmappings.sequence LIKE '%[^0-9]%' THEN 999999998
                            ELSE CAST(seriesmappings.sequence AS INTEGER)
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