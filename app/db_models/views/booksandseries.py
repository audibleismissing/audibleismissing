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
                        series.id AS seriesId,
                        series.name AS seriesname,
                        series.seriesAsin
                    FROM books
                    INNER JOIN seriesmappings ON books.id = seriesmappings.bookId
                    INNER JOIN series ON seriesmappings.seriesId = series.id
                """)
            connection.commit()
    except sqlite3.Error as error:
        print('DB conneciton error occured -', error)