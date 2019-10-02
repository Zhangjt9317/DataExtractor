"""
DataExtractor.parsers.tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For table extraction 

Searhces for tables and extract property information from them. 
"""

import chemdataextractor as cde 
from chemdataextractor.doc import Paragraph
from chemdataextractor.parse import table

def tables(para):
    """
    This function is used to find tables and containing property or experimental information inside
    them. 
    """
    
