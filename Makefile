.PHONY: venv README.md

requirements.txt: requirements.in
	pip-compile requirements.in

venv:
	python -m venv venv
	venv/bin/pip install -r requirements.txt

run:
	venv/bin/python scripts/convert.py $(FEED_URL) > output/feed.rss
	venv/bin/python scripts/historify.py output/feed.rss > output/history.csv

lint:
	venv/bin/black --check scripts
	venv/bin/isort --check scripts
	venv/bin/flake8 scripts

format:
	venv/bin/black scripts
	venv/bin/isort scripts

README.md:
	cog -r README.md
