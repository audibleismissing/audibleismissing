from app.app_helpers.audnexus import audnexus_api

from app.db_models.tables.books import updateBook, getAllBooks, getBook


def backfillAudnexusBookData(engine) -> None:
    """
    Populates missing book, author, genre, narrator, and series information from audimeta.
    """

    all_books = getAllBooks(engine)

    for single_book in all_books:
        audnexus_book = audnexus_api.getAudnexusBookAsBook(single_book.bookAsin)

        if audnexus_book is None:
            continue  # Skip this book
        
        library_book = getBook(engine, audnexus_book.bookAsin)
        audnexus_book.id = library_book.id
        audnexus_book.isOwned = library_book.isOwned
        updateBook(engine, audnexus_book)
