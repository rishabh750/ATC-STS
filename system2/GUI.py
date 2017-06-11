#System packages
import pygame
import numpy
from pygame.locals import *
import time as t
from tabulate import tabulate

#User Defined Packages
import audio
from ATC import ATC
from channel import channel
from analyser import analysquery
from collision import checkcollision,updatecluster

#Global definitions
pi = 3.146

#Classes
class gui:
	i = list()
	j = list()
	resx = 0
	resy = 0
	cenx = 0
	ceny = 0
	screen = None
	scroll = 0
	zoom = 10
	def __init__(self):
		pygame.init()
		res = max(pygame.display.list_modes())
		self.resx = res[0]
		self.resy = res[1]
		self.cenx = self.resx/2-200
		self.ceny = self.resy/2
		self.screen = pygame.display.set_mode(res,pygame.FULLSCREEN)
	def scalex(self,lon):
		return (self.cenx+((77.211001-lon)*8*self.zoom)/21)
	def scaley(self,lat):
		return (self.ceny+((28.580975-lat)*8*self.zoom)/21)
	def plot(self,a,b,alt,name,state,collision):
		if name == 'TOWER' or state == 'taxi':
			return
		elif state == 'passby':
			pygame.draw.rect(self.screen, (0,0,204), pygame.Rect(a, b, 5,5))
		elif state == 'takeoff':
			pygame.draw.rect(self.screen, (204,0,0), pygame.Rect(a, b, 5,5))
		else:
			pygame.draw.rect(self.screen, (0,204,0), pygame.Rect(a, b, 5,5))
		text = pygame.font.SysFont('arial',20)
		text = text.render(name, True, (0, 128, 0))
		self.screen.blit(text,(a+5,b-20))
		if collision == 1:
			pygame.draw.circle(self.screen,(30,30,30),(self.cenx,self.ceny),self.zoom,1)
		elif collision == 2:
			pygame.draw.circle(self.screen,(30,0,0),(self.cenx,self.ceny),self.zoom,1)
	def panel(self):
		pygame.draw.rect(self.screen,(0,204,0), pygame.Rect(self.resx-405,0,405,self.resy))
		pygame.draw.rect(self.screen,(0,51,0), pygame.Rect(self.resx-400,0,400,self.resy))
	def panelitems(self,plane,pos):
		if plane.name == 'TOWER':
			return
		text = pygame.font.SysFont('impact',30)
		if plane.query == 'NULL':
			text = text.render(plane.name, True, (0, 150, 0))
		else:
			text = text.render(plane.name, True, (100, 150, 100))
		self.screen.blit(text,(self.resx-400,100+150*(pos+1)-200*self.scroll))
		text1 = pygame.font.SysFont('arial',20)
		text2 = text3 = text4 = text5 = text6 = text1
		text1 = text1.render('Lat:'+str(plane.latitude), True, (0, 0, 0))
		self.screen.blit(text1,(self.resx-300,100+150*(pos+1)-200*self.scroll))
		text2 = text2.render('Lon:'+str(plane.longitude), True, (0, 0, 0))
		self.screen.blit(text2,(self.resx-300,120+150*(pos+1)-200*self.scroll))
		text3 = text3.render('Alt:'+str(plane.altitude), True, (0, 0, 0))
		self.screen.blit(text3,(self.resx-300,140+150*(pos+1)-200*self.scroll))
		text4 = text4.render('Hdg:'+str(plane.heading), True, (0, 0, 0))
		self.screen.blit(text4,(self.resx-300,160+150*(pos+1)-200*self.scroll))
		text5 = text5.render('Spd:'+str(plane.speed), True, (0, 0, 0))
		self.screen.blit(text5,(self.resx-300,180+150*(pos+1)-200*self.scroll))
		text6 = text6.render('Dst:'+str(plane.distance), True, (0, 0, 0))
		self.screen.blit(text6,(self.resx-300,200+150*(pos+1)-200*self.scroll))
	def terrain(self):
		for i in xrange(30):
			pygame.draw.line(self.screen,(0,30,0),(self.cenx-(5*i*self.zoom),0),(self.cenx-(5*i*self.zoom),self.resy),1)
			pygame.draw.line(self.screen,(0,30,0),(0,self.ceny-(5*i*self.zoom)),(self.resx,self.ceny-(5*i*self.zoom)),1)
			pygame.draw.line(self.screen,(0,30,0),(self.cenx+(5*i*self.zoom),0),(self.cenx+(5*i*self.zoom),self.resy),1)
			pygame.draw.line(self.screen,(0,30,0),(0,self.ceny+(5*i*self.zoom)),(self.resx,self.ceny+(5*i*self.zoom)),1)
		for i in xrange(30):
			pygame.draw.circle(self.screen,(0,30,0),(self.cenx,self.ceny),5*(i+1)*self.zoom,1)
		i = 1
		while i<40:
			pygame.draw.circle(self.screen,(0,204,0),(self.cenx,self.ceny),10*i*self.zoom,1)
			i *= 2
		ch =channel()
		if not ch.getrunway():
			pygame.draw.line(self.screen,(0,204,0),(self.cenx-0.43*self.zoom*numpy.sin(60*pi/180),self.ceny-0.43*self.zoom*numpy.cos(60*pi/180)),(self.cenx+0.43*self.zoom*numpy.sin(60*pi/180),self.ceny+0.43*self.zoom*numpy.cos(60*pi/180)),3)
		else:
			pygame.draw.line(self.screen,(204,0,0),(self.cenx-0.43*self.zoom*numpy.sin(60*pi/180),self.ceny-0.43*self.zoom*numpy.cos(60*pi/180)),(self.cenx+0.43*self.zoom*numpy.sin(60*pi/180),self.ceny+0.43*self.zoom*numpy.cos(60*pi/180)),3)
	def predictor(self,plane):
		if plane.state == 'taxi' or plane.name == 'TOWER':
			return
		lat = plane.latitude
		lon = plane.longitude
		lat = self.scaley(lat)
		lon = self.scalex(lon)
		head = plane.heading
		nhead = plane.newhead
		pygame.draw.line(self.screen,(100,0,0),(lon,lat),(lon-self.zoom*numpy.sin(-1*nhead*pi/180),lat-self.zoom*numpy.cos(-1*head*pi/180)),1)
		#present heading
		pygame.draw.line(self.screen,(0,100,0),(lon,lat),(lon-self.zoom*numpy.sin(-1*head*pi/180),lat-self.zoom*numpy.cos(head*pi/180)),1)
		#expected heading
		if plane.state == 'inbound':
			pygame.draw.line(self.screen,(0,0,100),(lon,lat),(lon-self.zoom*numpy.sin(head*pi/180),lat-self.zoom*numpy.cos(head*pi/180)),1)
	def gui(self,planes):
		done = False
		ch = channel()
		while not done:
			self.screen.fill((0,20,0))
			temp = map(self.new,planes)
			name = [x[0] for x in temp]
			state = [x[1] for x in temp]
			lat = [x[2] for x in temp]
			lon = [x[3] for x in temp]
			alt = [x[4] for x in temp]
			head = [x[5] for x in temp]
			collision  = [x[10] for x in temp]
			lat = map(self.scaley,lat)
			lon = map(self.scalex,lon)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and ((event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE)):
					done = True
				#move map
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP2:
					self.ceny -= 50 if self.ceny >= 200 else 0
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP8:
					self.ceny += 50 if self.ceny <= self.resy-200 else 0
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP6:
					self.cenx -= 50 if self.cenx >= 200 else 0
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP4:
					self.cenx += 50 if self.cenx <= self.resx-200 else 0
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP5:
					self.cenx = self.resx/2-200
					self.ceny = self.resy/2
				#zoom
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP7:
					self.zoom += 5 if self.zoom <= 90 else 0
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP1:
					self.zoom -= 5 if self.zoom > 5 else 0
				#panel scroll
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP3:
					self.scroll += 1 if not self.scroll > (len(planes)-9) else 0
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP9:
					self.scroll -= 1 if not self.scroll < 1 else 0
				#get input
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
					audio.speak('Speak now')
					query = audio.listen()
					#query = raw_input()
					ch.sendquery(query)
				else:
					pass
			self.terrain()
			self.panel()
			map(self.panelitems,planes,map(planes.index,planes))
			map(self.predictor,planes)
			map(self.plot,lon,lat,alt,name,state,collision)
			pygame.display.flip()
			pygame.display.update()
			t.sleep(0.1)
	
	def new(self,plane):
		if plane.name == 'TOWER':
			plane.getquery()
			return plane.name,plane.state,plane.latitude,plane.longitude,0,plane.altitude,plane.heading,0,plane.query,plane.acknowledge(),0
		else:
			ch = channel()
	    	ack = plane.acknowledge()
	    	if ((plane.state == 'taxi') or (plane.state == 'takeoff')):
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
	        if (not ack):
	            if new:
	                if attr == 'H':
	                    plane.changeheading(new)
	                elif attr == 'A':
	                    plane.changealtitude(new)
	                elif attr == 'S':
	                    plane.changespeed(new)
	                elif attr == 'T':
	                    if plane.speed >= 150 and plane.distance >= 50:
	                        if (not plane.heading == new%1000) and plane.altitude > 200:
	                            plane.changeheading(new%1000)
	                        if not plane.altitude == new/1000:
	                            plane.changealtitude(new/1000) 
	                elif attr == 'G':
	                	audio.speak(plane.getquery())
	            else:
	                ch.clearchannel()
	                plane.getquery()
	        else:
	        	plane.getquery()
	        return plane.name,plane.state,plane.latitude,plane.longitude,dist,plane.altitude,plane.heading,plane.speed,plane.query,ack,checkcollision(plane)
