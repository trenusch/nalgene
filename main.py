import json

from application import *
from mental_lexicon import *
from words import *
# import ipaaca
import ast


def run(input, lexicon_input):
    #input_as_json = []
    #for i in input:
    #    as_json = ast.literal_eval(i)
    #    input_as_json.append(json.dumps(as_json))
    mental_lexicon = MentalLexicon()
    for word in lexicon_input:
        item = eval(word)
        mental_lexicon.add_item(item)
        if type(item) == Attribute:
            mental_lexicon.from_word(item.parent).add_attributes(item)

    produce_multiple(input, mental_lexicon)

"""
if __name__ == '__main__':
    # specify input of the system
    input = []

    dog_in2 = {"proposition": "subject",
               "subject": "hund",
               "action": "essen",
               "infostate": "old",
               "entity": "suppe"
               }

    gabel_in = {"proposition": "entity",
                "entity": "gabel",
                "activation": 1.00,
                "function": "modality"}

    dog_in = {"proposition": "subject",
              "subject": "hund",
              "attribute": "-",
              "entity": "loeffel",
              "action": "nehmen",
              "activation": 2.4,
              "infostate": "new"}

    loeffel_in = {"proposition": "entity",
                  "entity": "loeffel",
                  "activation": 1.99}

    laffe_in = {"proposition": "entity",
                "entity": "laffe",
                "activation": 2.01,
                "function": "modality"}

    relation_in = {"proposition": "part_of",
                   "entity": "laffe",
                   "rel_entity": "loeffel",
                   "activation": 1.99}

    attribute_rund_in = {"proposition": "property",
                         "entity": "laffe",
                         "attribute": "rund",
                         "activation": 10.00}

    attribute_gewoelbt_in = {"proposition": "property",
                             "entity": "loeffel",
                             "rel_entity": "loeffel",
                             "attribute": "gewoelbt",
                             "activation": 3.00}

    relpos_unten_in = {"proposition": "relpos",
                       "entity": "loeffel",
                       "rel_entity": "loeffel",
                       "attribute": "unten",
                       "activation": 5.00}

    direction_in = {"proposition": "direction",
                    "entity": "laffe",
                    "attribute": "unten",
                    "activation": 1.00}


    hund = Subject('m', "hund", known=True)
    loeffel = Entity('m', "loeffel")
    nehmen = Action("nehmen", "genommen", known=True)
    laffe = Entity('f', "laffe")
    unten = Attribute(loeffel, "unten", known=True)
    gewoelbt = Attribute(loeffel, "gewoelbt", known=True)
    rund = Attribute(laffe, "rund", known=True)
    laffe.add_attributes(gewoelbt)
    laffe.add_attributes(unten)
    laffe.add_attributes(rund)
    essen = Action("essen", "gegessen", known=True)
    suppe = Entity('f', "suppe", known=True)
    gabel = Entity('f', "gabel", known=True)

    mental_lexicon = MentalLexicon()
    mental_lexicon.add_item(hund)
    mental_lexicon.add_item(loeffel)
    mental_lexicon.add_item(nehmen)
    mental_lexicon.add_item(laffe)
    mental_lexicon.add_item(unten)
    mental_lexicon.add_item(gewoelbt)
    mental_lexicon.add_item(rund)
    mental_lexicon.add_item(essen)
    mental_lexicon.add_item(suppe)
    mental_lexicon.add_item(gabel)

    input.append(json.dumps(dog_in))
    input.append(json.dumps(loeffel_in))
    input.append(json.dumps(laffe_in))
    input.append(json.dumps(relation_in))
    input.append(json.dumps(attribute_rund_in))
    input.append(json.dumps(attribute_gewoelbt_in))
    input.append(json.dumps(relpos_unten_in))
    input.append(json.dumps(direction_in))
    # input.append(json.dumps(dog_in2))
    # input.append(json.dumps(gabel_in))
    produce_multiple(input, mental_lexicon)
    """
