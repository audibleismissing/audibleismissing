# Audible is Missing - AI Copilot Instructions

## Project Overview

A FastAPI web application that tracks missing audiobooks in a series by integrating with **Audible**, **Audiobookshelf**, and **Audnexus** APIs. Users can maintain series watch lists and book wish lists.

## Architecture Overview

### Core Services Layer
- **SQLiteService** (`app/services/sqlite.py`): Central database service initialized at app startup via `lifespan()` context manager
- **BackgroundTaskManagerService** (`app/services/task_manager.py`): APScheduler-based background job manager that runs:
  - `job_refresh_book_metadata()`: Syncs Audnexus data nightly
  - `job_refresh_audiobookshelf_data()`: Syncs user's Audiobookshelf library daily at midnight UTC

### API Integration Layer
Each external API has a 3-module pattern:
- `*_api.py`: Main async API client functions
- `*_functions.py`: Business logic using the API
- `*_helpers.py`: Data transformation to custom objects

**Key integrations:**
- **audibleapi**: Uses `audible` library (async) with stored auth file at `config/audible_auth`
- **audiobookshelf**: REST API (async HTTP) - requires URL, API key, library ID in settings
- **audnexus**: Free public API (https://api.audnex.us) for metadata enrichment
- **audimeta**: Free public API (https://audimeta.vercel.app/api) for additional metadata (not currently used)

### Data Model Pipeline
1. **Custom Objects** (`app/custom_objects/*.py`): In-memory domain models (Book, Series, Author, etc.)
2. **Database Tables** (`app/db_models/tables/*.py`): SQLModel ORM definitions linked to custom objects via helpers
3. **Response Models** (`app/response_models/*.py`): FastAPI Pydantic schemas for API responses

**Data flow:** External API → custom object → database table → response model

### Request Handling
- **Pages** (`app/routers/pages/`): REST endpoints for Jinja2 template rendering (HTML)
- **API Routes** (`app/routers/api/*.py`): REST endpoints
- REST Helper (`app/app_helpers/rest_handler/methods.py`): Centralized async HTTP client wrapper

## Critical Workflows

### Development Setup
```bash
git clone <repo>
cd audibleismissing
uv sync                    # Install dependencies (uses uv package manager)
uv run fastapi dev main.py # Start dev server with auto-reload
```

### Docker Development
```bash
./build.sh                 # Spins up dev container with `--watch` mode for hot reload
```

### Database
- Location: `config/audibleismissing.sqlite`
- Import/Export: JSON dump functionality in admin API
- Schema initialized on startup via `SQLiteService.create_tables()`

### Testing Authentication
- Audible auth stored in `config/audible_auth` (loaded by `loadExistingAuth()`)
- Settings file: `config/settings.toml` (created if missing)
- User configures via Settings page (UI) → updates toml file → services read on next job

## Project Conventions

### Settings & Configuration
- Configuration via `config/settings.toml` (TOML format, see `app/custom_objects/settings.py`)
- Environment variables override file paths: `SETTINGS_FILE`, `AUDIBLE_AUTH_FILE`
- Settings are read-once on service startup; changes require manual reload or restart

### Async Patterns
- All API calls are async (`async def` with `await`)
- Use `aiohttp` or `audible.AsyncClient` for HTTP operations
- `BackgroundTaskManagerService` runs jobs in thread pool via APScheduler

### Database Queries
- Use SQLModel `Session` and `select()` with `where()` filters
- Helpers in `app/db_models/tables/helpers.py` convert DB records ↔ custom objects
- Global `db_service` and `background_manager` accessed via dependency injection in routers

### Error Handling
- Custom API classes raise `ValueError` with descriptive messages
- REST helper retries via `tenacity` library
- Audible API has 50-book hard limit per request (handled in `audibleapi_functions.py`)

### Naming Conventions
- Database columns: `snake_case`
- Python classes/functions: `camelCase` for methods, `PascalCase` for classes
- API: singular resource names (e.g., `/api/book`, `/api/series`)

## Key Files to Know

- **[main.py](main.py)**: App initialization, lifespan management, route registration
- **[app/services/sqlite.py](app/services/sqlite.py)**: All database operations
- **[app/services/task_manager.py](app/services/task_manager.py)**: Scheduled sync jobs
- **[app/custom_objects/book.py](app/custom_objects/book.py)**: Core domain model
- **[config/settings.toml](config/settings.toml)**: User credentials & API endpoints
- **[app/routers/api/book_api.py](app/routers/api/book_api.py)**, **[series_api.py](app/routers/api/series_api.py)**: Main API endpoints

## Common Development Tasks

1. **Add a new API field**: Update custom object → add to DB table → add response model field
2. **Fix API sync issue**: Debug in `job_refresh_*` methods in task_manager or specific `*_functions.py`
3. **Modify authentication**: Check `loadExistingAuth()` and settings integration
4. **Add new endpoint**: Create function in routers/api, register in main.py
5. **Update task schedule**: Modify `CronTrigger` in `BackgroundTaskManagerService.start()`

## Dependencies & Versions
- FastAPI 0.121.3+ (with Starlette)
- SQLModel 0.0.27 (SQLAlchemy + Pydantic)
- APScheduler 3.11.1 (background jobs)
- audible 0.10.0 (Audible API client)
- Python 3.14+
