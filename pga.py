#!/usr/bin/env python

"""
Scrape the PGA tour's official data endpoint.
"""

import lxml.html as lh
import requests as req


headers = {
    "User-Agent": "Mozilla/5.0 (ESPN) AppleWebKit/535.30 (KHTML, like Gecko)",
    "Referer": "http://www.pgatour.com"
}


def scrape(year):
    """Scrape PGA JSON data for a given year."""
    print year
    url = "http://www.pgatour.com/data/r/stats/{0}/".format(year)
    text = req.get(url, headers=headers).text
    html = lh.fromstring(text)
    links = html.cssselect("td > a")
    for link in links:
        href = link.attrib["href"]
        if href.endswith("json"):
            endpoint = url + href
            print "\t {0}".format(endpoint)
            data = req.get(endpoint, headers=headers).text
            file_name = "data/{0}/{1}".format(year, href)
            with open(file_name, "w") as f:
                f.write(data)


if __name__ == '__main__':
    for year in range(1980, 2012):
        scrape(year)
