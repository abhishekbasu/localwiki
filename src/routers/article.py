from typing import Annotated

from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.models.article import Article
from src.db.base import Engine, Session, execute_raw_statement, get_db_engine
from src.utils.llm import generate_article
from src.utils.publish import render_markdown

router = APIRouter(
    prefix="/wiki",
)

templates = Jinja2Templates(directory="./src/templates")


@router.get("/search", response_class=HTMLResponse)
async def search_article(
    request: Request,
    q: str,
    engine: Annotated[Engine, Depends(get_db_engine)],
) -> HTMLResponse:
    # sanitize term

    # find k-closest articles in db
    stmt = f"""SELECT title FROM titles_fts WHERE title MATCH '{q}'
    ORDER BY LENGTH(title) ASC, rank DESC;"""
    results = execute_raw_statement(stmt, engine)

    output = []
    for title in results:
        output.append(f"<li><a href='/wiki/{title[0]}'>{title[0]}</a></li>")

    output = "<ul>" + "\n".join(output) + "</ul>"
    return templates.TemplateResponse(
        "article.html",
        {
            "title": f"localwiki: {q}",
            "article": output,
            "request": request,
        },
    )


@router.get("/{title}", response_class=HTMLResponse)
async def get_article(
    request: Request,
    title: str,
    engine: Annotated[Engine, Depends(get_db_engine)],
) -> HTMLResponse:
    article = None
    article_body = "Article not found."

    with Session(engine) as session:
        article = session.get(Article, title)

    if article:
        article_body = article.content
    if not article:
        article_body = generate_article(title)
        db_article = Article(title=title, content=article_body)
        with Session(engine) as session:
            session.add(db_article)
            session.commit()
            session.refresh(db_article)

    return templates.TemplateResponse(
        "article.html",
        {
            "title": f"localwiki: {title}",
            "article": render_markdown(article_body, title=title),
            "request": request,
        },
    )
