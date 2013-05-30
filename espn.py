#!/usr/bin/env python

"""
Scrape each season of the PGA from ESPN.
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
    # Create the tournaments directory, if necessary
    disk_path = "html/tournaments"
    if not os.path.exists(disk_path):
        os.makedirs(disk_path)
    # Save it to disk
    file_name = "html/tournaments/{0}.html".format(tournament)
    with open(file_name, "w") as f:
        print "\t Saved."
        f.write(content)


def saved_tournaments():
    """Return the saved tournaments HTML files."""
    html_files = []
    for file_name in os.listdir('html/tournaments'):
        file_name = "html/tournaments/{0}".format(file_name)
        if not os.path.isfile(file_name):
            continue
        html_files.append(file_name)
    return html_files


def find_players(tournament=None):
    """
    Parse the players from saved tournament HTML files. Then, scrape their
    strokes for the given tournament.
    """
    if not tournament:
        html_files = saved_tournaments()
    else:
        html_files = ["html/tournaments/{0}.html".format(tournament)]
    for file_name in html_files:
        with open(file_name) as f:
            html = lh.fromstring(f.read())
        match = re.search(r'(\d+)', file_name)
        tournament = match.group(0)
        players = html.cssselect('.player a')
        for player in players:
            player_id = player.attrib['name']
            scrape_strokes(player_id, tournament)


def scrape_strokes(player, tournament):
    """Find a player's HTML strokes by round for a given tournament."""
    disk_path = "html/strokes/{0}".format(tournament)
    file_name = disk_path + "/{0}.html".format(player)
    if not os.path.exists(disk_path):
        os.makedirs(disk_path)
    if not os.path.isfile(file_name):
        print tournament, player
        url = ("http://espn.go.com/golf/leaderboard11/controllers/ajax/playerDropdown?"
               "xhr=1&playerId={0}&tournamentId={1}").format(player, tournament)
        html = req.get(url, headers=headers).text
        with open(file_name, "w") as f:
            f.write(html)


def main():
    #for year in range(2001, 2013):
        #season(year)
    #find_tournaments()
    find_players()


if __name__ == '__main__':
    main()
