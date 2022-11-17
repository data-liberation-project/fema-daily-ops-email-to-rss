# FEMA Daily Operations Briefing: Converting Email → RSS (→ CSV)

## Introduction

Every day, the US [Federal Emergency Management Agency](https://www.fema.gov/) (FEMA) compiles a PDF report they call the "Daily Operations Briefing."

To the Data Liberation Project's best knowledge, FEMA does not publish these briefings anywhere online. You can, however, [subscribe](https://public.govdelivery.com/accounts/USDHSFEMA/subscriber/new) to receive a link to each day's briefing. (You can also [find past briefings at disastercenter.com](https://disastercenter.com/FEMA%20Daily%20Situation%20Report%20Archive%202022.html), which has been collecting the reports for many years.)

The lack of an official, public-facing source for FEMA reports provides the motivation for this repository, which is the first step in what will be a more comprehensive processing pipeline.

## Step 1: Collect Briefing Emails Into a Private RSS Feed

Using the service [kill-the-newsletter.com](https://kill-the-newsletter.com/), the Data Liberation Project has subscribed to FEMA's Daily Operations Briefing emails. The service receives each email and makes its contents available as a private RSS feed.

That feed's address, however, must remain private; if it were public, someone could unsubscribe it from the newsletter and/or send spam to the inbox. So...

## Step 2: Convert Private RSS Feed Into Public RSS Feed

To make the information in the inbox publicly acessible without compromising the inbox itself, the [`scripts/convert.py`](scripts/convert.py) Python script does the following:

- Fetches the private RSS feed.
- Extracts the necessary, non-private information: the time the email was received, the name of the PDF, and a link to the PDF file.
- Rrites a new, reformatted RSS feed, which is available as [`output/feed.rss`](output/feed.rss).

## Step 3: Record RSS History as a CSV File

The (public and private) RSS feeds only contain the most recent 42 entries. The [`scripts/historify.py`](scripts/historify.py) script iterates through this git/GitHub repository's history and generates a file of all unique entries, which is available as [`output/history.csv`](output/history.csv).

## Licensing

The code in this repository is available under the [MIT License](https://choosealicense.com/licenses/mit/); the output files are available under the [CC0 license](https://creativecommons.org/share-your-work/public-domain/cc0/).

## Questions?

Email Jeremy Singer-Vine at `jsvine@gmail.com`. 
