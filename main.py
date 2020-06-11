from random import random, randint

from params import *
from base_station import *
from user_equipment import *

def simulation():
    bs = base_station(X_CENTER, Y_CENTER)
    ue_id = 0
    for _ in range(NUMBER_OF_UE):
        x, y = _, _
        while True:
            x = random() * 1000
            y = random() * 1000
            if RANGE_NO_DEPLOY < ((bs.x - x)**2 + (bs.y - y)**2)**0.5 < RANGE_BS_COMM:
                ue = user_equipment(ue_id, x, y, bs)
                ue.s = randint(0, NUMBER_OF_SUBCARRIER-1)
                bs.append_user(ue)
                ue_id += 1
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

    
    
    # Proposed Algorithm
    cnt_conv = 0
    while True:
        idx_ue = randint(0, NUMBER_OF_UE-1)
        ue = bs.list_user[idx_ue]
        idx_coalition = _
        while True:
            idx_coalition = randint(-1, NUMBER_OF_SUBCARRIER-1)
            if idx_coalition == -1:
                idx_coalition = NUMBER_OF_SUBCARRIER + ue.id
            if ue.s != idx_coalition:
                break
        if bs.preference(ue, idx_coalition):
            bs.move(ue, idx_coalition)
            cnt_conv = 0
        else:
            cnt_conv += 1
        
        for idx in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
            bs.utility_coalition(idx)
        
        if cnt_conv == MAX_CNT:
            break

    for i in range(NUMBER_OF_SUBCARRIER):
        print(bs.computation_overhead[i], end=" ")
    print()
    for i in range(NUMBER_OF_UE):
        print(bs.computation_overhead[NUMBER_OF_SUBCARRIER + i], end=" ")
    print()

if __name__ == "__main__":
    simulation()