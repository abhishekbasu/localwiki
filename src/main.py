from fastapi import (
    FastAPI,
    Request,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.db.base import create_tables
from src.routers.article import router as article_router
from src.routers.root import router as root_router

# CORS allowed origins
cors_allowed_origins = []

app = FastAPI(
    title="localwiki",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


app.include_router(root_router)
app.include_router(article_router)

create_tables()
