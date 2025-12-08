# https://api.audnex.us/books/{asin}
# https://api.audnex.us/books/B01NBOUV2D

from app.app_helpers.rest_handler.methods import get_json_from_api
from app.app_helpers.audnexus.audnexus_helpers import returnBookObj
from typing import Dict, Any, Optional
from app.custom_objects.book import Book


HEADERS = {
    "User-Agent": "audibleismissing/1.0 (+https://github.com/audibleismissing/audibleismissing)"
}


async def getAudnexusBook(book_asin: str) -> Optional[Dict[str, Any]]:
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
    url = f"https://api.audnex.us/books/{book_asin}"

    try:
        return await get_json_from_api(url, headers=HEADERS, timeout=30)
    except Exception as e:
        raise Exception(f"API request failed: {e}")


async def getAudnexusBookAsBook(book_asin: str) -> Optional[Book]:
    """
    Retrieve book details from Audnexus and return as a Book object.

    Args:
        book_asin (str): The ASIN of the book to retrieve.

    Returns:
        Optional[Book]: The Book object, or None if the request fails.
    """
    json_data = await getAudnexusBook(book_asin)
    if json_data:
        return returnBookObj(json_data)
    return None
