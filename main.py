from application import *
from mental_lexicon import *

if __name__ == '__main__':
    # specify input of the system
    input = []

    dog_in2 = {"proposition": "subject",
               "subject": "hund",
               "action": "essen",
               "infostate": "old",
               "entity": ["suppe", "loeffel"]
    }

    dog_in = {"proposition": "subject",
              "subject": "hund",
              "attribute": "-",
              "entity": ["loeffel"],
              "action": "nehmen",
              "activation": 2.4,
              "infostate": "new"}

    loeffel_in = {"proposition": "entity",
                  "entity": "loeffel",
                  "activation": 1.99}

    laffe_in = {"proposition": "entity",
                "entity": "laffe",
                "activation": 2.01}

    relation_in = {"proposition": "part_of",
                   "entity": "laffe",
                   "rel_entity": "loeffel",
                   "activation": 1.99}

    attribute1_in = {"proposition": "property",
                     "entity": "laffe",
                     "rel_entity": "loeffel",
                     "attribute": "rund",
                     "activation": 4.00}

    attribute2_in = {"proposition": "property",
                     "entity": "laffe",
                     "rel_entity": "loeffel",
                     "attribute": "gewoelbt",
                     "activation": 3.00}

    relpos_in = {"proposition": "relpos",
                 "entity": "laffe",
                 "rel_entity": "loeffel",
                 "attribute": "unten",
                 "activation": 5.00}

    hund = Subject('m', "hund", known=True)
    loeffel = Entity('m', "loeffel", known=True)
    nehmen = Action("nehmen", "genommen", known=True)
    laffe = Entity('f', "laffe")
    unten = Attribute(laffe, "unten", known=True)
    gewölbt = Attribute(laffe, "gewoelbt", known=True)
    laffe.add_attributes(gewölbt)
    laffe.add_attributes(unten)
    essen = Action("essen", "gegessen", known=True)
    suppe = Entity('f', "suppe", known=True)


    mental_lexicon = MentalLexicon()
    mental_lexicon.add_item(hund)
    mental_lexicon.add_item(loeffel)
    mental_lexicon.add_item(nehmen)
    mental_lexicon.add_item(laffe)
    mental_lexicon.add_item(unten)
    mental_lexicon.add_item(gewölbt)
    mental_lexicon.add_item(essen)
    mental_lexicon.add_item(suppe)

input.append(json.dumps(dog_in))
input.append(json.dumps(loeffel_in))
input.append(json.dumps(laffe_in))
input.append(json.dumps(relation_in))
#input.append(json.dumps(dog_in2))
#input.append(json.dumps(attribute1_in))
#input.append(json.dumps(attribute2_in))
#input.append(json.dumps(relpos_in))
#produce(input, mental_lexicon)
produce_multiple(input, mental_lexicon)
