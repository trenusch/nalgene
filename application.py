from generate import *

"""
    parses grammar file and adds specific entries given in the input
"""
def produce(input, mental_lexicon):
    subjects = [json.loads(item) for item in input if json.loads(item)["proposition"] == "subject"]
    entities = [json.loads(item) for item in input if json.loads(item)["proposition"] == "entity"]
    attributes = [json.loads(item) for item in input if json.loads(item)["proposition"] == "property"]
    positions = [json.loads(item) for item in input if json.loads(item)["proposition"] == "relpos"]
    relation = [json.loads(item) for item in input if json.loads(item)["proposition"] == "part_of"]

    file = open("examples/grammar.nlg", "r")
    file_write = open("examples/grammar_complete.nlg", "w")
    for line in file:
        file_write.write(line)
        if line.startswith("$subject"):
            for item in subjects:
                try:
                    object = item['entity'][0]  # quick fix for multiple entities as list
                    if mental_lexicon.contains_word(item['subject']):
                        if item['infostate'] == "new":
                            if mental_lexicon.from_word(item['subject']).genus == 'm':
                                file_write.write("    der ")
                            elif mental_lexicon.from_word(item['subject']).genus == 'f':
                                file_write.write("    die ")
                            else:
                                file_write.write("    das ")
                            file_write.write(item['subject'])
                        else:
                            if mental_lexicon.from_word(item['subject']).genus == 'm':
                                file_write.write("    er")
                            elif mental_lexicon.from_word(item['subject']).genus == 'f':
                                file_write.write("    sie")
                            else:
                                file_write.write("    es")
                except KeyError as e:
                    object = None

        elif line.startswith("$object"):
            for item in entities:
                if item['entity'] == object:
                    if mental_lexicon.contains_word(item['entity']):
                        if mental_lexicon.from_word(item['entity']).genus == 'm':
                            file_write.write("    den ")
                        elif mental_lexicon.from_word(item['entity']).genus == 'f':
                            file_write.write("    die ")
                        else:
                            file_write.write("    das ")
                        file_write.write(item['entity'])
                    else:
                        word = mental_lexicon.from_word(item['entity'])
                        if word is not None:
                            for attribute in word.attributes:
                                file_write.write("    " + attribute.value + "\n")
        elif line.startswith("$action"):
            for item in subjects:
                if mental_lexicon.contains_word(item['action']):
                    file_write.write("    " + mental_lexicon.from_word(item['action']).perfekt)
        elif line.startswith("$location"):
            for item in positions + attributes:
                if item['rel_entity'] == object:
                    if mental_lexicon.contains_word(item['attribute']):
                        file_write.write("    " + item['attribute'] + str(item["activation"]) + "/" + "\n")
            for item in relation:
                if item['rel_entity'] == object:
                    if mental_lexicon.contains_word(item["entity"]):
                        file_write.write("    an der " + item['entity'] + str(item["activation"]) + "/" + "\n")
                    else:
                        attributes_rel = mental_lexicon.from_word(item['entity']).attributes
                        for attribute in attributes_rel:
                            if mental_lexicon.contains_word(attribute.value):
                                file_write.write("    " + attribute.value + "1./\n")

    file_write.close()
    file.close()

    filename = os.path.realpath("examples/grammar_complete.nlg")
    base_dir = os.path.dirname(filename)
    filename = os.path.basename(filename)
    generate_from_file(base_dir, filename)  # , root_context)

"""
    creates grammar file + output sentences for every subject given
    adds entries for objects / actions specified in subject
"""
def produce_multiple(input, mental_lexicon):
    subjects = [json.loads(item) for item in input if json.loads(item)["proposition"] == "subject"]
    entities = [json.loads(item) for item in input if json.loads(item)["proposition"] == "entity"]
    attributes = [json.loads(item) for item in input if json.loads(item)["proposition"] == "property"]
    positions = [json.loads(item) for item in input if json.loads(item)["proposition"] == "relpos"]
    relation = [json.loads(item) for item in input if json.loads(item)["proposition"] == "part_of"]

    for item in subjects:
        file = open("examples/grammar2.nlg", "r")
        file_write = open("examples/grammar2_complete.nlg", "w")
        for line in file:
            file_write.write(line)
        file_write.write("\n")

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
            for i in range(len(item['entity'])):
                object = item['entity'][i]
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
                        for attribute in word.attributes:
                            file_write.write("    " + attribute.value + "\n")
                file_write.write("\n")

                """file_write.write("$location" + str(i) + "!\n")
                for pos in positions + attributes:
                    if pos['rel_entity'] == object:
                        if mental_lexicon.contains_word(pos['attribute']):
                            file_write.write("    " + pos['attribute'] + str(pos["activation"]) + "/\n")
                for rel in relation:
                    if rel['rel_entity'] == object:
                        if mental_lexicon.contains_word(rel["entity"]):
                            file_write.write("    an der " + rel['entity'] + str(rel["activation"]) + "/\n")
                        else:
                            attributes_rel = mental_lexicon.from_word(rel['entity']).attributes
                            for attribute in attributes_rel:
                                if mental_lexicon.contains_word(attribute.value):
                                    file_write.write("    " + attribute.value + "1./\n")
                file_write.write("\n")"""

        except KeyError as e:
            file_write.write("\n")
        file_write.close()
        file.close()

        filename = os.path.realpath("examples/grammar2_complete.nlg")
        base_dir = os.path.dirname(filename)
        filename = os.path.basename(filename)
        generate_from_file(base_dir, filename)  # , root_context)
