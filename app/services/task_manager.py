import asyncio
import logging
from datetime import UTC
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from app.services.sqlite import SQLiteService
from app.custom_objects.settings import readSettings


class BackgroundTaskManagerService:
    """Manager for background tasks."""

    def __init__(self):
        self.scheduler = None
        # self.db_service = SQLiteService() # This will initalize the database
        self.db_service = SQLiteService()
        self.job_stores = {"default": MemoryJobStore()}
        self.job_defaults = {}

        # logging config
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def start(self):
        """Start the background task manager."""
        if not self.scheduler:
            self.scheduler = AsyncIOScheduler(
                jobstores=self.job_stores,
                timezone=UTC,
            )
            self.scheduler.start()

        self.logger.info("Starting background tasks...")

        self.scheduler.add_job(
            self.job_refresh_audiobookshelf_data,
            trigger=CronTrigger(hour=0),
            id="job_refresh_audiobookshelf_data",
            name="Audiobookshelf data refresh daily",
            replace_existing=True,
        )

        self.scheduler.add_job(
            self.job_refresh_book_metadata,
            trigger=CronTrigger(hour=1),
            id="job_refresh_book_metadata",
            name="Metadata refresh",
            replace_existing=True,
        )

        self.scheduler.add_job(
            self.job_check_for_new_books,
            trigger=CronTrigger(hour=2),
            id="job_check_for_new_books",
            name="New book check",
            replace_existing=True,
        )

        self.logger.info(
            "Background task manager started with update checker scheduled"
        )

    async def stop(self):
        """Stop the background task manager."""
        if self.scheduler:
            self.scheduler.shutdown(wait=False)
        self.logger.info("Background task manager stopped")

    async def job_check_for_new_books(self):
        """
        Background task to check for updates to all book series in the database.
        Adds new books if they are available.
        """

        try:
            from app.app_helpers.audibleapi import audibleapi_functions

            self.logger.info("Starting scheduled new book check...")

            await audibleapi_functions.getMissingBooks(self.db_service)

            self.logger.info("New book check completed")

        except Exception as e:
            self.logger.error(f"New book checker failed: {e}")

    async def job_refresh_book_metadata(self):
        """
        Background task to refresh book metadata.
        updates book metadata.
        """

        try:
            from app.app_helpers.audnexus import audnexus_functions

            self.logger.info("Starting scheduled book metadata update...")

            await audnexus_functions.backfillAudnexusBookData(self.db_service)

            self.logger.info("Book metadata update completed")

        except Exception as e:
            self.logger.error(f"Error in book metadata updater: {e}")

    async def job_refresh_audiobookshelf_data(self):
        """
        Background task to get new books from audiobookshelf.
        Reads settings fresh each execution to pick up configuration changes.
        """

        try:
            from app.app_helpers.audiobookshelf.audiobookshelf_functions import (
                refreshAbsData,
            )

            # Read settings fresh each job execution (not cached at startup)
            settings = readSettings()

            self.logger.info("Starting scheduled audiobookshelf data refresh...")

            await refreshAbsData(
                settings.abs_url,
                settings.abs_api_key,
                settings.abs_library_id,
                self.db_service,
            )

            self.logger.info("Audiobookshelf data refresh completed")

        except Exception as e:
            self.logger.error(f"Error in audiobookshelf data refresher: {e}")
