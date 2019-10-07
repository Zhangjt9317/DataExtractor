"""
DataExtractor.parsers.tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For table extraction 

Searhces for tables and extract property information from them. 
"""

import chemdataextractor as cde 
from chemdataextractor.doc import Paragraph
from chemdataextractor.parse import table

def find_tables(paras):
    ls = []
    length = len(paras)
    for i in range(length):
        if str(paras[i]).startswith("Table"):
            ls.append(i)
    return ls

def tables(paras):
    """
    This function is used to find tables and containing property or experimental information inside
    them. 
    """

    # find paras where tables are stored
    ls = find_tables(paras)
    