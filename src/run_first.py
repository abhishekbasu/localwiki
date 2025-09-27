import gzip
from tqdm import tqdm

from pathlib import Path
import sqlalchemy
from sqlalchemy.exc import IntegrityError


DBNAME = "wiki.db"
WIKI_INDEX = "enwiki-latest-all-titles-in-ns0.gz"


# create sqlite db first
def get_connection():
    engine = sqlalchemy.create_engine(f"sqlite:///{DBNAME}")
    connection = engine.connect()
    return connection


def check_index_exists():
    indexfile = Path(f"./wiki-index/{WIKI_INDEX}")
    assert indexfile.exists(), "Index file not found!"


def create_tables(connection, indexfile):
    # create a table for titles
    connection.execute(
        sqlalchemy.text(
            """CREATE TABLE IF NOT EXISTS titles (
                title TEXT PRIMARY KEY
            );"""
        )
    )
    connection.commit()

    with gzip.open(indexfile, "rt", encoding="utf-8") as f:
        num_lines = sum(1 for _ in f)

    pbar = tqdm(total=num_lines, desc="Building titles table...")
    with gzip.open(indexfile, "rt", encoding="utf-8") as f:
        for i, title in enumerate(f):
            pbar.update(1)
            title = title.strip().replace("_", " ").replace('"', "").lower()
            title = "".join([i for i in title if i.isalnum() or i.isspace()]).strip()
            if (
                not title
                or not title[0].isalpha()
                or len(title) > 50
                or len(title.split(" ")) > 4
            ):
                continue
            try:
                connection.execute(
                    sqlalchemy.text("INSERT INTO titles (title) VALUES (:title)"),
                    {"title": title},
                )
            except IntegrityError:
                continue

    pbar.close()
    print("Creating FTS index...")
    connection.commit()
    connection.execute(
        sqlalchemy.text(
            """CREATE VIRTUAL TABLE titles_fts USING
            fts5(title, tokenize=porter);"""
        )
    )
    connection.commit()
    connection.execute(
        sqlalchemy.text("""INSERT INTO titles_fts SELECT * FROM titles;""")
    )
    connection.commit()

    print("Creating articles cache...")
    connection.execute(
        sqlalchemy.text(
            """CREATE TABLE IF NOT EXISTS articles (
                title TEXT PRIMARY KEY
                , content TEXT
            );"""
        )
    )
    connection.commit()
    connection.close()


if __name__ == "__main__":
    check_index_exists()
    conn = get_connection()
    create_tables(conn, f"./wiki-index/{WIKI_INDEX}")
