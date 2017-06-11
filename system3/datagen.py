#System packages
import numpy

#User Defined Packages
import Plane

#Global definitions

#Classes
class initiateplane:
    latitude = 28.580975
    longitude = 77.211001
    heading = 120
    newhead = 120
    altitude = 0
    speed = 0
    state = None
    def __init__(self,num):
        global traffic
        rand = numpy.random.random_integers
        if num == 1:
            self.state = 'taxi'
        else:
            if num <= traffic/2:
                self.state = 'taxi'
            else:
                if rand(0,10) > 5 :
                    self.state = 'inbound'
                else:
                    self.state = 'passby'
        if not self.state == 'taxi':
            self.latitude = 28.580975+(rand(-100,-1))*(-1)**rand(0,1)
            self.longitude = 77.211001+(rand(-100,-1))*(-1)**rand(0,1)
            self.altitude = rand(10000,20000)
            self.speed = rand(200,300)
            if self.longitude*self.latitude > 0:
                if self.longitude > 0:
                    self.heading = rand(180,270)
                    self.newhead = self.heading
                else:
                    self.heading = rand(0,90)
            else:
                if self.longitude > 0:
                    self.heading = rand(90,180)
                else:
                    self.heading = rand(270,360)
        else:
            self.newhead = rand(180,270)            
                    
    def getdata(self):
        return self.latitude,self.longitude,self.heading,self.newhead,self.altitude,self.state,self.speed
    
class generateset:
    pid = list()
    def __init__(self,total = None):
        global traffic
        traffic = total
        self.addplane()
    def addplane(self):
        rand = numpy.random.random_integers
        for i in xrange(traffic):
            self.pid.append('AI-%d%d%d'%(rand(1,9),rand(1,9),rand(1,9)))
