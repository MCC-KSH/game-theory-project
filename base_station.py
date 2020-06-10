from params import *
from user_equipment import *

class base_station(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.list_user = []
        self.coalitions = [[] for _ in range(NUMBER_OF_UE + NUMBER_OF_SUBCARRIER)]
        self.computation_overhead = [0 for _ in range(NUMBER_OF_UE + NUMBER_OF_SUBCARRIER)]
    
    def append_user(self, user):
        self.list_user.append(user)

    def dist_from_user(self, user):
        return ((self.x - user.x)**2 + (self.y - user.y)**2)**0.5
    
    def computation_offloading(self, idx):
        idx_coalition = 0
        for coalition in self.coalitions:
            sum_overhead = 0
            if idx_coalition >= NUMBER_OF_SUBCARRIER:
                break
            for ue in coalition:
                sum_overhead -= ue.remote_computation_overhead()
                sum_overhead += ue.local_computation_overhead()
            self.computation_overhead[idx_coalition] = sum_overhead
            idx_coalition += 1
        
    # def preference(self, ue):