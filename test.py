import json
from application import produce_multiple
from mental_lexicon import MentalLexicon
from words import *

if __name__ == "__main__":

    lexicon = MentalLexicon()
    hund = Subject("m", "hund", True)
    nehmen = Action("nehmen", "genommen", True)
    lexicon.add_item(hund)
    lexicon.add_item(nehmen)

    input = []
    input.append(json.dumps({"proposition": "subject", "subject": "hund", "infostate": "new", "action": "nehmen", "activation": 2.0}))
    assert (produce_multiple(input, lexicon) == "Der hund hat genommen.")

    loeffel = Entity("m", "loeffel", False)
    lexicon.add_item(loeffel)
    input.clear()
    input.append(json.dumps({"proposition": "subject", "subject": "hund", "infostate": "new", "action": "nehmen",
                             "entity": "loeffel", "activation": 2.0}))
    input.append(json.dumps({"proposition": "entity", "entity": "loeffel", "activation": 1.5}))
    assert (produce_multiple(input, lexicon) == "Der hund hat den aehm genommen.")

    loeffel.known = True
    lexicon.add_item(loeffel)
    assert (produce_multiple(input, lexicon) == "Der hund hat den loeffel genommen.")

    lexicon.remove_item(nehmen)
    assert (produce_multiple(input, lexicon) == "")

    lexicon.add_item(nehmen)
    lexicon.remove_item(hund)
    assert (produce_multiple(input, lexicon) == "")

    lexicon.add_item(hund)
    laffe = Entity("f", "laffe", False)
    lexicon.add_item(laffe)
    input.append(json.dumps({"proposition": "entity", "entity": "laffe", "activation": 1.5}))
    assert (produce_multiple(input, lexicon) == "Der hund hat den loeffel genommen.")

    input.remove(json.dumps({"proposition": "entity", "entity": "laffe", "activation": 1.5}))
    input.append(json.dumps({"proposition": "entity", "entity": "laffe", "activation": 1.5, "function": "location"}))
    assert (produce_multiple(input, lexicon) == "Der hund hat den loeffel genommen.")

    input.remove(json.dumps({"proposition": "entity", "entity": "laffe", "activation": 1.5, "function": "location"}))
    input.append(json.dumps({"proposition": "part_of", "entity": "laffe", "rel_entity": "loeffel"}))
    input.append(json.dumps({"proposition": "entity", "entity": "laffe", "activation": 1.5, "function": "location"}))
    sentence = produce_multiple(input, lexicon)
    assert (sentence == "Der hund hat den loeffel da genommen." or sentence == "Da hat der hund den loeffel genommen.")

    rund = Attribute("laffe", "rund", True)
    lexicon.add_item(rund)
    input.append(json.dumps({"proposition": "property", "attribute": "rund", "activation": 4.0, "entity": "laffe"}))
    sentence = produce_multiple(input, lexicon)
    assert (sentence == "Der hund hat den loeffel am runden genommen." or
            sentence == "Am runden hat der hund den loeffel genommen.")

    laffe.known = True
    lexicon.add_item(laffe)
    sentence = produce_multiple(input, lexicon)
    assert (sentence == "Der hund hat den loeffel an der laffe genommen." or
            sentence == "An der laffe hat der hund den loeffel genommen.")

    hund.known = False
    lexicon.add_item(hund)
    sentence = produce_multiple(input, lexicon)
    assert (sentence == "Der aeh hat den loeffel an der laffe genommen." or
            sentence == "An der laffe hat der aeh den loeffel genommen.")

    hund.known = True
    lexicon.add_item(hund)
    input.clear()
    input.append(json.dumps({"proposition": "subject", "subject": "hund", "infostate": "old", "action": "nehmen",
                             "entity": "loeffel", "activation": 2.0}))
    input.append(json.dumps({"proposition": "entity", "entity": "loeffel", "activation": 1.5}))
    assert (produce_multiple(input, lexicon) == "Er hat den loeffel genommen.")

    input.append(json.dumps({"proposition": "entity", "entity": "stiel", "activation": 1.5, "function": "modality"}))
    input.append(json.dumps({"proposition": "property", "attribute": "laenglich", "activation": 4.0, "entity": "stiel"}))
    stiel = Entity("m", "stiel", False)
    laenglich = Attribute("stiel", "laenglich", True)
    lexicon.add_item(stiel)
    lexicon.add_item(laenglich)
    sentence = produce_multiple(input, lexicon)
    assert (sentence == "Er hat den loeffel mit dem laenglichen genommen." or
            sentence == "Mit dem laenglichen hat er den loeffel genommen.")

