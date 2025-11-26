import toml
from fastapi import Form
from typing import Annotated
from pydantic import BaseModel

from app.routers.api import api_router
from app.routers.route_tags import Tags


router = api_router.initRouter()

file = "settings.toml"

class SettingsFormModel(BaseModel):
    abs_url: str
    abs_api_key: str
    abs_library_id: str
    model_config = {"extra": "forbid"}


# https://fastapi.tiangolo.com/tutorial/request-forms/
# https://fastapi.tiangolo.com/tutorial/request-form-models/#forbid-extra-form-fields
@router.post("/settings/save/", tags=[Tags.settings])
async def save_settings(data: Annotated[SettingsFormModel, Form()]):
    # Load existing settings
    try:
        with open(file, 'r') as f:
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
    with open(file, 'w') as f:
        toml.dump(settings, f)

    return {"message": "Settings saved successfully"}