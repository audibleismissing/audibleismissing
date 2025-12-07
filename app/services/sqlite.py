import os
import json
import logging

from typing import List, Optional, Generator
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import contextmanager

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



class SQLiteService:
    """Service for managing SQLite database operations."""

    def __init__(self, database_url: str = None):
        if database_url is None:
            print
            db_path = os.path.join(os.getcwd(), "config/audibleismissing.sqlite")
            database_url = f"sqlite:///{db_path}"

        self.engine = create_engine(
            database_url,
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
