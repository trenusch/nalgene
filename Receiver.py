import sys
import time
import helper
import os
import string

import ipaaca

from application import produce_multiple
from mental_lexicon import MentalLexicon


class Receiver:
    def __init__(self, component, lexicon):
        my_category_interests = ['preverbal', 'lexicon']
        in_buffer = ipaaca.InputBuffer("commGoal", my_category_interests)
        in_buffer.register_handler(self.handle_input)
        self.lexicon = lexicon

    def handle_input(self, iu, event_type, local):
        if event_type in ['ADDED', 'UPDATED', 'MESSAGE']:
            if iu.category == "preverbal":
                #print (iu.category)
                #print(u'Received payload: ' + unicode(iu.payload))
                produce_multiple(iu.payload["input"], self.lexicon)
            elif iu.category == "lexicon":
                #print (iu.category)
                #print(u'Received payload: ' + unicode(iu.payload))
                self.lexicon.add_item(iu.payload["entry"])

def signal_handler(signal, frame):
    print ("Catched Ctrl+C! Shutting down sagaImageGenerator...")
    sys.exit(0)


def main(argv=None):
    keepThisComponentRunning = True
    component = "Receiver"
    if len(sys.argv) > 1:
        component = sys.argv[1]
    print ("starting ipaaca component ", component)

    lexicon = MentalLexicon()
    RC = Receiver(component, lexicon)

    while keepThisComponentRunning:
        time.sleep(1)  # sleep for some time


if __name__ == "__main__":
    sys.exit(main())
