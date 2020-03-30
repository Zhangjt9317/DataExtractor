def pull_articles(ls):
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