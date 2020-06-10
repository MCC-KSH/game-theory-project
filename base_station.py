from params import *
from user_equipment import *

class base_station(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.list_user = []
    
    def append_user(self, user):
        self.list_user.append(user)

    def dist_from_user(self, user):
        return ((self.x - user.x)**2 + (self.y - user.y)**2)**0.5