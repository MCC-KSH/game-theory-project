from random import random, randint

from params import *
from base_station import *
from user_equipment import *

def simulation():
    bs_params = [NUMBER_OF_UE, NUMBER_OF_SUBCARRIER]
    ue_params = [TX_POWER, UE_TX_POWER, AMPLIFIER, n0, SUBCARRIER_BANDWIDTH, ALPHA, BETA, KAPA, LAMBDA, F_N]
    
    bs = base_station(X_CENTER, Y_CENTER, bs_params)
    list_ue_s = []
    ue_id = 0
    for _ in range(NUMBER_OF_UE):
        x, y = _, _
        while True:
            x = random() * 1000
            y = random() * 1000
            if RANGE_NO_DEPLOY < ((bs.x - x)**2 + (bs.y - y)**2)**0.5 < RANGE_BS_COMM:
                ue = user_equipment(ue_id, x, y, bs, ue_params)
                ue.s = randint(0, NUMBER_OF_SUBCARRIER-1)
                bs.coalitions[ue.s].append(ue)
                list_ue_s.append(ue.s)
                bs.append_user(ue)
                ue_id += 1
                break

    LCO_result = [0, 0, 0, 0, 0]
    COO_result = [0, 0, 0, 0, 0]
    HOO_result = [0, 0, 0, 0, 0]
    PRO_result = [0, 0, 0, 0, 0]
    GOO_result = [0, 0, 0, 0, 0]

    # LCO
    bs.reset()
    for ue in bs.list_user:
        ue.s = NUMBER_OF_SUBCARRIER + ue.id
        bs.coalitions[ue.s].append(ue)
    
    for idx in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
        bs.utility_coalition(idx)
    
    LCO_result[0] = sum(bs.computation_overhead)
    LCO_result[1] = bs.computation_overhead[NUMBER_OF_SUBCARRIER:].count(0) / NUMBER_OF_UE
    for i in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
        LCO_result[2] += bs.utility_coalition(i)

    # COO
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
        
        COO_result[4] += 1

        if bs.preference(ue, idx_coalition):
            sum_overhead_curr = sum(bs.computation_overhead)
            curr_coalition = ue.s
            
            bs.move(ue, idx_coalition)
            bs.utility_coalition(curr_coalition)
            bs.utility_coalition(idx_coalition)

            sum_overhead_move = sum(bs.computation_overhead)
            
            if sum_overhead_curr > sum_overhead_move:            
                cnt_conv = 0
                COO_result[3] += 1
            else:
                bs.move(ue, curr_coalition)
                bs.utility_coalition(curr_coalition)
                bs.utility_coalition(idx_coalition)
                cnt_conv += 1
        else:
            cnt_conv += 1
    
        for idx in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
            bs.utility_coalition(idx)
        
        if cnt_conv == MAX_CNT:
            break
    
    COO_result[0] = sum(bs.computation_overhead)
    COO_result[1] = bs.computation_overhead[NUMBER_OF_SUBCARRIER:].count(0) / NUMBER_OF_UE
    for i in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
        COO_result[2] += bs.utility_coalition(i)

    # HOO
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
        
        HOO_result[4] += 1

        if idx_coalition == NUMBER_OF_SUBCARRIER + ue.id:
            sum_overhead_curr = sum(bs.computation_overhead)
            curr_coalition = ue.s
            bs.move(ue, idx_coalition)
            bs.utility_coalition(curr_coalition)
            bs.utility_coalition(idx_coalition)
            sum_overhead_move = sum(bs.computation_overhead)
            if sum_overhead_curr > sum_overhead_move:
                cnt_conv = 0
                HOO_result[3] += 1
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
                    sum_overhead_curr = sum(bs.computation_overhead)
                    curr_coalition = ue.s
                    
                    bs.move(ue, idx_coalition)
                    bs.utility_coalition(curr_coalition)
                    bs.utility_coalition(idx_coalition)

                    sum_overhead_move = sum(bs.computation_overhead)
                    
                    if sum_overhead_curr > sum_overhead_move:            
                        cnt_conv = 0
                        HOO_result[3] += 1
                    else:
                        bs.move(ue, curr_coalition)
                        bs.utility_coalition(curr_coalition)
                        bs.utility_coalition(idx_coalition)
                        cnt_conv += 1
            
        for idx in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
            bs.utility_coalition(idx)
        
        if cnt_conv == MAX_CNT:
            break

    HOO_result[0] = sum(bs.computation_overhead)
    HOO_result[1] = bs.computation_overhead[NUMBER_OF_SUBCARRIER:].count(0) / NUMBER_OF_UE
    for i in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
        HOO_result[2] += bs.utility_coalition(i)

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
        
        PRO_result[4] += 1
        
        if idx_coalition == NUMBER_OF_SUBCARRIER + ue.id:
            sum_overhead_curr = sum(bs.computation_overhead)
            curr_coalition = ue.s
            bs.move(ue, idx_coalition)
            bs.utility_coalition(curr_coalition)
            bs.utility_coalition(idx_coalition)
            sum_overhead_move = sum(bs.computation_overhead)
            if sum_overhead_curr > sum_overhead_move:
                cnt_conv = 0
                PRO_result[3] += 1
            else:
                bs.move(ue, curr_coalition)
                bs.utility_coalition(curr_coalition)
                bs.utility_coalition(idx_coalition)
                cnt_conv += 1
        else:    
            if bs.preference(ue, idx_coalition):
                sum_overhead_curr = sum(bs.computation_overhead)
                curr_coalition = ue.s
                
                bs.move(ue, idx_coalition)
                bs.utility_coalition(curr_coalition)
                bs.utility_coalition(idx_coalition)

                sum_overhead_move = sum(bs.computation_overhead)
                
                if sum_overhead_curr > sum_overhead_move:            
                    cnt_conv = 0
                    PRO_result[3] += 1
                else:
                    bs.move(ue, curr_coalition)
                    bs.utility_coalition(curr_coalition)
                    bs.utility_coalition(idx_coalition)
                    cnt_conv += 1
        
        for idx in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
            bs.utility_coalition(idx)
        
        if cnt_conv == MAX_CNT:
            break

    PRO_result[0] = sum(bs.computation_overhead)
    PRO_result[1] = bs.computation_overhead[NUMBER_OF_SUBCARRIER:].count(0) / NUMBER_OF_UE
    for i in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
        PRO_result[2] += bs.utility_coalition(i)

    # GOO
    channel_stat = []

    bs.reset()
    for ue in bs.list_user:
        ue.s = NUMBER_OF_SUBCARRIER + ue.id
        bs.coalitions[ue.s].append(ue)
        channel_stat.append((ue.data_rate(), ue))

    channel_stat.sort()

    for t_ue in channel_stat:
        ue = t_ue[1]
        curr_coalition = ue.s
        bs.utility_coalition(curr_coalition)
        min_overhead = bs.computation_overhead[curr_coalition]
        for s in range(NUMBER_OF_SUBCARRIER):
            GOO_result[4] += 1

            if bs.preference(ue, s):
                bs.move(ue, s)
                bs.utility_coalition(s)
                bs.utility_coalition(curr_coalition)
                move_overhead = bs.computation_overhead[ue.s]
                if move_overhead < min_overhead:
                    min_overhead = move_overhead
                    curr_coalition = ue.s
                    GOO_result[3] += 1
                else:
                    bs.move(ue, curr_coalition)
                    bs.utility_coalition(s)
                    bs.utility_coalition(curr_coalition)

    GOO_result[0] = sum(bs.computation_overhead)
    GOO_result[1] = bs.computation_overhead[NUMBER_OF_SUBCARRIER:].count(0) / NUMBER_OF_UE
    for i in range(NUMBER_OF_SUBCARRIER + NUMBER_OF_UE):
        GOO_result[2] += bs.utility_coalition(i)

    print(" ".join(str(data) for data in LCO_result))
    print(" ".join(str(data) for data in COO_result))
    print(" ".join(str(data) for data in HOO_result))
    print(" ".join(str(data) for data in PRO_result))
    print(" ".join(str(data) for data in GOO_result))

if __name__ == "__main__":
    global NUMBER_OF_UE, NUMBER_OF_SUBCARRIER, TX_POWER, UE_TX_POWER
    NUMBER_OF_UE = 300
    NUMBER_OF_SUBCARRIER = 15
    simulation()