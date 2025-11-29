from app.custom_objects.settings import Settings, createDefaultSettingsFile, readSettings
from app.db_models import db_helpers

from os.path import isfile

engine = db_helpers.connectToDb()

# Create default settings.toml if it doesn't exist
config = Settings()
if not isfile(config.settings_file):
    createDefaultSettingsFile()


# create the database
config = readSettings()
if not isfile(config.sqlite_path):
    db_helpers.createTables(engine, config.sqlite_path)