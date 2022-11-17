.PHONY: venv README.md output/feed.rss output/history.csv

requirements.txt: requirements.in
	pip-compile requirements.in

venv:
	python -m venv venv
	venv/bin/pip install -r requirements.txt

lint:
	venv/bin/black --check scripts
	venv/bin/isort --check scripts
	venv/bin/flake8 scripts

format:
	venv/bin/black scripts
	venv/bin/isort scripts

README.md:
	cog -r README.md

output/feed.rss:
	venv/bin/python scripts/convert.py $(FEED_URL) > output/feed.rss

output/history.csv:
	venv/bin/python scripts/historify.py output/feed.rss > output/history.csv

ensure-unstaged:
	@git diff --cached --quiet || (echo "Cannot run while files staged" && false)

run-feed: ensure-unstaged output/feed.rss
	git add output/feed.rss
	git diff --cached --quiet || git commit -m "Update feed"

run-history: ensure-unstaged output/history.csv
	git add output/history.csv
	git diff --cached --quiet || git commit -m "Update history"

run: run-feed run-history
