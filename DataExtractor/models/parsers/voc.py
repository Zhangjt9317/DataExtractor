class Voc(BaseModel):
    value = StringType()
    units = StringType()

Compound.voc_pattern = ListType(ModelType(Voc))

abbrv_prefix = (
    I(u'VOC') | I(u'voc') | I(u'Voc') ).hide()
words_pref = (
    I(u'open') + I(u'circuit') + I(u'voltage')
    ).hide()
hyphanated_pref =(
    I(u'open-circuit') + I(u'voltage')
    ).hide()
prefix = abbrv_prefix | words_pref | hyphanated_pref

common_text = R('(\w+)?\D(\D+)+(\w+)?').hide()
units = (W(u'V') | I(u'volt'))(u'units')
# value = R(u'^\d+(\.\d+)?$')(u'value')
value = R(u'\d+(\.\d+)?')(u'value')

voc_first= (prefix + ZeroOrMore(common_text) + value + units)(u'voc')
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
    """ Takes a list of sentences and parses for quantified PCE
        information and relationships to chemicals/chemical labels
        """

    Sentence.parsers.append(VocParser())

    cde_senteces = [Sentence(sent).records.serialize() for sent in list_of_sentences]
    return cde_senteces