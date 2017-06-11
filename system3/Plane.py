#System packages
from __future__ import division
import numpy

#User Defined Packages
from datagen import initiateplane
from channel import channel

#Global definitions
pi = 3.146

#Classes
class Plane:
    name = None
    num = None
    query = 'NULL'
    latitude = 0
    longitude = 0
    heading = 120
    newhead = 120
    altitude = 0
    speed = 0
    state = None
    collision = 0
    distance = 0
    def __init__(self,name,num):
        self.num = num
        self.name = name
        init = initiateplane(self.num+1)
        self.latitude,self.longitude,self.heading,self.newhead,self.altitude,self.state,self.speed = init.getdata()
    def changealtitude (self,alt2):
        if abs(self.altitude-alt2) < int(self.speed/50):
            fact = 1
        else:
            fact = int(self.speed/50)
        self.altitude += 2*fact if (self.altitude<alt2) else -2*fact
    def changeheading (self,head2):
        if abs(head2-self.heading)<=180:
            self.heading += 1 if not (self.heading>head2) else -1
        else:
            if self.heading>head2:
                self.heading = 0 if (self.heading==360) else self.heading+1
            else:
                self.heading = 360 if (self.heading==0) else self.heading-1
    def changespeed (self,new):
        if self.state == 'taxi':
            return
        if self.speed == 0:
            self.speed = 1
        if abs(self.speed-new) < (self.speed*1.5):
            self.speed = new
            return
        if new > self.speed and not self.speed == 1:
            self.speed += self.speed*0.5
        elif new > self.speed and self.speed == 1:
            self.speed += self.speed
        else:
            self.speed -= self.speed*0.5
        self.speed = int(self.speed)
    def getlatitude (self,head):
        self.latitude += numpy.cos(-1*head*pi/180)/10000*self.speed if not (self.state == 'taxi') else 0
        '''
        if self.latitude<-90:
            self.heading -= 180 if self.heading>180 else -180
        elif self.latitude>90:
            self.heading += 180 if self.heading<180 else -180
        else:
            pass
        '''
    def getlongitude (self,head):
        self.longitude += numpy.sin(-1*head*pi/180)/10000*self.speed if not (self.state == 'taxi') else 0
        '''
        if self.longitude<-180:
            self.longitude += 360
        elif self.longitude>180:
            self.longitude -= 360
        else:
            pass
        '''
    def getdistance(self):
        self.distance = ((((self.latitude-28.580975)*69)**2 + ((self.longitude-77.211007)*69)**2)**0.5)
        return self.distance
    def getquery(self):
        ch = channel()
        self.query = ch.getquery(self.name)
    def acknowledge(self):
        return 0 if not (self.query == 'NULL') else 1
