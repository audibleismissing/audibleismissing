import json
from app.app_helpers.rest_handler.methods import get_json_from_api
from app.app_helpers.audimeta.audimeta_helpers import returnBookObj
from typing import Dict, Any, Optional
import requests
from app.custom_objects.book import Book

HEADERS = {
    "User-Agent": "audibleismissing/1.0 (+https://github.com/audibleismissing/audibleismissing)"
}


def getAudimetaSeries(series_asin):
    """Gets series details by series asin"""
    # https://audimeta.de/series/B01M1RDL6W?cache=true&region=us
    url = f"https://audimeta.de/series/book/{series_asin}?cache=true&region=us"

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid JSON response: {e}")


def getAudimetaBook(book_asin: str) -> Optional[Dict[str, Any]]:
    """
    Make an API call to retrieve book details from Audnexus.

    Args:
        book_asin (str): The ASIN of the book to retrieve.

    Returns:
        Optional[Dict[str, Any]]: The JSON response from the API, or None if the request fails.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
        ValueError: If the response is not valid JSON.
    """
    url = f"https://audimeta.de/book/{book_asin}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid JSON response: {e}")


def getAudnexusBookAsBook(book_asin: str) -> Optional[Book]:
    """
    Retrieve book details from Audnexus and return as a Book object.

    Args:
        book_asin (str): The ASIN of the book to retrieve.

    Returns:
        Optional[Book]: The Book object, or None if the request fails.
    """
    json_data = getAudimetaBook(book_asin)
    if json_data:
        return returnBookObj(json_data)
    return None


def getAudimetaBookInSeries(series_asin):
    """Get books in series by series asin"""
    # https://audimeta.de/series/books/B01M1RDL6W?cache=true&region=us

    url = f"https://audimeta.de/series/books/{series_asin}?cache=true&region=us"

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid JSON response: {e}")


def getAudimetaSeriesOfBooksAsBooks(series_asin: str) -> list:
    """Gets a list of books in a series with a given series asin.

    Args:
        series_asin (str): asin of series

    Returns:
        list: List of Book objects.
    """
    json_data = getAudimetaBookInSeries(series_asin)
    if json_data:
        books = []
        for json_book in json_data:
            books.append(returnBookObj(json_book))
        return books
    return []
