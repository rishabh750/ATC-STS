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
    def command(self,plane):
        #print 'hello',plane.name,plane.latitude,plane.longitude,plane.heading,plane.altitude
        ch = channel()
        if plane.state == 'taxi' and not ch.getrunway():
            ch.sendquery(plane.name+' takeoff')
            ch.lockrunway()
            return
        elif plane.state == 'takeoff' and plane.altitude >= 3000 and ch.getrunway():
            plane.state = 'outound'
            ch.releaserunway()
            return
        elif plane.state == 'inbound' and plane.distance <= 100:
            if ch.getrunway():
                print 'goarround'
            else:
                ch.lockrunway()
        ch.sendquery(plane.name+' hello')
        #ch.sendquery(plane.name+' '+query)
