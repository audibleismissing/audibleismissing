from fastapi import APIRouter

def initRouter() -> APIRouter:
    """Creates an instance of APIRouter with parameters and returns the object."""
    router = APIRouter(prefix='/api')
    return router