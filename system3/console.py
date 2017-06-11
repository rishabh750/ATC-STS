#System packages
import os
import platform
import time as t
import msvcrt
from tabulate import tabulate

#User Defined Packages
from channel import channel
from analyser import analysquery
from collision import checkcollision,updatecluster
import audio
from ATC import ATC

#Global definitions

#Classes
class console:
    def __init__(self,planes):
    	cl = 'cls' if (platform.system() == 'Windows') else 'clear'
        clear = lambda: os.system(cl)
        clear()
        ch = channel()
        atc = ATC()
        timestamp = 0
        traffic = len(planes)
        rrtimer = 0
        while True:
        	timestamp += 1
        	print tabulate(map(self.new,planes), headers=['Name','State','Latitude','Longitude','Distance','Altitude','Heading','Speed','Query','Acknowledged','Collision'])
        	query = ''
        	if msvcrt.kbhit():
        		key = msvcrt.getch()
        		if (key == 'q') or (key == 'Q'):
        			clear()
        			exit()
        	if timestamp == 5:
        		if rrtimer == traffic-1:
        			rrtimer = 0
        		atc.command(planes[rrtimer])
        		rrtimer += 1
        		timestamp = 0
        	ch.printlast()
        	t.sleep(1)
        	clear()
            
    def new(self,plane):
        if plane.name == 'TOWER':
            plane.getquery()
            return plane.name,plane.state,plane.latitude,plane.longitude,0,plane.altitude,plane.heading,0,plane.query,plane.acknowledge(),0
    	ch = channel()
    	ack = plane.acknowledge()
        if (plane.state == 'taxi') or (plane.state == 'takeoff'):
            plane.getlatitude(120)
            plane.getlongitude(120)
        else:
            if not (plane.newhead == plane.heading):
                plane.changeheading(plane.newhead)
            plane.getlatitude(plane.heading)
            plane.getlongitude(plane.heading)
        dist = plane.getdistance()
        if dist < 0.001 :
            dist = 0
        updatecluster(plane)
        analys = analysquery()
        new,attr = analys.analysquery(plane)
        if not ack:
            if new:
                if attr == 'H':
                    plane.changeheading(new)
                elif attr == 'A':
                    plane.changealtitude(new)
                elif attr == 'S':
                    plane.changespeed(new)
                elif attr == 'T':
                    if plane.speed >= 150:
                        if (not plane.heading == new%1000) and plane.altitude > 200:
                            plane.changeheading(new%1000)
                        if not plane.altitude == new/1000:
                            plane.changealtitude(new/1000)       
            else:
                ch.clearchannel()
                plane.getquery()
        else:
        	plane.getquery()
        return plane.name,plane.state,plane.latitude,plane.longitude,dist,plane.altitude,plane.heading,plane.speed,plane.query,ack,checkcollision(plane)


