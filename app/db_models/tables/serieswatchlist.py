import uuid

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select

from app.custom_objects.serieswatchlistitem import SeriesWatchListItem

from app.services.sqlite import SQLiteService
from app.services.task_manager import BackgroundTaskManagerService

# setup global services
db_service = None
background_manager = None

def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service

def get_background_manager() -> BackgroundTaskManagerService:
    """Get the background task manager instance."""
    global background_manager
    if background_manager is None:
        background_manager = BackgroundTaskManagerService()
    return background_manager


# service: SQLiteService = Depends(get_db_service)



class SeriesWatchListTable(SQLModel, table=True):
    __tablename__ = "serieswatchlist"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    seriesId: str | None


def addSeriesWatchListItem(series_id, engine: create_engine) -> str:
    """Add SeriesWatchListItem"""
    print(f"Adding SeriesWatchListItem: {series_id}")
    row = SeriesWatchListTable(
        seriesId=series_id,
    )

    with Session(engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id
    return None


def getSeriesWatchListItem(search_string, engine: create_engine) -> SeriesWatchListItem:
    """Get SeriesWatchListItem
    returns: SeriesWatchListItem
    """
    with Session(engine) as session:
        statement = select(SeriesWatchListTable).where(
            or_(
                SeriesWatchListTable.seriesId == search_string,
                SeriesWatchListTable.id == search_string,
            )
        )

        results = session.exec(statement).first()
        if results:
            return returnSeriesWatchListItemObj(results)
        return None


def updateSeriesWatchListItem(
    engine: create_engine, watch_list_item: SeriesWatchListItem
) -> str:
    """Update SeriesWatchListItem
    returns: row id
    """
    print(f"Updating SeriesWatchListItem: {watch_list_item.id}")
    with Session(engine) as session:
        statement = select(SeriesWatchListTable).where(
            SeriesWatchListTable.id == watch_list_item.id
        )
        results = session.exec(statement).one()

        results.seriesId = watch_list_item.seriesId

        session.add(results)
        session.commit()
        return results.id


def deleteSeriesWatchListItem(engine: create_engine, watch_list_item_id) -> None:
    """Delete SeriesWatchListItem"""
    print(f"Deleting SeriesWatchListItem: {watch_list_item_id}")
    with Session(engine) as session:
        statement = select(SeriesWatchListTable).where(
            SeriesWatchListTable.id == watch_list_item_id
        )
        results = session.exec(statement)
        row = results.one()
        session.delete(row)
        session.commit()


def returnSeriesWatchListItemObj(sql_data) -> SeriesWatchListItem:
    """Converts sql data to SeriesWatchListItem"""
    item = SeriesWatchListItem()
    item.id = sql_data.id
    item.seriesId = sql_data.seriesId

    return item


def getAllSeriesWatchListItems(engine) -> list:
    """Gets all SeriesWatchListItems"""
    with Session(engine) as session:
        statement = select(SeriesWatchListTable)
        results = session.exec(statement).all()

        watch_list = []
        for single_item in results:
            watch_list_item = returnSeriesWatchListItemObj(single_item)
            watch_list.append(watch_list_item)

        return watch_list
