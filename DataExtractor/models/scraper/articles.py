"""
DataExtractor.scraper.articles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is built on urllib and feedparser

Scraping down articles with specific scope or search query for parsers to process
Supported platforms include Elsevier, Springer, ACS, RSC


RSC only supports compounds API, so not all content related to the topic can be searched
"""

import re
import time
import os
import logging
import urllib
import feedparser
import unittest
import pandas as pd


def scrape(platform, scope, search_term, start, count):
    """
    This function is used to scrape articles from platforms
    :platform Elsvier-Scopus, Elsvier-ScienceDirect
    :apikey normal API key
    :doi digital object identifier
    : author author of the literature
    """

    search_term = search_term.replace('"', "%22").replace(" ", "+")
    # set wait time and iteration step
    wait_time = 2
    date_dict = {
        "date": [],
        "article_id": [],
        "summary": [],
        "source": platform
    }
    
    # Elsevier
    # Scopus, ScienceDirect, etc.
    if platform == "Elsvier":
        apiKey = "4bc84cbdadca6050062348015ac963aa"
        # scopus hosts abstracts and citation statistics
        # sicencedirect hosts full articles, so we use sciencedirect here 
        url = "https://api.elsevier.com/content/search/sciencedirect?query={scope}:{search_term}&count={count}&start={start}&apiKey={apiKey}&sortBy=submittedDate&sortOrder=ascending&start={start}&max_results={count}"

    # Springer Nature
    elif platform == "Springer":
        apiKey = "eca22bc7a0b1ee3153ab02c024a6a06e"
        url = "http://api.springernature.com/openaccess/JSON?api_key={apiKey}&q={scope}:{search_term}&s={start}&p={count}"

    # American Chemical Society
    # ACS uses CAS portal to export
    elif platform == "ACS":
        # ACS has CAS system
        url = ""

    # arXiv e-prints
    elif platform == "arXiv":
        # arXiv doesn't have API keys
        url = "http://export.arxiv.org/api/query?search_query={scope}:{search_term}&sortBy=submittedDate&sortOrder=ascending&start={start}&max_results={count}"

    # Royal Society of Chemistry
    elif platform == "RSC":
        consumer_key = "rCv9bcgMfuUyvCXAG1vtZFUL0sTyuxjL"
        secret_key = "aoCLYeFC4IInwBnX"
        url = ""

    while True:
        response = urllib.request.urlopen(url)
        feed = feedparser.parse(response)
        if not feed.entries:
            print('query complete')
            print(f"There should be {feed.feed.opensearch_totalresults} results?")
            break
        date_dict['date'].extend([entry.published for entry in feed.entries])
        date_dict['article_id'].extend(
            [entry.id.split('/abs/')[-1] for entry in feed.entries])
        date_dict['summary'].extend(
            [entry.summary.replace("\n", " ") for entry in feed.entries])
        print(f"gathering results {start} to {start + count-1} ")
        start = start + count
        time.sleep(wait_time)

    return pd.DataFrame(date_dict)
