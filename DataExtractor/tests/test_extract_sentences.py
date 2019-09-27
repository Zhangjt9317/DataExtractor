# the same test from paper-parser

import chemdataextractor
from paperparser.read_paper import extract_sentences
import os

def test_read_html_paper():
    """
    this is a test function to see if read parser works well
    """
    doc = extract_sentences.read_html_paper(os.path.join(
        os.path.dirname(__file__),
        '../data/journal_articles/paper0.html'
    ))
    
    assert type(doc) == chemdataextractor.doc.Document, \
        'output is not a CDE document type'
        
    return

