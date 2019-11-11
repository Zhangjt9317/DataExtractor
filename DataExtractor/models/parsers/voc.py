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


class Voc(BaseModel):
    value = StringType()
    units = StringType()


Compound.voc_pattern = ListType(ModelType(Voc))

common_text = R('(\w+)?\D(\D+)+(\w+)?').hide()
units = (W(u'V') | I(u'v') | I(u'volt') | I(u'volts'))(u'units')
value = R(u'\d+(\.\d+)?')(u'value')

abbrv_prefix = (I(u'Voc') | I(u'voc')).hide()
words_pref = (I(u'open') + I(u'circuit') + I(u'voltage')).hide()
hyphanated_pref = (I(u'open') + I(u'-') + I('circuit') + I(u'voltage')).hide()
joined_range = R(
    '^[\+\-–−]?\d+(\.\d+)?[\-–−~∼˜]\d+(\.\d+)?$')('value').add_action(merge)
spaced_range = (R('^[\+\-–−]?\d+(\.\d+)?$') + Optional(units).hide() + (R('^[\-–−~∼˜]$') +
                                                                        R('^[\+\-–−]?\d+(\.\d+)?$') | R('^[\+\-–−]\d+(\.\d+)?$')))('value').add_action(merge)
to_range = (R('^[\+\-–−]?\d+(\.\d+)?$') + Optional(units).hide() + (I('to') +
                                                                    R('^[\+\-–−]?\d+(\.\d+)?$') | R('^[\+\-–−]\d+(\.\d+)?$')))('value').add_action(join)

prefix = Optional(I('a')).hide() + (Optional(lbrct) + W('Voc') + Optional(rbrct) | I('open') + Optional(I('circuit')) + Optional((I('voltage')))
                                    ).hide() + Optional(lbrct + W('Voc') + rbrct) + Optional(W('=') | I('of') | I('was') | I('is') | I('at')).hide() + Optional(I('in') + I('the') + I('range') + Optional(I('of')) | I('about') | ('around') | I('V')).hide()

voc_first = (words_pref + (Optional(lbrct) + abbrv_prefix +
                           Optional(rbrct)) + ZeroOrMore(common_text) + value + units)(u'voc')
voc_second = (prefix + value + units)(u'voc')
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
