from typing import Any, Dict
import os.path
import asyncio

import audible
import json

from app.custom_objects.book import Book


# get book and return book object
async def getAudibleBook(auth, asin) -> Book:
    from app.app_helpers.audibleapi.audibleapi_helpers import returnBookObj

   
    auth = loadExistingAuth()

    async with audible.AsyncClient(auth) as client:
        item = await client.get(
            f"1.0/catalog/products/{asin}",
            response_groups="product_desc, product_details, series, contributors, rating, category_ladders, relationships, media",
        )
        if item:
            # print(json.dumps(item, indent=4)) # friendly json view
            return returnBookObj(item)
            # return item
    return None


async def getAudibleBooksInSeries(asin) -> Dict[str, Any]:
    from app.app_helpers.audibleapi.audibleapi_helpers import returnListofBookObjs

    auth = loadExistingAuth()

    async with audible.AsyncClient(auth) as client:
        item = await client.get(
            f"/1.0/catalog/products/{asin}/sims",
            response_groups="product_desc, product_details, series, contributors, rating, media",
            similarity_type="InTheSameSeries",
            num_results=50,
        )
        
        if item:
            # print(json.dumps(item, indent=4)) # friendly json view
            # return item
            return returnListofBookObjs(item)
    return None


# create audible device
# If you have activated 2-factor-authentication for your Amazon account, you can append the current OTP to your password. This eliminates the need for a new OTP prompt.
def createDeviceAuth(username, password, country_code, auth_file):
    # Authorize and register in one step
    auth = audible.Authenticator.from_login(
        username, password, locale=country_code, with_username=False
    )

    # Save credentials to file
    auth.to_file(auth_file)


def loadExistingAuth() -> audible.Client:
    from app.custom_objects.settings import readSettings

    config = readSettings()

    if doesAuthExist(config.audible_auth_file):
        return audible.Authenticator.from_file(config.audible_auth_file)
    else:
        print("Run with parameters to create auth.")
    return None


def doesAuthExist(auth_file) -> bool:
    if os.path.isfile(auth_file):
        return True
    return False


# def removeDevice()
#     auth.deregister_device()
