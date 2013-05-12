#!/usr/bin/env python

"""
Scrape historical seasons of the PGA that are only available on Yahoo -- and,
sadly, only have the player's total for a given round.
"""

import os
import re

import lxml.html as lh
import requests as req


headers = {
    "User-Agent": "Mozilla/5.0 (ESPN) AppleWebKit/535.30 (KHTML, like Gecko)",
    "Referer": "http://sports.yahoo.com/golf/pga/schedule"
}


def season(year):
    """Grab a Yahoo golf season's HTML schedule."""
    print year
    url = "http://sports.yahoo.com/golf/pga/schedule?season={0}".format(year)
    text = req.get(url, headers=headers).text
    html = lh.fromstring(text)
    # Grab the schedule
    schedule = html.cssselect("#schedule")
    schedule = lh.tostring(schedule[0])
    file_name = "ysports/{0}.html".format(year)
    with open(file_name, "w") as f:
        print "\t Saved."
        f.write(schedule)


if __name__ == '__main__':
    for year in range(1977, 2001):
        season(year)
