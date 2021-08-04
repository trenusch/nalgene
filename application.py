from generate import *
import ipaaca
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
    objects = [json.loads(item) for item in input if json.loads(item)['proposition'] == "entity"]
    if len(subjects) == 0 or len(subjects) > 1:
        return ""
    item = subjects[0]
    file = open("examples/grammar2.nlg", "r")
    file_write = open("examples/grammar2_complete.nlg", "w")

    # copy sentence structures
    for line in file:
        file_write.write(line)
    file_write.write("\n")

    if mental_lexicon.contains_word(item['subject']):
        file_write.write("$subject!\n")
        try:
            if item['infostate'] == "new":
                if mental_lexicon.from_word(item['subject']).genus == 'm':
                    file_write.write("    der ")
                elif mental_lexicon.from_word(item['subject']).genus == 'f':
                    file_write.write("    die ")
                else:
                    file_write.write("    das ")
                file_write.write(item['subject'] + "1.0/\n")
            else:
                if mental_lexicon.from_word(item['subject']).genus == 'm':
                    file_write.write("    er1.0/\n")
                elif mental_lexicon.from_word(item['subject']).genus == 'f':
                    file_write.write("    sie1.0/\n")
                else:
                    file_write.write("    es1.0/\n")
        except KeyError:  # missing infostate will be treated as new
            if mental_lexicon.from_word(item['subject']).genus == 'm':
                file_write.write("    der ")
            elif mental_lexicon.from_word(item['subject']).genus == 'f':
                file_write.write("    die ")
            else:
                file_write.write("    das ")
            file_write.write(item['subject'] + "1.0/\n")
    else:
        if mental_lexicon.contains_concept(item['subject']):
            file_write.write("$subject!\n")
            attributes = [att for att in mental_lexicon.from_word(item['subject']).attributes]
            if item['infostate'] == "new":
                for attribute in attributes:
                    file_write.write("    das " + attribute.value + "e" + str(item['activation']) + "/\n")
                if len(attributes) == 0:
                    file_write.write("    der aeh1.0/\n")
                    # TODO: add gesture
            else:
                if mental_lexicon.from_word(item['subject']).genus == 'm':
                    file_write.write("    er1.0/\n")
                elif mental_lexicon.from_word(item['subject']).genus == 'f':
                    file_write.write("    sie1.0/\n")
                else:
                    file_write.write("    es1.0/\n")

    file_write.write("\n")
    try:
        if mental_lexicon.contains_word(item['action']):
            file_write.write("$action\n")
            file_write.write("    " + mental_lexicon.from_word(item['action']).perfekt + "\n")
        file_write.write("\n")
    except KeyError:  # missing action
        print("No Action specified")
        return ""
    try:
        # only one entity given in subject, additional entities can be given with individual proposition
        # "er hat die suppe gegessen" vs. "er hat die suppe mit dem loeffel gegessen"
        # semantic information is needed (proposition)! e.g:
        # Der Hund hat die suppe MIT DEM LOEFFEL gegessen -> Mittel
        # Der Hund hat den loeffel AN DER LAFFE gehalten -> Ort
        # Der Hund hat den loeffel NACH OBEN gehalten -> Richtung
        dir_object = {}
        if len([obj for obj in objects if obj['entity'] == item['entity']]) != 0:
            if mental_lexicon.contains_word(item['entity']):
                dir_object = [obj for obj in objects if obj['entity'] == item['entity']][0]
                file_write.write("$object!" + "\n")
                if mental_lexicon.from_word(item['entity']).genus == 'm':
                    file_write.write("    den ")
                elif mental_lexicon.from_word(item['entity']).genus == 'f':
                    file_write.write("    die ")
                else:
                    file_write.write("    das ")
                file_write.write(item['entity'] + "1.0/\n")
            else:
                attributes = [att for att in positions + properties if att['entity'] == item['entity']
                              and mental_lexicon.contains_word(att['attribute'])]
                if len(attributes) != 0:
                    file_write.write("$object!\n")
                    for att in attributes:
                        if att['attribute'][-2:] != "en":
                            file_write.write("    den " + att['attribute'] + "en" + str(att['activation']) + "/\n")
                        else:
                            file_write.write(
                                "    den " + att['attribute'][0:-1] + "ren" + str(att['activation']) + "/\n")
                else:
                    if mental_lexicon.contains_concept(item['entity']):
                        file_write.write("$object!\n")
                        if mental_lexicon.from_word(item['entity']).genus == 'm':
                            file_write.write("    den ")
                        elif mental_lexicon.from_word(item['entity']).genus == 'f':
                            file_write.write("    die ")
                        else:
                            file_write.write("    das ")
                        file_write.write("aehm1.0/\n")
                    # TODO: add gesture

        file_write.write("\n")

        add_direction(dir_object, directions, file_write, mental_lexicon)

        # relation is key for generating specific location
        part_of = [rel for rel in relations if rel['rel_entity'] == item['entity']]
        if len(part_of) == 1:  # should be 1, produce object addition
            relation = part_of[0]
            object = [obj for obj in objects if obj['entity'] == relation['entity']][0]
            objects = [obj for obj in objects if obj['entity'] != relation['entity']]
            attributes = [att for att in positions + properties
                          if att['entity'] == object['entity']
                          and mental_lexicon.contains_word(att['attribute'])]
            if object['function'] == 'location':
                add_location(object, attributes, file_write, mental_lexicon)
            elif object['function'] == 'modality':
                add_modality(object, attributes, file_write, mental_lexicon)

                # only added if additional direction is given
                add_direction(object, directions, file_write, mental_lexicon)
        if len(objects) >= 1:
            for entity in objects:
                try:
                    if entity['function'] == "modality":
                        attributes = [att for att in positions + properties
                                      if att['entity'] == entity['entity']
                                      and mental_lexicon.contains_word(att['attribute'])]
                        add_modality(entity, attributes, file_write, mental_lexicon)
                        add_direction(entity, directions, file_write, mental_lexicon)

                    # TODO elif entity['function'] == "?" possibility to extend with different functions

                except KeyError:
                    pass



    except KeyError:
        file_write.write("\n")
    file_write.close()
    file.close()

    filename = os.path.realpath("examples/grammar2_complete.nlg")
    base_dir = os.path.dirname(filename)
    filename = os.path.basename(filename)
    msg = generate_from_file(base_dir, filename)  # , root_context)
    print(msg)

    # ipaaca component, throws TypeError (sometimes)
    outbuffer = ipaaca.OutputBuffer('speech_generator')
    iu = ipaaca.IU('verbal')
    iu.payload = {"type": "sentence",
                  "msg": msg}
    outbuffer.add(iu)


