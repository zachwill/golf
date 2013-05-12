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
    "Referer": "http://espn.go.com/golf"
}


def season(year):
    """Save an ESPN PGA season's HTML."""
    print year
    url = "http://espn.go.com/golf/schedule/_/year/{0}".format(year)
    text = req.get(url, headers=headers).text
    html = lh.fromstring(text)
    # Extract just the content <div>
    content = html.cssselect(".mod-table")
    content = lh.tostring(content[0])
    # Save it to disk
    file_name = "html/{0}.html".format(year)
    with open(file_name, "w") as f:
        print "\t Saved."
        f.write(content)


def find_tournaments(year=None):
    """
    A semi-convoluted way of parsing the saved HTML seasons and then scraping
    the tourneys.
    """
    html_files = []
    if not year:
        for file_name in os.listdir('html'):
            file_name = "html/{0}".format(file_name)
            if not os.path.isfile(file_name):
                continue
            html_files.append(file_name)
    else:
        file_name = "html/{0}.html".format(year)
        html_files.append(file_name)
    for file_name in html_files:
        with open(file_name) as f:
            html = lh.fromstring(f.read())
        tournament_links(html)


def tournament_links(html):
    """Find links for tournaments in a season's HTML."""
    links = html.cssselect("tr td > a")
    for link in links:
        href = link.attrib['href']
        if not href.startswith('/'):
            continue
        scrape_tournament(href)


def scrape_tournament(endpoint):
    """Scrape a tournament's HTML content."""
    # Find the tournament ID
    match = re.search(r'\d+', endpoint)
    tournament = match.group(0)
    url = "http://espn.go.com{0}".format(endpoint)
    print url
    # Scrape the tournament
    text = req.get(url, headers=headers).text
    html = lh.fromstring(text)
    content = html.cssselect("#content")
    content = lh.tostring(content[0])
    # Save it to disk
    file_name = "html/tournaments/{0}.html".format(tournament)
    with open(file_name, "w") as f:
        print "\t Saved."
        f.write(content)


def main():
    #for year in range(2001, 2013):
        #season(year)
    find_tournaments()


if __name__ == '__main__':
    main()
