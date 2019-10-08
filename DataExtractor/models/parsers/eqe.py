"""
DataExtractor.parser.eqe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is built on top of the chemdataextractor module:
'chemdataextractor.parse.uvvis' as an example for implementaion of the
chemdataextractor pasing syntax.

Parses the external quantum efficiency, similar to the one of IQE

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


class Eqe(BaseModel):
    value = StringType()
    units = StringType()

Compound.eqe_pattern = ListType(ModelType(Eqe))

abbrv_prefix = (I(u'EQE')).hide()
words_pref = (I(u'external') + I(u'quantum') + I(u'efficiency')).hide()
# hyphanated_pref = (I(u'power-conversion') + I(u'efficiency')).hide()
prefix = abbrv_prefix | words_pref

common_text = R('(\w+)?\D(\D+)+(\w+)?').hide()
units = (W(u'%') | I(u'percent'))(u'units')
value = R(u'\d+(\.\d+)?')(u'value')

eqe_first = (prefix + ZeroOrMore(common_text) + value + units)(u'eqe')
eqe_second = (value + units + prefix)(u'ff')
eqe_pattern = eqe_first | eqe_second

class EqeParser(BaseParser):
    root = eqe_pattern

    def interpret(self, result, start, end):
        compound = Compound(
            eqe_pattern=[
                Eqe(
                    value=first(result.xpath('./value/text()')),
                    units=first(result.xpath('./units/text()'))
                )
            ]
        )
        yield compound


def parse_eqe(list_of_sentences):
    """ 
    Takes a list of sentences and parses for quantified PCE
    information and relationships to chemicals/chemical labels
    """

    Sentence.parsers.append(EqeParser())

    cde_senteces = [Sentence(sent).records.serialize()
                    for sent in list_of_sentences]
    return cde_senteces
