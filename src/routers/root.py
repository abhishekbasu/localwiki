from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="",
)

templates = Jinja2Templates(directory="./src/templates")


@router.get("/", response_class=HTMLResponse)
async def get_landing(request: Request) -> HTMLResponse:
    landing = "<h1>localwiki</h1><p>Your local wiki powered by LLMs.</p>"
    return templates.TemplateResponse(
        "article.html",
        {"title": "localwiki", "article": landing, "request": request},
    )
