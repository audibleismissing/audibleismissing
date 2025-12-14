# Audible is Missing - AI Copilot Instructions

## Project Overview
FastAPI web app tracking missing audiobooks across series. Users maintain watch lists (series) and wish lists (books) while integrating with Audible, Audiobookshelf, and Audnexus for metadata and library sync.

## Architecture Essentials

### Service Layer (Initialized at Startup)
- **SQLiteService** (`app/services/sqlite.py`): Manages SQLite DB at `config/audibleismissing.sqlite`, initialized in `lifespan()` context manager
- **BackgroundTaskManagerService** (`app/services/task_manager.py`): APScheduler running 3 daily jobs:
  - **0:00 UTC**: `job_refresh_audiobookshelf_data()` - syncs Audiobookshelf library
  - **1:00 UTC**: `job_refresh_book_metadata()` - enriches books with Audnexus data
  - **2:00 UTC**: `job_check_for_new_books()` - checks series for new releases

### Data Flow: API → Custom Object → DB → Response
1. **`app/custom_objects/*.py`**: Plain Python classes (Book, Series, Author, etc.) - in-memory domain models
2. **`app/db_models/tables/*.py`**: SQLModel ORM with helpers in `helpers.py` converting custom objects ↔ DB rows
3. **`app/response_models/*.py`**: Pydantic schemas for FastAPI responses
4. **`app/routers/api/*.py`**: Endpoints grouped by resource (book_api, series_api, etc.)

Each external API uses 3-module pattern: `*_api.py` (client) → `*_functions.py` (logic) → `*_helpers.py` (custom objects)

### External Integrations
- **audibleapi**: Uses `audible` library (Python async client) with auth file `config/audible_auth`
- **audiobookshelf**: REST API requiring URL, API key, library ID from `config/settings.toml`
- **audnexus** & **audimeta**: Free public APIs for metadata; retry logic via `tenacity` in REST helper

## Development Setup
```bash
uv sync                    # Install dependencies (uses uv package manager)
uv run fastapi dev main.py # Dev server with hot reload on port 8000
./build.sh                 # Docker dev container with volume mount (Dockerfile-dev)
```

## Configuration & Environment

**Settings flow:** `config/settings.toml` (TOML) → `app/custom_objects/settings.py` → `readSettings()` reads fresh on each background job  
**Env var overrides:** `SETTINGS_FILE`, `AUDIBLE_AUTH_FILE`, `ALLOWED_ORIGINS` (default: `http://localhost:8000`)  
**Auto-init:** Missing `settings.toml` triggers `createDefaultSettingsFile()` on first `readSettings()` call

## Patterns & Conventions

**Database Access:**
- Use SQLModel `Session` with `select()` + `where()`/`and_()` filters
- Dependency injection: routers call `get_db_service()` / `get_background_manager()` functions
- Complex reads use SQL views: `booksandseries` and `seriesandcounts` in `app/db_models/views/`

**Async:** All API calls async with `aiohttp`/`audible.AsyncClient`; background jobs run in thread pool  

**Adding a field:** Update custom object → DB table + helper converters → response model  

**API errors:** Raise `ValueError` with messages; REST helper catches and retries failed requests  

**Naming:** `snake_case` columns/files, `camelCase` methods, `PascalCase` classes  

## Key Files
- [main.py](main.py): Lifespan setup, service init, route registration
- [app/services/sqlite.py](app/services/sqlite.py): DB ops, table creation
- [app/services/task_manager.py](app/services/task_manager.py): Scheduled jobs
- [app/custom_objects/settings.py](app/custom_objects/settings.py): Config management
- [app/app_helpers/rest_handler/methods.py](app/app_helpers/rest_handler/methods.py): HTTP client wrapper

## Dependencies
Python 3.14+, FastAPI 0.121.3+, SQLModel 0.0.27, APScheduler 3.11.1, audible 0.10.0, aiohttp, tenacity
