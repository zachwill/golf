#!/usr/bin/env python

"""
Scrape each season of the PGA.
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
    """Grab a Yahoo golf season's html."""
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
