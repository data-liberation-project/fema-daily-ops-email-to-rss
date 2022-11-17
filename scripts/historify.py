import argparse
import csv
import sys
from datetime import datetime

import feedparser
import git


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("feed")
    return parser.parse_args()


# Inspired by https://github.com/simonw/git-history/blob/main/git_history/cli.py
def iterate_file_versions(path, ref="main"):
    repo = git.Repo()
    commits = reversed(list(repo.iter_commits(ref, paths=[path])))
    for commit in commits:
        for leaf in commit.tree.traverse():
            if isinstance(leaf, git.Blob) and leaf.path == path:
                dt, offset = git.objects.util.parse_date(commit.committed_datetime)
                dt_str = datetime.fromtimestamp(dt + offset).isoformat()
                yield commit.hexsha, dt_str, leaf.data_stream


def main():
    args = parse_args()

    writer = csv.writer(sys.stdout)
    writer.writerow(
        ["commit_sha", "commit_dt", "entry_dt", "entry_title", "entry_link"]
    )

    seen = set()

    history = iterate_file_versions(args.feed)
    for sha, dt, blob in history:
        feed = feedparser.parse(blob)
        for entry in feed.entries:
            if entry.id in seen:
                continue

            writer.writerow(
                [
                    sha,
                    dt,
                    datetime(*entry.published_parsed[:6]).isoformat(),
                    entry.title,
                    entry.link,
                ]
            )
            seen.add(entry.id)


if __name__ == "__main__":
    main()
