from generate import *

"""
    creates grammar file + output sentences for every subject given
    adds entries for objects / actions specified in subject
"""


def produce_multiple(input, mental_lexicon):
    subjects = [json.loads(item) for item in input if json.loads(item)["proposition"] == "subject"]
    positions = [json.loads(item) for item in input if json.loads(item)["proposition"] == "relpos"]
    properties = [json.loads(item) for item in input if json.loads(item)["proposition"] == "property"]
    relations = [json.loads(item) for item in input if json.loads(item)["proposition"] == "part_of"]
    for item in subjects:
        file = open("examples/grammar2.nlg", "r")
        file_write = open("examples/grammar2_complete.nlg", "w")
        # copy sentence structures
        for line in file:
            file_write.write(line)
        file_write.write("\n")

        assert len(subjects) != 0
        file_write.write("$subject\n")
        if mental_lexicon.contains_word(item['subject']):
            if item['infostate'] == "new":
                if mental_lexicon.from_word(item['subject']).get_genus() == 'm':
                    file_write.write("    der ")
                elif mental_lexicon.from_word(item['subject']).get_genus() == 'f':
                    file_write.write("    die ")
                else:
                    file_write.write("    das ")
                file_write.write(item['subject'] + "\n")
            else:
                if mental_lexicon.from_word(item['subject']).get_genus() == 'm':
                    file_write.write("    er\n")
                elif mental_lexicon.from_word(item['subject']).get_genus() == 'f':
                    file_write.write("    sie\n")
                else:
                    file_write.write("    es\n")
        file_write.write("\n")

        file_write.write("$action\n")
        if mental_lexicon.contains_word(item['action']):
            file_write.write("    " + mental_lexicon.from_word(item['action']).get_perfekt() + "\n")
        file_write.write("\n")

        try:
            for i in range(len(item['entity'])):  # in case of multiple entities, e.g.
                # "er hat mit dem loeffel die suppe gegessen"
                # additionally, the "laffe" entity could also be in the list as a second object
                # semantic information is needed! e.g:
                # Der Hund hat MIT DEM LOEFFEL die Suppe gegessen -> Mittel
                # Der Hund hat den loeffel AM RUNDEN gehalten -> Ort
                file_write.write("$object" + str(i) + "\n")
                if mental_lexicon.contains_word(item['entity'][i]):
                    if mental_lexicon.from_word(item['entity'][i]).get_genus() == 'm':
                        file_write.write("    den ")
                    elif mental_lexicon.from_word(item['entity'][i]).get_genus() == 'f':
                        file_write.write("    die ")
                    else:
                        file_write.write("    das ")
                    file_write.write(item['entity'][i] + "\n")
                else:
                    word = mental_lexicon.from_word(item['entity'][i])
                    if word is not None:
                        for attribute in word.get_attributes():
                            file_write.write("    " + attribute.get_value() + "\n")
                file_write.write("\n")

                # should attributes are mentioned if no part_of relation given?
                # -> missing semantic information, i.e. what kind of additional information is given,
                # e.g. where or how (an der laffe vs. mit dem loeffel)

                attributes = [att for att in positions + relations + properties
                              if att['rel_entity'] == item['entity'][i]]
                if len(attributes) != 0:
                    file_write.write("$location" + str(i) + "!\n")
                    for att in attributes:
                        if att['proposition'] == 'property' and mental_lexicon.contains_word(att["attribute"]):
                            file_write.write("    am " + att['attribute'] + "en" + str(att["activation"]) + "/\n")
                        elif att['proposition'] == 'relpos' and mental_lexicon.contains_word(att["attribute"]):
                            file_write.write("    " + att['attribute'] + str(att["activation"]) + "/\n")
                        elif att['proposition'] == 'part_of':
                            if mental_lexicon.contains_word(att['entity']):
                                file_write.write("    an ")
                                file_write.write("der ") if mental_lexicon.from_word(att['entity']).get_genus() == 'f' \
                                    else file_write.write("dem ")
                                file_write.write(att['entity'] + str(att["activation"]) + "/\n")
                            else:
                                # add all attributes known in lexicon
                                for attribute in mental_lexicon.from_word(att['entity']).get_attributes():
                                    if mental_lexicon.contains_word(attribute.get_value()):
                                        if attribute.type == "shape":
                                            file_write.write("    an dem " + attribute.get_value() + "en1./\n")
                                        elif attribute.type == "position":
                                            file_write.write("    " + attribute.get_value() + "1./\n")

        except KeyError:
            file_write.write("\n")
        file_write.close()
        file.close()

        filename = os.path.realpath("examples/grammar2_complete.nlg")
        base_dir = os.path.dirname(filename)
        filename = os.path.basename(filename)
        generate_from_file(base_dir, filename)  # , root_context)
