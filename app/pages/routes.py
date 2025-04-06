from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/pages", tags=["Front"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_pages(
    request: Request
):
    return templates.TemplalsteResponse(name="hotels.html", context={"request": request})