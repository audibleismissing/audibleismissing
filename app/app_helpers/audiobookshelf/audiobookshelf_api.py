from typing import Any, Dict

from app.custom_objects.book import Book
from app.app_helpers.rest_handler import methods as rest
from app.app_helpers.audiobookshelf.audiobookshelf_helpers import returnBookObj


def getHeaders(api_key: str):
    HEADERS = {
        "User-Agent": "audibleismissing/1.0 (+https://github.com/audibleismissing/audibleismissing)",
        "accept": "application/json",
        "authorization": api_key,
    }
    return HEADERS


# gets all library items (books)
def getLibraryItems(url, api_key, library_id) -> Dict[str, Any]:
    """Retrieves library items from a specified library API endpoint.

    Parameters:
        url (str): Base URL of the API service.
        api_key (str): Authorization key for API access.
        library_id (str): Unique identifier for the target library.

    Returns:
        Dict[str, Any]: JSON response containing library items.
    """

    url = f"{url}/api/libraries/{library_id}/items"
    headers = getHeaders(api_key)

    try:
        return rest.get_json_from_api(url, headers)
    except ValueError as e:
        raise ValueError(f"getLibraryItems(): {e}")


# gets single library item (book)
def getLibraryItem(url, api_key, item_id) -> Dict[str, Any]:
    """Retrieves a specific library item and converts it to a Book object.

    Parameters:
        url (str): Base URL of the API service.
        api_key (str): Authorization key for API access.
        item_id (str): Unique identifier for the target library item.

    Returns:
        Book: A Book object created from the library item's data.
    """

    url = f"{url}/api/items/{item_id}"
    headers = getHeaders(api_key)

    try:
        book = rest.get_json_from_api(url, headers)
        return returnBookObj(book)
    except ValueError as e:
        raise ValueError(f"getLibraryItem(): {e}")
