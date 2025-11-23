import uuid

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select


class NarratorMappingsTable(SQLModel, table=True):
    __tablename__ = "narratormappings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    narratorId: str = Field(default=None, foreign_key="narrators.id")
    bookId: str = Field(default=None, foreign_key="books.id")



def addNarratorMapping(engine:create_engine, narrator_id, book_id) -> str:
    """Add narrator mapping to db"""
    print(f"Adding narrator mapping: {narrator_id} -> {book_id}")
    row = NarratorMappingsTable(
        narratorId=narrator_id,
        bookId=book_id
    )

    with Session(engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id
    return None


def getNarratorMapping():
    """Get narrator mapping from db"""


def updateNarratorMapping():
    """Update narrator mapping in db"""


def deleteNarratorMapping():
    """Delete narrator mapping from db"""