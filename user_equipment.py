from math import log2, log10
from random import randint

from params import *
from base_station import *

class user_equipment(object):
    computing_capacity = [0.5, 0.8, 1.0]
    def __init__(self, x, y, bs):
        self.x = x
        self.y = y
        self.bs = bs
        self.s = 0      # sub-carrier idx
        self.tx_power = self.set_power()
        self.computing_power = user_equipment.computing_capacity[randint(0, 2)]
    
    @staticmethod
    def pathloss(dist):
        return 15.3 + 37.6 * log10(dist)

    def set_power(self):
        dbm_tx_power = TX_POWER
        db_ps = user_equipment.pathloss(self.bs.dist_from_user(self))

        dbm_result_power = dbm_tx_power - db_ps
        print(dbm_result_power)

        return 10**(dbm_result_power/10)

    def dist_from_user(self, user):
        return ((self.x - user.x)**2 + (self.y - user.y)**2)**0.5
    
    def SINR(self):
        interference = n0
        for ue in self.bs.list_user:
            if ue == self:
                continue
            if ue.s == self.s and self.bs.dist_from_user(self) > self.bs.dist_from_user(ue):
                interference += ue.tx_power
        return self.tx_power / interference
    
    def data_rate(self):
        return SUBCARRIER_BANDWIDTH * log2(1 + self.SINR())
    
    def task_completion_time(self):
        return BETA/self.computing_power
    
    def energy_consumption(self):
        return BETA*self.computing_capacity**2