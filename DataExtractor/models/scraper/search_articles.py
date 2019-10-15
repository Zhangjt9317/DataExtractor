"""
DataExtractor.scraper.search_articles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import json
import urllib
import requests

import pymongo
from pymongo import MongoClient
import sys
import glob
import os

# This class aims at scraping down articles for tests and store in local drive
class search_and_pull:

    def __init__(self):
        # these three major platforms currently support full-text mining
        self.els_key = "4bc84cbdadca6050062348015ac963aa"
        self.spn_key = "eca22bc7a0b1ee3153ab02c024a6a06e"
        self.rsc_key = "rCv9bcgMfuUyvCXAG1vtZFUL0sTyuxjL"
        self.rsc_secret = "aoCLYeFC4IInwBnX"

        self.file = "testing_download_articles/write_test_els_paper2.json"
        self.folder = "testing_download_articles/"

        # key words that can be taken as query
        # this will make the search results more focused
        self.key_words = [
            'organic photovoltaics',
            'organic solar cell',
            'thin film solar cell',
            'π‑Conjugated polymer',
            'fullerene-based'
        ]

    # define search articles using API
    def search_articles(self, file):
        """
        This is the combination of search and full text retrieval API
        input : JSON file location
        """
        names = []
        dois = []

        # read json as dictionary in python
        file = self.file
        with open(file) as f:
            data = json.load(f)

        for i in data['search-results']['entry']:
            if 'prism:doi' in i:
                dois.append(i['prism:doi'])
                names.append(i['dc:title'])
        return dois

    # define full article retrieval using API
    def pull_articles(self, ls):
        """
        This function writes txt files for scraped documents
        """
        # pull articles
        doi = self.search_articles(file)
        els_key = self.els_key

        for i in doi:
            els_url = 'https://api.elsevier.com/content/article/doi/' + doi + '?APIKey=' + els_key
            r = requests.get(els_url)
            for num in range(len(ls)):
                with open(folder + f'/write_test_els_paper{num}.xml', 'wb') as file:
                    file.write(r.content)


# connecting to the mongodb and save the scraped results
path = '../test_articles/'
os.chdir(path)

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['OPVDB']

articles = db.articles
article_data = {
    'title': "file",
    'content': "document",
    'author': 'Sam'
}

