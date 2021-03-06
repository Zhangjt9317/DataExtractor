"""
DataExtractor.parser.jsc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is built on top of the chemdataextractor module:
'chemdataextractor.parse.uvvis' as an example for implementaion of the
chemdataextractor pasing syntax.

Parses the short circuit current density

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

class Jsc(BaseModel):
    value = StringType()
    units = StringType()

Compound.jsc_pattern = ListType(ModelType(Jsc))

abbrv_prefix = (I(u'jsc') | I(u'Jsc')).hide()
words_pref = (I(u'short') + I(u'circuit') + I(u'current') + I(u'density')).hide()
hyphanated_pref = (I(u'short') + I(u'-') + I('circuit') + I(u'current') + I(u'density')).hide()

prefix = abbrv_prefix | words_pref | hyphanated_pref

common_text = R('(\w+)?\D(\D+)+(\w+)?').hide()
units = ((W(u'mA') + W(u'/') + W(u'cm') + W('2')) | (W(u'mA') + W(u'/') + W(u'cm') + W('2')))(u'units')
value = R(u'\d+(\.\d+)?')(u'value')

jsc_first= (prefix + ZeroOrMore(common_text) + value + units)(u'jsc')
jsc_second = (value + units + prefix)(u'jsc')

jsc_pattern = jsc_first | jsc_second

class JscParser(BaseParser):
    root = jsc_pattern

    def interpret(self, result, start, end):
        compound = Compound(
            jsc_pattern=[
                Jsc(
                    value=first(result.xpath('./value/text()')),
                    units=first(result.xpath('./units/text()'))
                )
            ]
        )
        yield compound

def parse_jsc(list_of_sentences):
    """ 
    Takes a list of sentences and parses for quantified PCE
    information and relationships to chemicals/chemical labels
    """

    Sentence.parsers.append(JscParser())

    cde_senteces = [Sentence(sent).records.serialize() for sent in list_of_sentences]
    return cde_senteces