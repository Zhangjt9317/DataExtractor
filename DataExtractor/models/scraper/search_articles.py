import json
import urllib
import requests

class search_and_pull:
    """
    One search api and one full article retrieval api
    
    """
    def __init__(self):
        self.els_key = "4bc84cbdadca6050062348015ac963aa"
        self.file = "testing_download_articles/write_test_els_paper2.json"
        self.folder = "testing_download_articles/"
        
    def search_articles(self,file):
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

    def pull_articles(self,ls):
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