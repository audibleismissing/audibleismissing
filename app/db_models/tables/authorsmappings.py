import uuid
from fastapi import Depends

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select

from app.custom_objects import book
from app.services.sqlite import SQLiteService

# setup global services
db_service = None


def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service


class AuthorsMappingsTable(SQLModel, table=True):
    __tablename__ = "authormappings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    authorId: str | None = Field(default=None, foreign_key="authors.id")
    bookId: str | None = Field(default=None, foreign_key="books.id")


def addAuthorMapping(author_id, book_id, service: SQLiteService) -> str:
    """Add author mapping to db"""
    print(f"Adding author mapping: {author_id} -> {book_id}")
    row = AuthorsMappingsTable(authorId=author_id, bookId=book_id)

    with Session(service.engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id
    return None


def getAuthorMappingByBook(book_id, service: SQLiteService):
    """Get author mapping from db"""
    with Session(service.engine) as session:
        statement = select(AuthorsMappingsTable).where(
            AuthorsMappingsTable.bookId == book_id
        )

        results = session.exec(statement).first()
        if results:
            return results
        return None


def updateAuthorMapping():
    """Update author mapping in db"""


def deleteAuthorMapping():
    """Delete author mapping from db"""
