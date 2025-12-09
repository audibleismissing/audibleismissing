import uuid
from fastapi import Depends

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select, delete

from app.custom_objects.author import Author
from app.db_models.tables.authorsmappings import AuthorsMappingsTable
from app.services.sqlite import SQLiteService
from app.db_models.tables.helpers import (
    returnAuthorObj,
    returnBookObj,
    returnGenreObj,
    returnNarratorObj,
    returnSeriesObj,
)

# setup global services
db_service = None


def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service


class AuthorsTable(SQLModel, table=True):
    __tablename__ = "authors"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    authorAsin: str | None = None


def addAuthor(author: Author, service: SQLiteService) -> str:
    """Add author to db"""
    print(f"Adding author: {author.name}")
    row = AuthorsTable(name=author.name, authorAsin=author.authorAsin)

    with Session(service.engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id


def getAuthor(search_string, service: SQLiteService):
    """Get author from db"""
    with Session(service.engine) as session:
        statement = select(AuthorsTable).where(
            or_(
                AuthorsTable.name == search_string,
                AuthorsTable.authorAsin == search_string,
                AuthorsTable.id == search_string,
            )
        )

        results = session.exec(statement).first()
        if results:
            return returnAuthorObj(results)
        return None


def updateAuthor(author: Author, service: SQLiteService) -> str:
    """Update author in db"""
    print(f"Updating author: {author.name}")
    with Session(service.engine) as session:
        statement = select(AuthorsTable).where(AuthorsTable.id == author.id)
        results = session.exec(statement).one()

        results.name = author.name
        results.authorAsin = author.authorAsin

        session.add(results)
        session.commit()
        return results.id


def deleteAuthor():
    """Delete author from db"""


def doesAuthorExist(search_string, service: SQLiteService) -> bool:
    with Session(service.engine) as session:
        statement = select(AuthorsTable).where(
            or_(
                AuthorsTable.name == search_string,
                AuthorsTable.authorAsin == search_string,
                AuthorsTable.id == search_string,
            )
        )

        results = session.exec(statement)
        if len(results.all()) > 0:
            return True
        else:
            return False


def getBookAuthors(book_id, service: SQLiteService) -> list:
    """Get authors by book id"""
    with Session(service.engine) as session:
        # get the authors related to a specific book id
        author_mappings_query = select(AuthorsMappingsTable).where(
            AuthorsMappingsTable.bookId == book_id
        )
        author_mappings_table = session.exec(author_mappings_query).all()

        authors = []
        for author_mappings_row in author_mappings_table:
            author_query = select(AuthorsTable).where(
                AuthorsTable.id == author_mappings_row.authorId
            )
            authors_table = session.exec(author_query).one_or_none()

            author = Author()
            author.id = authors_table.id
            author.name = authors_table.name
            author.authorAsin = authors_table.authorAsin
            authors.append(author)

    return authors


def cleanupDanglingAuthors(service: SQLiteService) -> None:
    """Deletes DB entries from the AuthorsTable and AuthorsMappingsTable that don't have a authorsAsin."""

    with Session(service.engine) as session:
        # Find authors that don't have a authorsAsin
        statement = select(AuthorsTable).where(AuthorsTable.authorAsin.is_(None))
        authors_without_asin = session.exec(statement).all()

        for authors in authors_without_asin:
            print(
                f"Deleting authors without authorsAsin: {authors.name} (ID: {authors.id})"
            )
            # Delete mappings for this authors
            session.exec(
                delete(AuthorsMappingsTable).where(
                    AuthorsMappingsTable.authorId == authors.id
                )
            )
            # Delete the authors
            session.delete(authors)

        session.commit()
