"""Pytest configuration and fixtures for e2e tests."""
import pytest
import os
import tempfile
import shutil
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session

from main import app
from app.services.sqlite import SQLiteService


@pytest.fixture(scope="session")
def temp_config_dir():
    """Create a temporary config directory for testing."""
    temp_dir = tempfile.mkdtemp(prefix="aim_test_")
    os.environ["CONFIG_DIR"] = temp_dir
    yield temp_dir
    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    # Remove env var
    if "CONFIG_DIR" in os.environ:
        del os.environ["CONFIG_DIR"]


@pytest.fixture(scope="session")
def test_db_service(temp_config_dir):
    """Create a test SQLite service with in-memory database."""
    # Use in-memory database for testing
    db_url = "sqlite:///:memory:"
    service = SQLiteService(database_url=db_url)
    service.create_tables()
    return service


@pytest.fixture(scope="session")
def test_client(temp_config_dir, test_db_service):
    """Create a test client for the FastAPI app."""
    # Override the database service in the app
    from main import database
    from app.routers.pages import index, series, books
    from app.routers.pages import settings_page, serieswatchlist_page, bookwishlist_page
    from app.routers.api import book_api, series_api, admin_api, settings_api, user_api
    
    # Override all the db_service getters
    original_get_db = None
    
    def override_get_db():
        return test_db_service
    
    # Patch the database service in all modules
    for module in [index, series, books, settings_page, serieswatchlist_page, bookwishlist_page,
                   book_api, series_api, admin_api, settings_api, user_api]:
        if hasattr(module, 'get_db_service'):
            module.get_db_service = override_get_db
    
    # Patch the global database
    original_database = database
    database = test_db_service
    
    with TestClient(app) as client:
        yield client
    
    # Restore original
    database = original_database
    for module in [index, series, books, settings_page, serieswatchlist_page, bookwishlist_page,
                   book_api, series_api, admin_api, settings_api, user_api]:
        if hasattr(module, 'get_db_service') and original_get_db:
            module.get_db_service = original_get_db
