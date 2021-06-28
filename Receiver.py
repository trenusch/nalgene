import sys
import time
import helper
import os
import string

import ipaaca
from main import run

class Receiver:
    def __init__(self, component):
        my_category_interests = ['preverbal']
        in_buffer = ipaaca.InputBuffer("commGoal", my_category_interests)
        in_buffer.register_handler(self.handle_input)


    def handle_input(self, iu, event_type, local):
        if event_type in ['ADDED', 'UPDATED', 'MESSAGE']:
            if iu.category == "preverbal":
                print (iu.category)
                print(u'Received payload: ' + unicode(iu.payload))
                run(iu.payload["input"], iu.payload["lexicon"])


def signal_handler(signal, frame):
    print ("Catched Ctrl+C! Shutting down sagaImageGenerator...")
    sys.exit(0)


def main(argv=None):
    keepThisComponentRunning = True
    component = "Receiver"
    if len(sys.argv) > 1:
        component = sys.argv[1]
    print ("starting ipaaca component ", component)


    RC = Receiver(component)



    while keepThisComponentRunning:
        time.sleep(1)  # sleep for some time



if __name__ == "__main__":
    sys.exit(main())
