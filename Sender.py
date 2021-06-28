import ipaaca
import json
import ast

def main(input, lexicon):
    outBuffer = ipaaca.OutputBuffer("complanner")
    msg = ipaaca.IU("preverbal")
    input_as_json = []
    for i in input:
        as_json = ast.literal_eval(i)
        input_as_json.append(json.dumps(as_json))
    msg.payload = {
        "preverbal": "input",
        "event_complete": False,
        "input": input_as_json,
        "lexicon": lexicon
    }
    outBuffer.add(msg)
