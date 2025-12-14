VENV_DIR ?= venv
.PHONY: venv output/feed.rss output/history.csv

requirements.txt: requirements.in
	pip-compile requirements.in

venv:
	python -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

lint:
	$(VENV_DIR)/bin/black --check scripts
	$(VENV_DIR)/bin/isort --check scripts
	$(VENV_DIR)/bin/flake8 scripts

format:
	$(VENV_DIR)/bin/black scripts
	$(VENV_DIR)/bin/isort scripts

output/feed.rss:
	$(VENV_DIR)/bin/python scripts/convert.py $(FEED_URL) > output/feed.rss

output/history.csv:
	$(VENV_DIR)/bin/python scripts/historify.py output/feed.rss > output/history.csv

ensure-unstaged:
	@git diff --cached --quiet || (echo "Cannot run while files staged" && false)

run-feed: ensure-unstaged output/feed.rss
	git add output/feed.rss
	git diff --cached --quiet || git commit -m "Update feed"

run-history: ensure-unstaged output/history.csv
	git add output/history.csv
	git diff --cached --quiet || git commit -m "Update history"

run: run-feed run-history
