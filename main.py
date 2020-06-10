from random import random, randint

from params import *
from base_station import *
from user_equipment import *

def simulation():
    bs = base_station(X_CENTER, Y_CENTER)
    for _ in range(NUMBER_OF_UE):
        x, y = _, _
        while True:
            x = random() * 1000
            y = random() * 1000
            if RANGE_NO_DEPLOY < ((bs.x - x)**2 + (bs.y - y)**2)**0.5 < RANGE_BS_COMM:
                ue = user_equipment(x, y, bs)
                ue.s = randint(0, NUMBER_OF_SUBCARRIER-1)   # TODO this is random method
                bs.append_user(ue)
                break
    
    print(bs)
    print(bs.x, bs.y)
    print("=======")
    for ue in bs.list_user:
        print(ue)
        print(ue.x, ue.y, bs.dist_from_user(ue), ue.s, ue.SINR(), ue.data_rate()/(1024))
        print(ue.local_task_completion_time(), ue.local_energy_consumption(), ue.local_computation_overhead())
        print(ue.remote_uplink_transmission_time(), ue.remote_execution_time(), ue.remote_energy_consumption(), ue.remote_computation_overhead())
    
    for ue in bs.list_user:
        bs.coalitions[ue.s].append(ue)

    # TODO coalition game based algorithm
    for idx in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
        bs.computation_offloading(idx)

    for overhead in bs.computation_overhead:
        print(overhead)

if __name__ == "__main__":
    simulation()