import sys
import time
import const, helper
import os
import string

import ipaaca


class Receiver:
    def __init__(self, component):
        my_category_interests = ['preverbal']
        in_buffer = ipaaca.InputBuffer("commGoal", my_category_interests)
        in_buffer.register_handler(self.my_first_iu_handler)


    def my_first_iu_handler(self, iu, event_type, local):
        if event_type in ['ADDED', 'UPDATED', 'MESSAGE']:
            elif iu.category == "preverbal":
                print (iu.category)
                print(u'Received payload: ' + unicode(iu.payload))


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
        time.sleep(const.updateRate)  # sleep for some time



if __name__ == "__main__":
    sys.exit(main())