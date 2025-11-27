from app.app_helpers.rest_handler.methods import get_json_from_api


def getAudimetaBook(book_asin: str):
    """Get book details by book asin"""
    # https://audimeta.de/book/B01L082HJ2?cache=true&region=us

    url = f"https://audimeta.de/book/{book_asin}"
    # headers = {
    #     "accept": "application/json",
    # }
    # params = {
    #     "cache": "true",
    #     "region": "us"
    # }

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid JSON response: {e}")


def getAudimetaBookInSeries(series_asin):
    """Get books in series by series asin"""
    # https://audimeta.de/series/books/B01M1RDL6W?cache=true&region=us
    url = f"https://audimeta.de/series/book/{series_asin}?cache=true&region=us"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid JSON response: {e}")


def getAudimetaSeries(series_asin):
    """Gets series details by series asin"""
    # https://audimeta.de/series/B01M1RDL6W?cache=true&region=us
    url = f"https://audimeta.de/series/book/{series_asin}?cache=true&region=us"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid JSON response: {e}")
    



import requests
from typing import Dict, Any, Optional

def get_audimeta_book(book_asin: str) -> Optional[Dict[str, Any]]:
    """
    Make an API call to retrieve book details from Audimeta.

    Args:
        book_asin (str): The ASIN of the book to retrieve.

    Returns:
        Optional[Dict[str, Any]]: The JSON response from the API, or None if the request fails.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
        ValueError: If the response is not valid JSON.
    """
    url = f"https://audimeta.de/book/{book_asin}"
    headers = {
        "accept": "application/json",
    }
    params = {
        "cache": "true",
        "region": "us"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid JSON response: {e}")
