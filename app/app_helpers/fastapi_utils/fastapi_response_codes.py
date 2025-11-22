from fastapi import HTTPException


def notFound():
    raise HTTPException(
        status_code=404,
        detail="No results",
        headers={"X-Error": "No results found from query."},
    )