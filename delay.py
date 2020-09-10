import time
import random


def delay(x, y):
    print("running delay.\n")
    time.sleep(random.uniform(x, y))
