"""
DataExtractor.parser.voc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is built on top of the chemdataextractor module:
'chemdataextractor.parse.uvvis' as an example for implementaion of the
chemdataextractor pasing syntax.

Parses the open circuit voltage

"""
import logging
import re

from chemdataextractor.model import Compound, UvvisSpectrum, UvvisPeak, BaseModel, StringType, ListType, ModelType
from chemdataextractor.parse.common import hyphen, lbrct, dt, rbrct
from chemdataextractor.parse.base import BaseParser
from chemdataextractor.utils import first
from chemdataextractor.parse.actions import strip_stop, merge, join
from chemdataextractor.parse.elements import W, I, T, R, Optional, ZeroOrMore, OneOrMore, Not, Any
from chemdataextractor.parse.cem import chemical_name
from chemdataextractor.doc import Paragraph, Sentence


class Voc(BaseModel):
    value = StringType()
    units = StringType()

# All hyphen and minus characters. Probably more robust than the hyph POS tag.
hyphen = R('^[\-‐‑⁃‒–—―−－⁻]$')

# All quote and apostrophe characters
quote = R('^[\'’՚Ꞌꞌ＇‘’‚‛"“”„‟`´’‘]$')

slash = W('/')

Compound.voc_pattern = ListType(ModelType(Voc))

abbrv_prefix = (I(u'VOC') | I(u'voc') | I(u'Voc')).hide()
words_pref = (I(u'open') + I(u'circuit') + I(u'voltage')).hide()
hyphanated_pref = (I(u'open') + hyphen + I('circuit') + I(u'voltage')).hide()

joined_range = R(
    '^[\+\-–−]?\d+(\.\d+)?[\-–−~∼˜]\d+(\.\d+)?$')('value').add_action(merge)
spaced_range = (R('^[\+\-–−]?\d+(\.\d+)?$') + Optional(units).hide() + (R('^[\-–−~∼˜]$') +
                                                                        R('^[\+\-–−]?\d+(\.\d+)?$') | R('^[\+\-–−]\d+(\.\d+)?$')))('value').add_action(merge)
to_range = (R('^[\+\-–−]?\d+(\.\d+)?$') + Optional(units).hide() + (I('to') +
                                                                    R('^[\+\-–−]?\d+(\.\d+)?$') | R('^[\+\-–−]\d+(\.\d+)?$')))('value').add_action(join)

prefix = abbrv_prefix | words_pref | hyphanated_pref
common_text = R('(\w+)?\D(\D+)+(\w+)?').hide()
units = (W(u'V') | I(u'volt'))(u'units')
value = R(u'\d+(\.\d+)?')(u'value')

voc_first = (words_pref + (Optional(lbrct) + abbrv_prefix +
                           Optional(rbrct)) + ZeroOrMore(common_text) + value + units)(u'voc')
voc_second = (value + units + prefix)(u'voc')

voc_pattern = voc_first | voc_second


class VocParser(BaseParser):
    root = voc_pattern

    def interpret(self, result, start, end):
        compound = Compound(
            voc_pattern=[
                Voc(
                    value=first(result.xpath('./value/text()')),
                    units=first(result.xpath('./units/text()'))
                )
            ]
        )
        yield compound


def parse_voc(list_of_sentences):
    """ 
    Takes a list of sentences and parses for quantified PCE
    information and relationships to chemicals/chemical labels
    """

    Sentence.parsers.append(VocParser())

    cde_senteces = [Sentence(sent).records.serialize()
                    for sent in list_of_sentences]
    return cde_senteces
