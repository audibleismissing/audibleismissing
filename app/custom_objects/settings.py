import toml
import json
import os


settings_file = "config/settings.toml"


class Settings:
    def __init__(self):
        self.settings_file = settings_file
        self.sqlite_path = str
        self.abs_url: str
        self.abs_api_key: str
        self.abs_library_id: str
        self.audible_auth_file: str


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

    # print("Using settings:")
    # print(json.dumps(config, indent=4))

    return getSettingsObj(config)


def getSettingsObj(toml_config) -> Settings:
    settings = Settings()
    settings.sqlite_path = toml_config["database"]["sqlite"]["sqlite_file"]
    settings.abs_url = toml_config["audiobookshelf"]["url"]
    settings.abs_api_key = toml_config["audiobookshelf"]["api_key"]
    settings.abs_library_id = toml_config["audiobookshelf"]["library_id"]
    settings.audible_auth_file = toml_config["audible"]["auth_file"]
    return settings


def createDefaultSettingsFile():
    """Creates a default settings file"""
    config = {
        "database": {
            "sqlite": {
                "sqlite_file": "/config/audibleismissing.sqlite",
            }
        },
        "audiobookshelf": {
            "url": "https://abs.example.com",
            "api_key": "Bearer somekey...",
            "library_id": "id-234234jkjdhfkjdf",
        },
        "audible": {
            "auth_file": "/config/audible_auth",
        },
    }
    with open(settings_file, "w") as file:
        toml.dump(config, file)
