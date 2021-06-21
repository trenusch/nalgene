from generate import *

"""
    creates grammar file + output sentences for every subject given
    adds entries for objects / actions specified in subject
"""


def produce_multiple(input, mental_lexicon):
    subjects = [json.loads(item) for item in input if json.loads(item)["proposition"] == "subject"]
    positions = [json.loads(item) for item in input if json.loads(item)["proposition"] == "relpos"]
    properties = [json.loads(item) for item in input if json.loads(item)["proposition"] == "property"]
    directions = [json.loads(item) for item in input if json.loads(item)["proposition"] == "direction"]
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
                if mental_lexicon.from_word(item['subject']).genus == 'm':
                    file_write.write("    der ")
                elif mental_lexicon.from_word(item['subject']).genus == 'f':
                    file_write.write("    die ")
                else:
                    file_write.write("    das ")
                file_write.write(item['subject'] + "\n")
            else:
                if mental_lexicon.from_word(item['subject']).genus == 'm':
                    file_write.write("    er\n")
                elif mental_lexicon.from_word(item['subject']).genus == 'f':
                    file_write.write("    sie\n")
                else:
                    file_write.write("    es\n")
        file_write.write("\n")

        file_write.write("$action\n")
        if mental_lexicon.contains_word(item['action']):
            file_write.write("    " + mental_lexicon.from_word(item['action']).perfekt + "\n")
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
                    if mental_lexicon.from_word(item['entity'][i]).genus == 'm':
                        file_write.write("    den ")
                    elif mental_lexicon.from_word(item['entity'][i]).genus == 'f':
                        file_write.write("    die ")
                    else:
                        file_write.write("    das ")
                    file_write.write(item['entity'][i] + "\n")
                else:
                    word = mental_lexicon.from_word(item['entity'][i])
                    if word is not None:
                        for attribute in word.attributes():
                            file_write.write("    " + attribute.value + "\n")
                file_write.write("\n")

                # should attributes are mentioned if no part_of relation given?
                # -> missing semantic information, i.e. what kind of additional information is given,
                # e.g. where or how (an der laffe vs. mit dem loeffel)

                attributes = [att for att in positions + properties
                              if att['rel_entity'] == item['entity'][i]
                              and mental_lexicon.contains_word(att['attribute'])]
                attributes += [att for att in relations if att['rel_entity'] == item['entity'][i]]
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
                                file_write.write("der ") if mental_lexicon.from_word(att['entity']).genus == 'f' \
                                    else file_write.write("dem ")
                                file_write.write(att['entity'] + str(att["activation"]) + "/\n")
                            else:
                                # add all attributes known in lexicon
                                for attribute in mental_lexicon.from_word(att['entity']).attributes():
                                    if mental_lexicon.contains_word(attribute.value):
                                        if attribute.type == "shape":
                                            file_write.write("    an dem " + attribute.value + "en1./\n")
                                        elif attribute.type == "position":
                                            file_write.write("    " + attribute.value + "1./\n")
                try:
                    relation = [rel for rel in relations if rel['rel_entity'] == item['entity'][i]]
                    for rel in relation:
                        direction = [dir for dir in directions if dir['rel_entity'] == rel['rel_entity']
                                     and dir['entity'] == rel['entity']
                                     and mental_lexicon.contains_word(dir['attribute'])][0]
                        assert len(direction) != 0
                        file_write.write("\n$direction\n")
                        file_write.write("    $dir_obj $dir_dir\n")
                        file_write.write("\n")
                        file_write.write("$dir_obj\n")
                        if mental_lexicon.contains_word(att['entity']):
                            file_write.write("    mit ")
                            file_write.write("der ") if mental_lexicon.from_word(att['entity']).genus == 'f' \
                                else file_write.write("dem ")
                            file_write.write(att['entity'] + str(att["activation"]) + "/\n")
                        else:
                            # add all attributes known in lexicon
                            for attribute in mental_lexicon.from_word(att['entity']).attributes:
                                if mental_lexicon.contains_word(attribute.value):
                                    if attribute.type == "shape":
                                        file_write.write("    mit dem " + attribute.value + "en1./\n")
                        file_write.write("\n$dir_dir\n")
                        file_write.write("    nach ")
                        file_write.write(direction['attribute'])
                except IndexError:
                    file_write.write("\n")

        except KeyError:
            file_write.write("\n")
        file_write.close()
        file.close()

        filename = os.path.realpath("examples/grammar2_complete.nlg")
        base_dir = os.path.dirname(filename)
        filename = os.path.basename(filename)
        msg = generate_from_file(base_dir, filename)  # , root_context)
        print(msg)

        # ipaaca component, currently throws socket error (connection refused)
        #outbuffer = ipaaca.OutputBuffer('speech_generator')
        #iu = ipaaca.IU('Message')
        #iu.payload = {"msg": msg}
        #outbuffer.add(iu)
