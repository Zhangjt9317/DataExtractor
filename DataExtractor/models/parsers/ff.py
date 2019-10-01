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
from chemdataextractor.parse.common import hyphen
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

abbrv_prefix = (I(u'FF') | I(u'FFs') | I(u'ff')).hide()
words_pref = (I(u'fill') + I(u'factor')).hide()
hyphanated_pref = (I(u'power-conversion') + I(u'efficiency')).hide()
prefix = abbrv_prefix | words_pref | hyphanated_pref

common_text = R('(\w+)?\D(\D+)+(\w+)?').hide()
units = (W(u'%') | I(u'percent'))(u'units')
value = R(u'\d+(\.\d+)?')(u'value')

ff_first = (prefix + ZeroOrMore(common_text) + value + units)(u'ff')
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
    """ Takes a list of sentences and parses for quantified PCE
        information and relationships to chemicals/chemical labels
        """

    Sentence.parsers.append(FfParser())

    cde_senteces = [Sentence(sent).records.serialize()
                    for sent in list_of_sentences]
    return cde_senteces
