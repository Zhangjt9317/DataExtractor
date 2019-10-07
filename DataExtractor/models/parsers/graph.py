"""
DataExtractor.parsers.graph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is built on top of chemdataextractor module:
'chemdataextractor.parse.uvvis' as an example for implementation of the 
chemdataextractor parsing syntax.

Parses chemical graphs, workflows, reaction processes, etc. from literature
and convert materials into SMILES using OSRA

"""

import logging 
import re

from chemdataextractor.model import Compound, UvvisSpectrum, UvvisPeak, BaseModel, StringType, ListType, ModelType
from chemdataextractor.parse.common import hyphen
from chemdataextractor.parse.base import BaseParser
from chemdataextractor.utils import first
from chemdataextractor.parse.actions import strip_stop
from chemdataextractor.parse.elements import W, I, T, R, Optional, ZeroOrMore, OneOrMore
from chemdataextractor.parse.cem import chemical_name
from chemdataextractor.doc import Paragraph, Sentence

 # in html images are shown in <img> tag, in pdf, not sure, in xml shown as GraphXML format
def graph(para):
    # 