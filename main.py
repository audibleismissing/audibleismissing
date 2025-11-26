from os.path import dirname, join, isfile
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.pages import index, series, books, settings_page
from app.routers.api import book_api, series_api, admin_api, test_api, settings_api

from fastapi.staticfiles import StaticFiles


# initialize FastAPI app
app = FastAPI(
    title="Audible is Missing API",
    summary="Interact with audibleismissing backend.",
    description="""
    fill this out later
    """,
)


origins = [
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# setup static directory for web files
current_dir = dirname(__file__)
static_dir = join(current_dir, 'app/static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")



# site routers
app.include_router(index.router)
app.include_router(series.router)
app.include_router(books.router)
app.include_router(settings_page.router)


# api routers
app.include_router(book_api.router)
app.include_router(series_api.router)
app.include_router(admin_api.router)
app.include_router(test_api.router)
app.include_router(settings_api.router)