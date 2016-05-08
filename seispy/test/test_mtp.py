import time

import mtp
from mtp import PoisonPill


def inputter(input_q, *args, **kwargs):
    j = 0
    for i in range(30):
        input_q.put(i)
        if j % 10 == 0:
            time.sleep(2.5)
        j += 1
    input_q.put(PoisonPill())

def processor(obj):
    return obj * 3.6539

def outputter(output_q, *args, **kwargs):
    while True:
        obj = output_q.get()
        if isinstance(obj, mtp.PoisonPill):
            return
        else:
            print obj, type(obj)
        time.sleep(0.125)

my_mtp = mtp.MultiThreadedProcessor(inputter, processor, outputter)
my_mtp.start()
