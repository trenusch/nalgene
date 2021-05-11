from generate import *


def create_file(input, mental_lexicon):
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
                object = item['entity']
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
                        if mental_lexicon.from_word(item['entity']).genus == 'm':
                            file_write.write("    er")
                        elif mental_lexicon.from_word(item['entity']).genus == 'f':
                            file_write.write("    sie")
                        else:
                            file_write.write("    es")
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
                                file_write.write("    " + attribute)
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
