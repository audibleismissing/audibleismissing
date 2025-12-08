from app.custom_objects.settings import (
    Settings,
    createDefaultSettingsFile,
)

from os.path import isfile

# Create default settings.toml if it doesn't exist
config = Settings()
if not isfile(config.settings_file):
    createDefaultSettingsFile()
