import toml
import json
import os

# settings_file = os.path.join(os.getcwd(), "config/settings.toml")
# audible_auth_file = os.path.join(os.getcwd(), "config/audible_auth")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))

settings_file = os.environ.get("SETTINGS_FILE", os.path.join(PROJECT_ROOT, "config", "settings.toml"))
audible_auth_file = os.environ.get("AUDIBLE_AUTH_FILE", os.path.join(PROJECT_ROOT, "config", "audible_auth"))


class Settings:
    def __init__(self):
        self.settings_file = settings_file
        self.sqlite_path = str
        self.abs_url: str
        self.abs_api_key: str
        self.abs_library_id: str
        self.audible_auth_file = audible_auth_file


def saveSettings() -> None:
    """Saves settings to toml file"""
    with open(settings_file, "w") as file:
        print("creating DB")
        toml.dump(settings_file, file)


def readSettings() -> toml:
    """Loads settings from toml file and returns a settings object"""
    if os.path.exists(settings_file):
        with open(settings_file) as file:
            config = toml.load(file)
    else:
        createDefaultSettingsFile()
        with open(settings_file) as file:
            config = toml.load(file)

    return getSettingsObj(config)


def getSettingsObj(toml_config) -> Settings:
    settings = Settings()
    settings.abs_url = toml_config["audiobookshelf"]["url"]
    settings.abs_api_key = toml_config["audiobookshelf"]["api_key"]
    settings.abs_library_id = toml_config["audiobookshelf"]["library_id"]
    settings.audible_auth_file = audible_auth_file
    return settings


def createDefaultSettingsFile():
    """Creates a default settings file"""
    config = {
        "audiobookshelf": {
            "url": "https://abs.example.com",
            "api_key": "Bearer somekey...",
            "library_id": "id-234234jkjdhfkjdf",
        },
    }
    with open(settings_file, "w") as file:
        toml.dump(config, file)
