from typing import Any, Dict

import audible
import json

from app.custom_objects.book import Book


# get book and return book object
def getAudibleBook(auth, asin) -> Book:
    from app.app_helpers.audibleapi.helpers import returnBookObj
    
    with audible.Client(auth) as client:
        item = client.get(
            f"1.0/catalog/products/{asin}",
            response_groups="product_desc, product_details, series, contributors, rating, category_ladders, relationships, media"
        )
        if item:
            # print(json.dumps(item, indent=4)) # friendly json view
            # return returnBookObj(item)
            return item
    return None


def getAudibleBooksInSeries(auth, asin) -> Dict[str, Any]:
    with audible.Client(auth) as client:
        item = client.get(
            f"/1.0/catalog/products/{asin}/sims",
            response_groups="product_desc, product_details, series, contributors, rating, media",
            similarity_type="InTheSameSeries",
            num_results=50
        )
        if item:
            # print(json.dumps(item, indent=4)) # friendly json view
            return item
    return None