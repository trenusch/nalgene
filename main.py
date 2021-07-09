import json
from application import *
from mental_lexicon import *
from words import *
import ast


def run(input, lexicon_input):
    input_as_json = []
    for i in input:
        as_json = ast.literal_eval(i)
        input_as_json.append(json.dumps(as_json))
    mental_lexicon = MentalLexicon()
    for word in lexicon_input:
        item = eval(word)
        mental_lexicon.add_item(item)
        if type(item) == Attribute:
            mental_lexicon.from_word(item.parent).add_attributes(item)
    msg = produce_multiple(input, mental_lexicon)
    if msg is not None:
        return msg
    else:
        return ""
