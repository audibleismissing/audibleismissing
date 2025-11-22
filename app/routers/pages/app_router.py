from fastapi import APIRouter

def initRouter() -> APIRouter:
    """Creates an instance of APIRouter with parameters and returns the object."""
    router = APIRouter(include_in_schema=False)
    return router