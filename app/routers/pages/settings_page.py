from os.path import dirname, join
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.custom_objects.settings import readSettings, saveSettings
from app.routers.route_tags import Tags
from app.routers.pages import app_router


router = app_router.initRouter()

current_dir = dirname(__file__)
templates_dir = join(current_dir, '../../templates')
templates = Jinja2Templates(directory=templates_dir)


@router.get('/settings', response_class=HTMLResponse, tags=[Tags.page])
def page(request: Request):
    """Render settings page"""

    file = "/config/settings.toml"
    settings = readSettings(file)
    audible_auth = None

    return templates.TemplateResponse(
        request = request, name='settings.html', context={"settings": settings, "audible": audible_auth}
    )