def add_location(entity, attributes, file_write, mental_lexicon):
    file_write.write("$location!\n")
    if mental_lexicon.contains_word(entity['entity']):
        file_write.write("    an ")
        file_write.write("der ") if mental_lexicon.from_word(entity['entity']).genus == 'f' \
            else file_write.write("dem ")
        file_write.write(entity['entity'] + str(entity["activation"]) + "/\n")
    else:
        for att in attributes:
            if att['proposition'] == 'property':
                file_write.write("    am " + att['attribute'] + "en" + str(att["activation"]) + "/\n")
            elif att['proposition'] == 'relpos':
                file_write.write("    " + att['attribute'] + str(att["activation"]) + "/\n")
        if len(attributes) == 0:
            file_write.write("    da1.0/\n")
            # TODO: add gesture


def add_modality(entity, attributes, file_write, mental_lexicon):
    file_write.write("$modality!\n")
    if mental_lexicon.contains_word(entity['entity']):
        file_write.write("    mit ")
        file_write.write("der ") if mental_lexicon.from_word(entity['entity']).genus == 'f' \
            else file_write.write("dem ")
        file_write.write(entity['entity'] + str(entity["activation"]) + "/\n")
    else:
        for att in attributes:
            if att['proposition'] == 'property':
                file_write.write("    mit dem " + att['attribute'] + "en" + str(att["activation"]) + "/\n")
            elif att['proposition'] == 'relpos':  # 4 possibilities: left, right, up, down
                if att['attribute'] == 'links' or att['attribute'] == 'rechts':
                    file_write.write("    mit dem " + att['attribute'][0:-1] + "en" +
                                     str(att['activation']) + "/\n")
                else:
                    file_write.write("    mit dem " + att['attribute'][0:-1] + "ren"
                                     + str(att["activation"]) + "/\n")
        if len(attributes) == 0:
            file_write.write("    so1.0/\n")
            # TODO: add gesture


def add_direction(entity, directions, file_write, mental_lexicon):
    if len([dir for dir in directions if dir['entity'] == entity['entity'] and
                                         mental_lexicon.contains_word(dir['attribute'])]) == 1:
        dir = [dir for dir in directions if dir['entity'] == entity['entity'] and
               mental_lexicon.contains_word(dir['attribute'])][0]

        file_write.write("$direction\n")
        file_write.write("    nach " + str(dir['attribute']) + "\n")
    elif len([dir for dir in directions if dir['entity'] == entity['entity'] and
              mental_lexicon.contains_concept(dir['attribute'])]) == 1:
        file_write.write("$direction\n")
        file_write.write("    nach da\n")
        # TODO: add gesture
