import random

from params import *
from base_station import *
from user_equipment import *

def simulation():
    bs = base_station(X_CENTER, Y_CENTER)
    for _ in range(NUMBER_OF_UE):
        x, y = _, _
        while True:
            x = random.random() * 1000
            y = random.random() * 1000
            if RANGE_NO_DEPLOY < ((bs.x - x)**2 + (bs.y - y)**2)**0.5 < RANGE_BS_COMM:
                ue = user_equipment(x, y)
                bs.append_user(ue)
                break
    
    print(bs)
    print(bs.x, bs.y)
    print("=======")
    for ue in bs.list_user:
        print(ue)
        print(ue.x, ue.y)

if __name__ == "__main__":
    simulation()