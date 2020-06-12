from math import log2, log10
from random import randint

from base_station import *

class user_equipment(object):
    computing_capacity = [0.5, 0.8, 1.0]
    def __init__(self, id, x, y, bs, params):
        self.id = id
        self.x = x
        self.y = y
        self.bs = bs
        self.s = 0      # sub-carrier idx

        self.TX_POWER = params[0]
        self.UE_TX_POWER = params[1]
        self.AMPLIFIER = params[2]
        self.n0 = params[3]
        self.SUBCARRIER_BANDWIDTH = params[4]
        self.ALPHA = params[5]
        self.BETA = params[6]
        self.KAPA = params[7]
        self.LAMBDA = params[8]
        self.F_N = params[9]

        self.tx_power = self.set_power()
        self.computing_power = user_equipment.computing_capacity[randint(0, len(user_equipment.computing_capacity)-1)] * 10**9
    
    @staticmethod
    def pathloss(dist):
        return 15.3 + 37.6 * log10(dist)

    def set_power(self):
        dbm_tx_power = self.TX_POWER
        db_ps = user_equipment.pathloss(self.bs.dist_from_user(self))

        dbm_result_power = dbm_tx_power - db_ps

        return 10**(dbm_result_power/10)

    def dist_from_user(self, user):
        return ((self.x - user.x)**2 + (self.y - user.y)**2)**0.5
    
    def SINR(self):
        interference = self.n0
        for ue in self.bs.list_user:
            if ue == self:
                continue
            if ue.s == self.s and self.bs.dist_from_user(self) > self.bs.dist_from_user(ue):
                interference += ue.tx_power
        return self.tx_power / interference
    
    def data_rate(self):
        return self.SUBCARRIER_BANDWIDTH * log2(1 + self.SINR())
    
    def local_task_completion_time(self):
        return self.BETA/self.computing_power
    
    def local_energy_consumption(self):
        return self.KAPA*self.BETA*self.computing_power**2
    
    def local_computation_overhead(self):
        return self.LAMBDA*self.local_task_completion_time() + self.LAMBDA*self.local_energy_consumption()
    
    def remote_uplink_transmission_time(self):
        return self.ALPHA/self.data_rate()
    
    def remote_execution_time(self):
        return self.BETA/self.F_N
    
    def remote_energy_consumption(self):
        return self.UE_TX_POWER/self.AMPLIFIER * self.remote_uplink_transmission_time()
    
    def remote_computation_overhead(self):
        return self.LAMBDA*(self.remote_uplink_transmission_time() + self.remote_execution_time()) + self.LAMBDA*(self.remote_energy_consumption())
    
