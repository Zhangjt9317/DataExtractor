"""
DataExtractor.parser.ff
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is built on top of the chemdataextractor module:
'chemdataextractor.parse.uvvis' as an example for implementaion of the
chemdataextractor pasing syntax.

Parses the Fill Factor, similar to PCE parser

"""
import logging
import re

from chemdataextractor.model import Compound, UvvisSpectrum, UvvisPeak, BaseModel, StringType, ListType, ModelType
from chemdataextractor.parse.common import hyphen,lbrct, dt, rbrct
from chemdataextractor.parse.base import BaseParser
from chemdataextractor.utils import first
from chemdataextractor.parse.actions import strip_stop
from chemdataextractor.parse.elements import W, I, T, R, Optional, ZeroOrMore, OneOrMore
from chemdataextractor.parse.cem import chemical_name
from chemdataextractor.doc import Paragraph, Sentence

class Ff(BaseModel):
    value = StringType()
    units = StringType()

Compound.ff_pattern = ListType(ModelType(Ff))

abbrv_prefix = (I(u'FF') | I(u'ff')).hide()
words_pref = (I(u'fill') + I(u'factor')).hide()
prefix = abbrv_prefix | words_pref
# pref = (Optional(lbrct) + W('ff') + Optional(rbrct)).hide()

# fill factor has a unit of % or no unit
common_text = R('(\w+)?\D(\D+)+(\w+)?').hide()
units = (W(u'%') | I(u'percent') | I(u''))(u'units')
value = R(u'\d+(\.\d+)?')(u'value')

ff_first = (words_pref + (Optional(lbrct) + abbrv_prefix + Optional(rbrct)) + ZeroOrMore(common_text) + value + units)(u'ff')
ff_second = (value + units + prefix)(u'ff')
ff_pattern = ff_first | ff_second

class FfParser(BaseParser):
    root = ff_pattern

    def interpret(self, result, start, end):
        compound = Compound(
            ff_pattern=[
                Ff(
                    value=first(result.xpath('./value/text()')),
                    units=first(result.xpath('./units/text()'))
                )
            ]
        )
        yield compound


def parse_ff(list_of_sentences):
    """ 
    Takes a list of sentences and parses for quantified PCE
    information and relationships to chemicals/chemical labels
    """

    Sentence.parsers.append(FfParser())

    cde_senteces = [Sentence(sent).records.serialize()
                    for sent in list_of_sentences]
    return cde_senteces
