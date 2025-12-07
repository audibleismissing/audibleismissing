import asyncio
import logging
from datetime import datetime, time
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from sqlmodel import Session, select

from app.services.sqlite import SQLiteService


class BackgroundTaskManagerService:
    """Manager for background tasks."""

    def __init__(self, games_directory: Optional[str] = None):
        self.games_directory = games_directory
        self.scheduler = None
        self.db_service = SQLiteService() # This will initalize the database

        # logging config
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    async def start(self):
        """Start the background task manager."""
        if not self.scheduler:
            self.scheduler = AsyncIOScheduler()
            self.scheduler.start()
        
        # # Schedule the update check task to run every hour
        # self.scheduler.add_job(
        #     self.check_for_game_updates,
        #     CronTrigger(day=0),
        #     id='refresh ',
        #     name='Check for game updates every hour',
        #     replace_existing=True
        # )
        
        self.logger.info("Background task manager started with update checker scheduled")
    
    async def stop(self):
        """Stop the background task manager."""
        if self.scheduler:
            self.scheduler.shutdown()
        self.logger.info("Background task manager stopped")
    
    # async def check_for_game_updates(self):
    #     """
    #     Background task to check for updates to all games in the database.
    #     Updates the update_available column for each game.
    #     """
    #     try:
    #         self.logger.info("Starting scheduled game update check...")
            
    #         # Get all games from the database
    #         with Session(self.db_service.engine) as session:
    #             games = session.exec(select(GogGames)).all()
                
    #             if not games:
    #                 self.logger.info("No games found in database")
    #                 return
                
    #             self.logger.info(f"Checking {len(games)} games for updates...")
                
    #             # Check each game for updates
    #             for game in games:
    #                 try:
    #                     has_update = await self.gog_service.check_game_update_available(game.slug)
                        
    #                     # Update the game record if the update status has changed
    #                     if game.update_available != has_update:
    #                         game.update_available = has_update
    #                         session.add(game)
    #                         self.logger.info(f"Updated {game.title}: update_available = {has_update}")
                        
    #                 except Exception as e:
    #                     self.logger.error(f"Error checking update for {game.title}: {e}")
    #                     continue
                
    #             # Commit all changes
    #             session.commit()
                
    #         self.logger.info("Game update check completed")
            
    #     except Exception as e:
    #         self.logger.error(f"Error in game update checker: {e}")