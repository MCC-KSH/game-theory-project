from random import random, randint

from params import *
from base_station import *
from user_equipment import *

def simulation():
    bs = base_station(X_CENTER, Y_CENTER)
    list_ue_s = []
    ue_id = 0
    for _ in range(NUMBER_OF_UE):
        x, y = _, _
        while True:
            x = random() * 1000
            y = random() * 1000
            if RANGE_NO_DEPLOY < ((bs.x - x)**2 + (bs.y - y)**2)**0.5 < RANGE_BS_COMM:
                ue = user_equipment(ue_id, x, y, bs)
                ue.s = randint(0, NUMBER_OF_SUBCARRIER-1)
                bs.coalitions[ue.s].append(ue)
                list_ue_s.append(ue.s)
                bs.append_user(ue)
                ue_id += 1
                break

    LCO_result = []
    COO_result = []
    HOO_result = []
    PRO_result = []
    GOO_result = []

    # LCO
    bs.reset()
    for ue in bs.list_user:
        ue.s = NUMBER_OF_SUBCARRIER + ue.id
        bs.coalitions[ue.s].append(ue)
    
    for idx in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
        bs.utility_coalition(idx)
    
    print("########## LCO ##########")
    for i in range(NUMBER_OF_SUBCARRIER):
        LCO_result.append(bs.computation_overhead[i])
        print(bs.computation_overhead[i], end=" ")
    print()
    for i in range(NUMBER_OF_UE):
        LCO_result.append(bs.computation_overhead[NUMBER_OF_SUBCARRIER + i])
        print(bs.computation_overhead[NUMBER_OF_SUBCARRIER + i], end=" ")
    input("\nTYPE ANY WORD >> ")
    print('\n')

    # TODO COO
    bs.reset()
    for i in range(len(bs.list_user)):
        bs.list_user[i].s = list_ue_s[i]
        bs.coalitions[bs.list_user[i].s].append(bs.list_user[i])
    
    cnt_conv = 0
    while True:
        idx_ue = randint(0, NUMBER_OF_UE-1)
        ue = bs.list_user[idx_ue]
        idx_coalition = _
        while True:
            idx_coalition = randint(0, NUMBER_OF_SUBCARRIER-1)
            if ue.s != idx_coalition:
                break   
            
        if bs.preference(ue, idx_coalition):
            curr_coalition = ue.s
            bs.move(ue, idx_coalition)
            bs.utility_coalition(curr_coalition)
            bs.utility_coalition(idx_coalition)
            cnt_conv = 0
        else:
            cnt_conv += 1
    
        for idx in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
            bs.utility_coalition(idx)
        
        if cnt_conv == MAX_CNT:
            break
    
    print("########## COO ##########")
    for i in range(NUMBER_OF_SUBCARRIER):
        COO_result.append(bs.computation_overhead[i])
        print(bs.computation_overhead[i], end=" ")
    print()
    for i in range(NUMBER_OF_UE):
        COO_result.append(bs.computation_overhead[NUMBER_OF_SUBCARRIER + i])
        print(bs.computation_overhead[NUMBER_OF_SUBCARRIER + i], end=" ")
    input("\nTYPE ANY WORD >> ")
    print('\n')

    # TODO HOO
    bs.reset()
    for i in range(len(bs.list_user)):
        bs.list_user[i].s = list_ue_s[i]
        bs.coalitions[bs.list_user[i].s].append(bs.list_user[i])

    for ue in bs.list_user:
        if len(bs.coalitions[ue.s]) > 1:
            while True:
                move_coalition_idx = randint(-1, NUMBER_OF_SUBCARRIER-1)
                if move_coalition_idx < 0:
                    bs.move(ue, NUMBER_OF_SUBCARRIER + ue.id)
                    break
                if len(bs.coalitions[move_coalition_idx]) == 0:
                    bs.move(ue, move_coalition_idx)
                    break
    
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
        if idx_coalition == NUMBER_OF_SUBCARRIER + ue.id:
            sum_overhead_curr = sum(bs.computation_overhead)
            curr_coalition = ue.s
            bs.move(ue, idx_coalition)
            bs.utility_coalition(curr_coalition)
            bs.utility_coalition(idx_coalition)
            sum_overhead_move = sum(bs.computation_overhead)
            if sum_overhead_curr > sum_overhead_move:
                cnt_conv = 0
            else:
                bs.move(ue, curr_coalition)
                bs.utility_coalition(curr_coalition)
                bs.utility_coalition(idx_coalition)
                cnt_conv += 1
        else:
            if len(bs.coalitions[idx_coalition]) > 1:
                cnt_conv += 1
            else:                
                if bs.preference(ue, idx_coalition):
                    curr_coalition = ue.s
                    bs.move(ue, idx_coalition)
                    bs.utility_coalition(curr_coalition)
                    bs.utility_coalition(idx_coalition)
                    cnt_conv = 0
                else:
                    cnt_conv += 1
            
        for idx in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
            bs.utility_coalition(idx)
        
        if cnt_conv == MAX_CNT:
            break

    print("########## HOO ##########")
    for i in range(NUMBER_OF_SUBCARRIER):
        HOO_result.append(bs.computation_overhead[i])
        print(bs.computation_overhead[i], end=" ")
    print()
    for i in range(NUMBER_OF_UE):
        HOO_result.append(bs.computation_overhead[NUMBER_OF_SUBCARRIER + i])
        print(bs.computation_overhead[NUMBER_OF_SUBCARRIER + i], end=" ")
    input("\nTYPE ANY WORD >> ")
    print('\n')

    # Proposed Algorithm
    bs.reset()
    for i in range(len(bs.list_user)):
        bs.list_user[i].s = list_ue_s[i]
        bs.coalitions[bs.list_user[i].s].append(bs.list_user[i])

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
        if idx_coalition == NUMBER_OF_SUBCARRIER + ue.id:
            sum_overhead_curr = sum(bs.computation_overhead)
            curr_coalition = ue.s
            bs.move(ue, idx_coalition)
            bs.utility_coalition(curr_coalition)
            bs.utility_coalition(idx_coalition)
            sum_overhead_move = sum(bs.computation_overhead)
            if sum_overhead_curr > sum_overhead_move:
                cnt_conv = 0
            else:
                bs.move(ue, curr_coalition)
                bs.utility_coalition(curr_coalition)
                bs.utility_coalition(idx_coalition)
                cnt_conv += 1
        else:    
            if bs.preference(ue, idx_coalition):
                curr_coalition = ue.s
                bs.move(ue, idx_coalition)
                bs.utility_coalition(curr_coalition)
                bs.utility_coalition(idx_coalition)
                cnt_conv = 0
            else:
                cnt_conv += 1
        
        for idx in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
            bs.utility_coalition(idx)
        
        if cnt_conv == MAX_CNT:
            break

    print("########## PRO ##########")
    for i in range(NUMBER_OF_SUBCARRIER):
        PRO_result.append(bs.computation_overhead[i])
        print(bs.computation_overhead[i], end=" ")
    print()
    for i in range(NUMBER_OF_UE):
        PRO_result.append(bs.computation_overhead[NUMBER_OF_SUBCARRIER + i])
        print(bs.computation_overhead[NUMBER_OF_SUBCARRIER + i], end=" ")
    input("\nTYPE ANY WORD >> ")
    print('\n')

    # TODO GOO
    bs.reset()
    for i in range(len(bs.list_user)):
        bs.list_user[i].s = list_ue_s[i]
        bs.coalitions[bs.list_user[i].s].append(bs.list_user[i])

    print("########## GOO ##########")
    for i in range(NUMBER_OF_SUBCARRIER):
        GOO_result.append(bs.computation_overhead[i])
        print(bs.computation_overhead[i], end=" ")
    print()
    for i in range(NUMBER_OF_UE):
        GOO_result.append(bs.computation_overhead[NUMBER_OF_SUBCARRIER + i])
        print(bs.computation_overhead[NUMBER_OF_SUBCARRIER + i], end=" ")
    input("\nTYPE ANY WORD >> ")
    print('\n')

if __name__ == "__main__":
    simulation()