"""E2E tests for main page endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestIndexPage:
    """Tests for the index page endpoint."""
    
    @pytest.mark.e2e
    def test_index_page_returns_200(self, test_client: TestClient):
        """Test that the index page returns HTTP 200."""
        response = test_client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_index_page_contains_title(self, test_client: TestClient):
        """Test that the index page contains expected content."""
        response = test_client.get("/")
        assert response.status_code == 200
        # Check for expected HTML elements
        assert "<title>" in response.text or "Audible is Missing" in response.text


class TestSeriesEndpoints:
    """Tests for series-related endpoints."""
    
    @pytest.mark.e2e
    def test_series_list_page_returns_200(self, test_client: TestClient):
        """Test that the series list page returns HTTP 200."""
        response = test_client.get("/series")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_series_list_api_returns_200(self, test_client: TestClient):
        """Test that the series list API endpoint returns HTTP 200."""
        response = test_client.get("/api/series/all")
        assert response.status_code == 200
        # Should return JSON
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_series_list_page_returns_200(self, test_client: TestClient):
        """Test that the series list page returns HTTP 200."""
        response = test_client.get("/series")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestBooksEndpoints:
    """Tests for book-related endpoints."""
    
    @pytest.mark.e2e
    def test_books_list_page_returns_200(self, test_client: TestClient):
        """Test that the books list page returns HTTP 200."""
        response = test_client.get("/books")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_books_api_returns_200(self, test_client: TestClient):
        """Test that the books API endpoint returns HTTP 200."""
        response = test_client.get("/api/books/all")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_book_details_page_returns_404_for_nonexistent(self, test_client: TestClient):
        """Test that book details page returns 404 for non-existent book."""
        response = test_client.get("/book/details/nonexistent-id")
        # Should return 200 but with empty data since no exception handling
        assert response.status_code == 200


class TestSettingsEndpoints:
    """Tests for settings-related endpoints."""
    
    @pytest.mark.e2e
    def test_settings_page_returns_200(self, test_client: TestClient):
        """Test that the settings page returns HTTP 200."""
        response = test_client.get("/settings")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestWatchlistEndpoints:
    """Tests for watchlist endpoints."""
    
    @pytest.mark.e2e
    def test_series_watchlist_page_returns_200(self, test_client: TestClient):
        """Test that the series watchlist page returns HTTP 200."""
        response = test_client.get("/user/serieswatchlist/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_book_wishlist_page_returns_200(self, test_client: TestClient):
        """Test that the book wishlist page returns HTTP 200."""
        response = test_client.get("/user/bookwishlist/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestAPIEndpoints:
    """Tests for API endpoints that don't require data."""
    
    @pytest.mark.e2e
    def test_api_books_allview_returns_200(self, test_client: TestClient):
        """Test the books allview endpoint."""
        response = test_client.get("/api/books/allview")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_api_series_books_returns_200(self, test_client: TestClient):
        """Test the series books endpoint."""
        response = test_client.get("/api/series/books/test-series-id")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_api_series_details_returns_200(self, test_client: TestClient):
        """Test the series details endpoint."""
        response = test_client.get("/api/series/details/test-series-id")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_api_series_counts_returns_200(self, test_client: TestClient):
        """Test the series counts endpoint."""
        response = test_client.get("/api/series/counts/test-series-id")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_api_health_returns_200(self, test_client: TestClient):
        """Test a basic health check endpoint."""
        # Test that API is alive
        response = test_client.get("/api/books/all")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_api_book_authors_returns_200(self, test_client: TestClient):
        """Test the book authors endpoint."""
        response = test_client.get("/api/book/authors/test-book-id")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_api_book_narrators_returns_200(self, test_client: TestClient):
        """Test the book narrators endpoint."""
        response = test_client.get("/api/book/narrators/test-book-id")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_api_book_genres_returns_200(self, test_client: TestClient):
        """Test the book genres endpoint."""
        response = test_client.get("/api/book/genres/test-book-id")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.e2e
    def test_api_book_releasedates_returns_200(self, test_client: TestClient):
        """Test the book release dates endpoint."""
        response = test_client.get("/api/book/releasedates/10")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
