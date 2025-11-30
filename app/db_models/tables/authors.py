import uuid

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select, delete

from app.custom_objects.author import Author
from app.db_models.tables.authorsmappings import AuthorsMappingsTable


class AuthorsTable(SQLModel, table=True):
    __tablename__ = "authors"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    authorAsin: str | None = None


def addAuthor(engine: create_engine, author: Author) -> str:
    """Add author to db"""
    print(f"Adding author: {author.name}")
    row = AuthorsTable(name=author.name, authorAsin=author.authorAsin)

    with Session(engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id


def getAuthor(engine: create_engine, search_string):
    """Get author from db"""
    with Session(engine) as session:
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


def updateAuthor(engine: create_engine, author: Author) -> str:
    """Update author in db"""
    print(f"Updating author: {author.name}")
    with Session(engine) as session:
        statement = select(AuthorsTable).where(AuthorsTable.id == author.id)
        results = session.exec(statement).one()

        results.name = author.name
        results.authorAsin = author.authorAsin

        session.add(results)
        session.commit()
        return results.id


def deleteAuthor():
    """Delete author from db"""


def doesAuthorExist(engine: create_engine, search_string) -> bool:
    with Session(engine) as session:
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


def getBookAuthors(engine: create_engine, book_id) -> list:
    """Get authors by book id"""
    with Session(engine) as session:
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


def returnAuthorObj(sql_data) -> Author:
    author = Author()
    author.id = sql_data.id
    author.name = sql_data.name
    author.authorAsin = sql_data.authorAsin
    return author


def cleanupDanglingAuthors(engine) -> None:
    """Deletes DB entries from the AuthorsTable and AuthorsMappingsTable that don't have a authorsAsin."""

    with Session(engine) as session:
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
