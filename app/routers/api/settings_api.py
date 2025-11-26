import toml
from fastapi import Form
from typing import Annotated
from pydantic import BaseModel

from app.routers.api import api_router
from app.routers.route_tags import Tags
from app.app_helpers.audibleapi.auth import createDeviceAuth
from app.custom_objects.settings import readSettings


router = api_router.initRouter()

# Load settings
config = readSettings()
# settings_file = "/config/settings.toml"
# audible_auth_file = "audible_auth"

class SettingsFormModel(BaseModel):
    abs_url: str
    abs_api_key: str
    abs_library_id: str
    model_config = {"extra": "forbid"}


# https://fastapi.tiangolo.com/tutorial/request-forms/
# https://fastapi.tiangolo.com/tutorial/request-form-models/#forbid-extra-form-fields
@router.post("/settings/save/", tags=[Tags.settings])
async def save_settings(data: Annotated[SettingsFormModel, Form()]):
    """Save settings"""
    # Load existing settings
    try:
        with open(config.settings_file, 'r') as f:
            settings = toml.load(f)
    except FileNotFoundError:
        settings = {}

    # Update audiobookshelf section
    if 'audiobookshelf' not in settings:
        settings['audiobookshelf'] = {}
    settings['audiobookshelf']['url'] = data.abs_url
    settings['audiobookshelf']['api_key'] = data.abs_api_key
    settings['audiobookshelf']['library_id'] = data.abs_library_id

    # Save back to file
    with open(config.settings_file, 'w') as f:
        toml.dump(settings, f)

    return {"message": "Settings saved successfully"}


class AudibleAuthFormModel(BaseModel):
    audible_username: str
    audible_password: str
    audible_country_code: str
    model_config = {"extra": "forbid"}

@router.post("/settings/audibleauth/", tags=[Tags.settings])
async def authenticate_to_audible(data: Annotated[AudibleAuthFormModel, Form()]):
    """Authenticate to audible"""
    import os.path

    # if not authenticated, create device auth
    # TODO: add check to see if the token is expired ("expires" key) maybe to doesAuthExist
    if not os.path.isfile(config.audible_auth_file):
        createDeviceAuth(data.audible_username, data.audible_password, data.audible_country_code, config.audible_auth_file)
        return {"message": "Settings saved successfully"}
    
    return {"message": "Auth not created. File exists."}