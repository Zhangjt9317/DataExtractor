"""
DataExtractor.parsers.pce
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is built on top of the chemdataextractor module:
'chemdataextractor.parse.uvvis' as an example for implementaion of the
chemdataextractor pasing syntax.

Parses the power conversion efficiency, it can be applied to solar cells.
PCE is one key parameter to measure the performance of solar cells.

"""

import logging
import re

import chemdataextractor as cde
from chemdataextractor import Document
from chemdataextractor.model import Compound, UvvisSpectrum, UvvisPeak, BaseModel, StringType, ListType, ModelType
from chemdataextractor.parse.common import hyphen,lbrct, dt, rbrct
from chemdataextractor.parse.base import BaseParser
from chemdataextractor.utils import first

from chemdataextractor.parse.actions import strip_stop, merge, join
from chemdataextractor.parse.elements import W, I, T, R, Optional, ZeroOrMore, OneOrMore, Or, And, Not, Any
from chemdataextractor.parse.cem import chemical_name,cem, chemical_label, lenient_chemical_label, solvent_name
from chemdataextractor.doc import Paragraph, Sentence, Caption, Figure,Table, Heading
from chemdataextractor.doc.table import Table, Cell


class Pce(BaseModel):
    value = StringType()
    units = StringType()

Compound.pce_pattern = ListType(ModelType(Pce))

common_text = R('(\w+)?\D(\D+)+(\w+)?').hide()
units = (W(u'%') | I(u'percent'))(u'units')
value = R(u'\d+(\.\d+)?')(u'value')

abbrv_prefix = (I(u'PCE') | I(u'PCEs') | I(u'pce')).hide()
words_pref = (I(u'power') + I(u'conversion') + I(u'efficiency')).hide()
hyphanated_pref = (I(u'power') + I(u'-') + I('conversion') + I(u'efficiency')).hide()
joined_range = R('^[\+\-–−]?\d+(\.\d+)?[\-–−~∼˜]\d+(\.\d+)?$')('value').add_action(merge)
spaced_range = (R('^[\+\-–−]?\d+(\.\d+)?$') + Optional(units).hide() + (R('^[\-–−~∼˜]$') +
                                                                        R('^[\+\-–−]?\d+(\.\d+)?$') | R('^[\+\-–−]\d+(\.\d+)?$')))('value').add_action(merge)
to_range = (R('^[\+\-–−]?\d+(\.\d+)?$') + Optional(units).hide() + (I('to') +
                                                                    R('^[\+\-–−]?\d+(\.\d+)?$') | R('^[\+\-–−]\d+(\.\d+)?$')))('value').add_action(join)

prefix = Optional(I('a')).hide() + (Optional(lbrct) + W('PCEs') + Optional(rbrct) | I('power') + Optional(I('conversion')) + Optional((I('efficiency') | I('range'))) + Optional((I('temperature') | I('range')))
                                    ).hide() + Optional(lbrct + W('PCE') + rbrct) + Optional(W('=') | I('of') | I('was') | I('is') | I('at')).hide() + Optional(I('in') + I('the') + I('range') + Optional(I('of')) | I('about') | ('around') | I('%')).hide()

pce_first  = (words_pref + (Optional(lbrct) + abbrv_prefix + Optional(rbrct)) + ZeroOrMore(common_text) + value + units)(u'pce')
# pce_first = (prefix + ZeroOrMore(common_text) + value + units)(u'pce')
pce_second = (prefix + value + units)(u'pce')
pce_pattern = pce_first | pce_second

class PceParser(BaseParser):
    root = pce_pattern

    def interpret(self, result, start, end):
        compound = Compound(
            pce_pattern=[
                Pce(
                    value=first(result.xpath('./value/text()')),
                    units=first(result.xpath('./units/text()'))
                )
            ]
        )
        yield compound
        
def parse_pce(list_of_sentences):
    """ 
    Takes a list of sentences and parses for quantified PCE
    information and relationships to chemicals/chemical labels
    """

    Sentence.parsers.append(PceParser())

    cde_senteces = [Sentence(sent).records.serialize()
                    for sent in list_of_sentences]
    return cde_senteces
