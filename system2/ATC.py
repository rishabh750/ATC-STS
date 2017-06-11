#System packages

#User Defined Packages
from channel import channel
import Plane

#Global definitions

#Classes
class ATC:
    name = 'TOWER'
    query = 'NULL'
    latitude = 28.580975
    longitude = 77.211001
    heading = 12
    altitude = 0
    state = None
    collision = 0 
    def __init__(self):
        pass
    def getquery(self):
        ch = channel()
        self.query = ch.getquery(self.name)
    def acknowledge(self):
        return 0 if not (self.query == 'NULL') else 1
