PYTHON := uv run

.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo "  install     Install project dependencies"
	@echo "  serve-dev   Run the app in dev mode"
	@echo "  first-run   Initialize the database and download the wiki index"
	@echo "  clean       Remove the SQLite database file"

install:
	brew install ollama wget uv
	brew services start ollama
	ollama pull gpt-oss:20b
	wget -q https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-all-titles-in-ns0.gz -P ./wiki-index/

first-run: clean
	$(PYTHON) ./src/run_first.py

serve:
	$(PYTHON) uvicorn src.main:app --host 127.0.0.1 --port 8000

clean:
	rm wiki.db 2> /dev/null