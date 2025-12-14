import argparse
import hashlib
import re
import sys

import feedparser
import requests
from feedgen.feed import FeedGenerator
from retry import retry

BASE_ID = "data-liberation-project:fema-daily-ops-email-to-rss"
HASH_SALT = "x#$+w3%~o;0~V+e'"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("feed")
    return parser.parse_args()


class NoDocumentWarning(Warning):
    pass


def get_entry_attachment(e):
    pat = r'"(?P<link>http[^"]+?)"[^>]*>(?P<title>[^<]+?)\.pdf'

    match = re.search(pat, e.description)

    if not match:
        raise NoDocumentWarning(f"Cannot find document link in entry {e.title}")

    link, title = match.groups()
    link_head = requests.head(link)
    link_url = link_head.headers["Location"]

    return link_url, title


def convert_entry(e):
    link, title = get_entry_attachment(e)
    hash_payload = f"{e.id}:{HASH_SALT}".encode("utf-8")  # noqa
    new_id = hashlib.sha1(hash_payload).hexdigest()
    return dict(
        id=BASE_ID + ":" + new_id,
        link=dict(link=dict(href=link)),
        title=title,
        published=e.date,
        content=dict(
            content=f'<a link="{link}">{title}</a>',
            type="html",
        ),
    )


def convert_feed(original):
    feed_attrs = dict(
        title="FEMA Daily Operations Briefings",
        id=BASE_ID,
        subtitle=(
            "As received via email, and then converted to RSS "
            "by the Data Liberation Project."
        ),
        author={"name": "FEMA + The Data Liberation Project"},
        language="en",
        link=dict(
            href=(
                "https://github.com/data-liberation-project/"
                "fema-daily-ops-email-to-rss"
            )
        ),
        updated=original.feed.updated,
    )

    fg = FeedGenerator()
    for key, val in feed_attrs.items():
        getattr(fg, key)(val)

    for e in reversed(original.entries):
        try:
            converted = convert_entry(e)
        except NoDocumentWarning as e:
            sys.stderr.write(repr(e) + "\n")
            continue

        new_entry = fg.add_entry()
        for key, val in converted.items():
            method = getattr(new_entry, key)
            if isinstance(val, dict):
                method(**val)
            else:
                method(val)

    return fg


@retry(tries=4, delay=15)
def fetch_feed(url):
    return requests.get(url).content.decode("utf-8")


def main():
    args = parse_args()
    feed_content = fetch_feed(args.feed)
    original = feedparser.parse(feed_content)
    converted = convert_feed(original)
    converted.rss_file(sys.stdout.buffer, pretty=True)


if __name__ == "__main__":
    main()
