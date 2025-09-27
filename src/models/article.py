"""All transactions related are defined here."""

from typing import (
    Annotated,
)

from sqlmodel import (
    Field,
    SQLModel,
)

ARTICLESTABLE = "articles"


class Article(SQLModel, table=True):
    __tablename__ = ARTICLESTABLE  # type: ignore

    title: Annotated[
        str,
        Field(
            description="Represents the title of a legitimate Wikipedia article.",
            primary_key=True,
        ),
    ]
    content: Annotated[str, Field(description="The full content of the article.")]
