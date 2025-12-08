import uuid
from fastapi import Depends

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select
from app.custom_objects.narrator import Narrator
from app.db_models.tables.narratormappings import NarratorMappingsTable
from app.services.sqlite import SQLiteService
from app.db_models.tables.helpers import returnAuthorObj, returnBookObj, returnGenreObj, returnNarratorObj, returnSeriesObj

# setup global services
db_service = None

def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service


class NarratorsTable(SQLModel, table=True):
    __tablename__ = "narrators"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str


def addNarrator(narrator: Narrator, service: SQLiteService) -> str:
    """Add narrator to db"""
    print(f"Adding narrator: {narrator.name}")
    row = NarratorsTable(
        name=narrator.name,
    )

    with Session(service.engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id


def getNarrator(search_string, service: SQLiteService):
    """Get narrator from db"""
    with Session(service.engine) as session:
        statement = select(NarratorsTable).where(
            or_(
                NarratorsTable.name == search_string, NarratorsTable.id == search_string
            )
        )

        results = session.exec(statement).first()
        if results:
            return returnNarratorObj(results)
        return None


def updateNarrator(narrator: Narrator, service: SQLiteService) -> str:
    """Update narrator in db"""
    print(f"Updating narrator: {narrator.name}")
    with Session(service.engine) as session:
        statement = select(NarratorsTable).where(NarratorsTable.id == narrator.id)
        results = session.exec(statement).one()

        results.name = narrator.name

        session.add(results)
        session.commit()
        return results.id


def deleteNarrator():
    """Delete narrator from db"""


def doesNarratorExist(search_string, service: SQLiteService) -> bool:
    with Session(service.engine) as session:
        statement = select(NarratorsTable).where(
            or_(
                NarratorsTable.name == search_string, NarratorsTable.id == search_string
            )
        )

        results = session.exec(statement)
        if len(results.all()) > 0:
            return True
        else:
            return False


def getBookNarrators(book_id, service: SQLiteService) -> list:
    """Get narrators by book id"""
    with Session(service.engine) as session:
        # get the authors related to a specific book id
        narrator_mappings_query = select(NarratorMappingsTable).where(
            NarratorMappingsTable.bookId == book_id
        )
        narrator_mappings_table = session.exec(narrator_mappings_query).all()

        narrators = []
        for narrator_mappings_row in narrator_mappings_table:
            narrator_query = select(NarratorsTable).where(
                NarratorsTable.id == narrator_mappings_row.narratorId
            )
            narrators_table = session.exec(narrator_query).one_or_none()

            narrator = Narrator()
            narrator.id = narrators_table.id
            narrator.name = narrators_table.name
            narrators.append(narrator)

        return narrators
