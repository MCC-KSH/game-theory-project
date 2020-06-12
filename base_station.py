from user_equipment import *

class base_station(object):
    def __init__(self, x, y, params):
        self.NUMBER_OF_UE = params[0]
        self.NUMBER_OF_SUBCARRIER = params[1]
        self.x = x
        self.y = y
        self.list_user = []
        self.coalitions = [[] for _ in range(self.NUMBER_OF_UE + self.NUMBER_OF_SUBCARRIER)]
        self.computation_overhead = [0 for _ in range(self.NUMBER_OF_UE + self.NUMBER_OF_SUBCARRIER)]

    def reset(self):
        self.coalitions = [[] for _ in range(self.NUMBER_OF_UE + self.NUMBER_OF_SUBCARRIER)]
        self.computation_overhead = [0 for _ in range(self.NUMBER_OF_UE + self.NUMBER_OF_SUBCARRIER)]

    def append_user(self, user):
        self.list_user.append(user)

    def dist_from_user(self, user):
        return ((self.x - user.x)**2 + (self.y - user.y)**2)**0.5
    
    def utility_coalition(self, idx):
        if idx >= self.NUMBER_OF_SUBCARRIER:
            sum_overhead = 0
            for ue in self.coalitions[idx]:
                sum_overhead += ue.local_computation_overhead()
            self.computation_overhead[idx] = sum_overhead
            return 0
        sum_overhead = 0
        sum_utility = 0
        for ue in self.coalitions[idx]:
            sum_overhead += ue.remote_computation_overhead()
            sum_utility += ue.local_computation_overhead() - ue.remote_computation_overhead()
        self.computation_overhead[idx] = sum_overhead
        return sum_utility
        
        
    def preference(self, ue, coalition):
        curr_coalition = ue.s
        
        ue.s = coalition
        self.coalitions[curr_coalition].remove(ue)
        utility_s = self.utility_coalition(curr_coalition)

        self.coalitions[coalition].append(ue)
        utility_k_n = self.utility_coalition(coalition)

        self.coalitions[coalition].remove(ue)
        self.coalitions[curr_coalition].append(ue)
        ue.s = curr_coalition

        utility_s_n = self.utility_coalition(curr_coalition)
        utility_k = self.utility_coalition(coalition)

        if utility_k < 0 or utility_s < 0 or utility_k_n < 0 or utility_s_n < 0:
            return False
        
        return utility_s_n + utility_k < utility_s + utility_k_n
    
    def move(self, ue, coalition):
        curr_coalition = ue.s
        self.coalitions[curr_coalition].remove(ue)
        self.coalitions[coalition].append(ue)
        ue.s = coalition