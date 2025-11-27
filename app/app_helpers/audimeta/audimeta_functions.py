from app.app_helpers.audimeta import audimeta_api
from app.app_helpers.audimeta import audimeta_helpers

from app.db_models.tables.books import updateBook, getAllBooks


def backfillAudimetaBookData(engine) -> None:
    """
    Populates missing book, author, genre, narrator, and series information from audimeta.
    """

    all_books = getAllBooks(engine)

    for single_book in all_books:
        audimeta_book = audimeta_api.getAudimetaBook(single_book.bookAsin)
        break
        if audimeta_book is None:
            continue  # Skip this book

        # import json
        # print(json.dumps(audimeta_book, indent=4))

        book = audimeta_helpers.returnBookObj(audimeta_book, True)

        updateBook(engine, book)
