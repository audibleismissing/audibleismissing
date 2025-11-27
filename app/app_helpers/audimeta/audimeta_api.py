from app.app_helpers.rest_handler.methods import get_json_from_api


def getAudimetaBook(book_asin: str):
    """Get book details by book asin"""
    # https://audimeta.de/book/B01L082HJ2?cache=true&region=us

    url = f"https://audimeta.de/book/{book_asin}?cache=true&region=us"
    headers = {
        "accept": "application/json",
    }

    try:
        json_data = get_json_from_api(url, headers)
        return json_data
    except ValueError as e:
        raise ValueError(f"getLibraryItems(): {e}")


def getAudimetaBookInSeries(series_asin):
    """Get books in series by series asin"""
    # https://audimeta.de/series/books/B01M1RDL6W?cache=true&region=us
    url = f"https://audimeta.de/series/book/{series_asin}?cache=true&region=us"
    headers = {
        "accept": "application/json",
    }

    try:
        json_data = get_json_from_api(url, headers)
        return json_data
    except ValueError as e:
        raise ValueError(f"getLibraryItems(): {e}")


def getAudimetaSeries(series_asin):
    """Gets series details by series asin"""
    # https://audimeta.de/series/B01M1RDL6W?cache=true&region=us
    url = f"https://audimeta.de/series/book/{series_asin}?cache=true&region=us"
    headers = {
        "accept": "application/json",
    }

    try:
        json_data = get_json_from_api(url, headers)
        return json_data
    except ValueError as e:
        raise ValueError(f"getLibraryItems(): {e}")