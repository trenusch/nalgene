import ipaaca
import json
import ast

if __name__ == '__main__':
    outBuffer = ipaaca.OutputBuffer("complanner")
    msg = ipaaca.IU("lexicon")
    msg.payload = {"entry": "Subject(\"m\", \"hund\", True)"}
    outBuffer.add(msg)

    msg = ipaaca.IU("lexicon")
    msg.payload = {"entry": "Action(\"nehmen\", \"genommen\", True)"}
    outBuffer.add(msg)

    msg = ipaaca.IU("lexicon")
    msg.payload = {"entry": "Entity(\"m\", \"loeffel\", False)"}
    outBuffer.add(msg)

    msg = ipaaca.IU("preverbal")
    input_as_json = []
    dog_in = {"proposition": "subject",
              "subject": "hund",
              "attribute": "-",
              "entity": "loeffel",
              "action": "nehmen",
              "activation": 2.4,
              "infostate": "new"}
    loeffel_in = {"proposition": "entity",
                  "entity": "loeffel",
                  "activation": 2.0}

    input_as_json.append(json.dumps(dog_in))
    input_as_json.append(json.dumps(loeffel_in))
    msg.payload = {"input": input_as_json}
    outBuffer.add(msg)
