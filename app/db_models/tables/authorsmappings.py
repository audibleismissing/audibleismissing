import uuid

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select

from app.custom_objects import book

class AuthorsMappingsTable(SQLModel, table=True):
    __tablename__ = "authormappings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    authorId: str | None = Field(default=None, foreign_key="authors.id")
    bookId: str | None = Field(default=None, foreign_key="books.id")



def addAuthorMapping(engine:create_engine, author_id, book_id) -> str:
    """Add author mapping to db"""
    print(f"Adding author mapping: {author_id} -> {book_id}")
    row = AuthorsMappingsTable(
        authorId=author_id,
        bookId=book_id
    )

    with Session(engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id
    return None


def getAuthorMapping():
    """Get author mapping from db"""


def updateAuthorMapping():
    """Update author mapping in db"""


def deleteAuthorMapping():
    """Delete author mapping from db"""