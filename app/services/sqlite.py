import os
import json
import logging

from typing import List, Optional, Generator
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import contextmanager

# needed for db table creation
from app.db_models.tables import (
    authors,
    authorsmappings,
    books,
    bookwishlist,
    genremappings,
    genres,
    narratormappings,
    narrators,
    series,
    seriesmappings,
    serieswatchlist,
)
from app.db_models.views import booksandseries, seriesandcounts



class SQLiteService:
    """Service for managing SQLite database operations."""

    def __init__(self, database_url: str = None):
        if database_url is None:
            self.db_path = os.path.join(os.getcwd(), "config/audibleismissing.sqlite")
            self.database_url = f"sqlite:///{self.db_path}"

        self.engine = create_engine(
            self.database_url,
            connect_args={"check_same_thread": False},  # Required for SQLite
            echo=False  # Set to True for debugging
        )

        # logging config
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Create tables
        self.create_tables()

    def create_tables(self):
        """Create all database tables."""
        self.logger.info("Creating database tables.")
        SQLModel.metadata.create_all(self.engine)
        booksandseries.createBooksAndSeriesView(self.db_path)
        seriesandcounts.createSeriesAndCountsView(self.db_path)
