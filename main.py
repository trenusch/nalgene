import json
from application import *
from mental_lexicon import *
from words import *
import ast


def run(input, lexicon_input):
    input_as_json = []
    if len(input) == 1 and input[0][0:7] == "input =":
        input_as_list = eval(input[0][7:])
        for i in input_as_list:
            input_as_json.append(json.dumps(i))
    else:
        for i in input:
            as_json = ast.literal_eval(i)
            input_as_json.append(json.dumps(as_json))
    mental_lexicon = MentalLexicon()
    if len(lexicon_input) == 1 and lexicon_input[0][0:7] == "input =":
        lexicon_input = eval(lexicon_input[0][7:])
    for word in lexicon_input:
        mental_lexicon.add_item(word)
        if type(word) == Attribute:
            object = mental_lexicon.from_word(word.parent)
            if object is not None:
                object.add_attributes(word)
    msg = produce_multiple(input_as_json, mental_lexicon)
    if msg is not None:
        return msg
    else:
        return ""
