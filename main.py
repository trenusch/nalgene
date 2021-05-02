from generate import *

"""
    method called by the system
    input: list of json-objects
"""


def produce_utterance(input):
    part_of = [json.loads(item) for item in input if json.loads(item)["proposition"] == "part_of"]
    property = [json.loads(item) for item in input if json.loads(item)["proposition"] == "property"]
    relpos = [json.loads(item) for item in input if json.loads(item)["proposition"] == "relpos"]

    if len(part_of) + len(property) + len(relpos) == 0:
        write(input)
    else:
        write_obj(input)


def write(input):
    file = open("examples/subj.nlg", "r")
    file_write = open("examples/subj_complete.nlg", "w")
    for line in file:
        file_write.write(line)
        if line.startswith("%Subjekt"):
            sub = [json.loads(item) for item in input if json.loads(item)["proposition"] == "subject"]
            if sub[0]["infostate"] == "new":
                file_write.write("    " + sub[0]["subject"])
            else:
                file_write.write("    er")
        elif line.startswith("~Praedikat"):
            sub = [json.loads(item) for item in input if json.loads(item)["proposition"] == "subject"]
            file_write.write("    " + sub[0]["action"])
        elif line.startswith("%Objekt"):
            obj = [json.loads(item) for item in input if json.loads(item)["proposition"] == "entity"]
            file_write.write("    " + obj[0]["entity"])

    file_write.close()
    file.close()

    filename = os.path.realpath("examples/subj_complete.nlg")
    base_dir = os.path.dirname(filename)
    filename = os.path.basename(filename)
    generate_from_file(base_dir, filename)  # , root_context)


def write_obj(input):
    file = open("examples/subj_obj.nlg", "r")
    file_write = open("examples/subj_obj_complete.nlg", "w")
    object = ""
    for line in file:
        file_write.write(line)
        if line.startswith("%Subjekt"):
            sub = [json.loads(item) for item in input if json.loads(item)["proposition"] == "subject"]
            if sub[0]["infostate"] == "new":
                file_write.write("    " + sub[0]["subject"])
            else:
                file_write.write("    er")
        elif line.startswith("~Praedikat"):
            sub = [json.loads(item) for item in input if json.loads(item)["proposition"] == "subject"]
            file_write.write("    " + sub[0]["action"])
        elif line.startswith("%Objekt"):
            obj = [json.loads(item) for item in input if json.loads(item)["proposition"] == "entity"]
            rel_obj = [json.loads(item) for item in input if
                       json.loads(item)["proposition"] == "part_of" or
                       json.loads(item)["proposition"] == "relpos" or
                       json.loads(item)["proposition"] == "property"]
            obj = [item for item in obj if item["entity"] not in [e["entity"] for e in rel_obj]]
            object = obj[0]["entity"]
            file_write.write("    " + object + "?")
        elif line.startswith("%Ortsergaenzung"):
            part_of = [json.loads(item) for item in input if json.loads(item)["proposition"] == "part_of" and
                       json.loads(item)["rel_entity"] == object]
            property = [json.loads(item) for item in input if json.loads(item)["proposition"] == "property" and
                        json.loads(item)["rel_entity"] == object]
            relpos = [json.loads(item) for item in input if json.loads(item)["proposition"] == "relpos" and
                      json.loads(item)["rel_entity"] == object]
            for item in property + relpos:
                file_write.write("    " + item["attribute"] + str(item["activation"]) + "/" + "\n")
            if len(property + relpos) == 0:
                for item in part_of:
                    file_write.write("    " + item["entity"] + "1./" + "\n")

    file_write.close()
    file.close()

    filename = os.path.realpath("examples/subj_obj_complete.nlg")
    base_dir = os.path.dirname(filename)
    filename = os.path.basename(filename)
    generate_from_file(base_dir, filename)  # , root_context)


if __name__ == '__main__':
    # specify input of the system
    input = []

    dog = {"proposition": "subject",
           "subject": "hund",
           "attribute": "-",
           "action": "nehmen",
           "entity": "loeffel",
           "activation": 2.4,
           "infostate": "new"}

    loeffel = {"proposition": "entity",
               "entity": "loeffel",
               "activation": 1.99}

    laffe = {"proposition": "entity",
             "entity": "laffe",
             "activation": 2.01}

    relation = {"proposition": "part_of",
                "entity": "laffe",
                "rel_entity": "loeffel",
                "activation": 1.99}

    attribute = {"proposition": "property",
                 "entity": "laffe",
                 "rel_entity": "loeffel",
                 "attribute": "rund",
                 "activation": 4.00}
    attribute2 = {"proposition": "property",
                 "entity": "laffe",
                 "rel_entity": "loeffel",
                 "attribute": "gewölbt",
                 "activation": 3.00}

    relpos = {"proposition": "relpos",
              "entity": "laffe",
              "rel_entity": "loeffel",
              "attribute": "unten",
              "activation": 4.00}

input.append(json.dumps(dog))
input.append(json.dumps(loeffel))
input.append(json.dumps(laffe))
input.append(json.dumps(relation))
#input.append(json.dumps(attribute))
#input.append(json.dumps(attribute2))
#input.append(json.dumps(relpos))
produce_utterance(input)
