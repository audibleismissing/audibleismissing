import uuid
from fastapi import Depends

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select

from app.custom_objects.bookwishlistitem import BookWishListItem
from app.services.sqlite import SQLiteService

# setup global services
db_service = None


def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service


class BookWishListTable(SQLModel, table=True):
    __tablename__ = "bookwishlist"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    bookId: str | None


def addBookWishListItem(book_id, service: SQLiteService) -> str:
    """Add BookWishListItem"""
    print(f"Adding BookWishListItem: {book_id}")
    row = BookWishListTable(
        bookId=book_id,
    )

    with Session(service.engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id
    return None


def getBookWishListItem(search_string, service: SQLiteService) -> BookWishListItem:
    """Get BookWishListItem
    returns: BookWishListItem
    """
    with Session(service.engine) as session:
        statement = select(BookWishListTable).where(
            or_(
                BookWishListTable.bookId == search_string,
                BookWishListTable.id == search_string,
            )
        )

        results = session.exec(statement).first()
        if results:
            return returnBookWishListItemObj(results)
        return None


def updateBookWishListItem(
    wish_list_item: BookWishListItem, service: SQLiteService
) -> str:
    """Update BookWishListItem
    returns: row id
    """
    print(f"Updating BookWishListItem: {wish_list_item.id}")
    with Session(service.engine) as session:
        statement = select(BookWishListTable).where(
            BookWishListTable.id == wish_list_item.id
        )
        results = session.exec(statement).one()

        results.bookId = wish_list_item.bookId

        session.add(results)
        session.commit()
        return results.id


def deleteBookWishListItem(wish_list_item_id, service: SQLiteService) -> None:
    """Delete BookWishListItem"""
    print(f"Deleting BookWishListItem: {wish_list_item_id}")
    with Session(service.engine) as session:
        statement = select(BookWishListTable).where(
            BookWishListTable.id == wish_list_item_id
        )
        results = session.exec(statement)
        row = results.one()
        session.delete(row)
        session.commit()


def returnBookWishListItemObj(sql_data) -> BookWishListItem:
    """Converts sql data to BookWishListItem"""
    item = BookWishListItem()
    item.id = sql_data.id
    item.bookId = sql_data.bookId

    return item


def getAllBookWishListItems(service: SQLiteService) -> list:
    """Gets all BookWishListItems"""
    with Session(service.engine) as session:
        statement = select(BookWishListTable)
        results = session.exec(statement).all()

        wish_list = []
        for single_item in results:
            wish_list_item = returnBookWishListItemObj(single_item)
            wish_list.append(wish_list_item)

        return wish_list
