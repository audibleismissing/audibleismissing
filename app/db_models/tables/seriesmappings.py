import uuid

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select


class SeriesMappingsTable(SQLModel, table=True):
    __tablename__ = "seriesmappings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    sequence: str | None = None
    seriesId: str | None = Field(default=None, foreign_key="series.id")
    bookId: str | None = Field(default=None, foreign_key="books.id")



def addSeriesMapping(engine:create_engine, series_id, book_id, sequence) -> str:
    """Add series mapping to db"""
    row = SeriesMappingsTable(
        seriesId=series_id,
        bookId=book_id,
        sequence=sequence
    )

    with Session(engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id
    return None


def getSeriesMapping():
    """Get series mapping from db"""


def updateSeriesMapping():
    """Update series mapping in db"""


def deleteSeriesMapping():
    """Delete series mapping from db"""