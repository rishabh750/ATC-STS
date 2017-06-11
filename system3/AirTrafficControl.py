#System packages
import os
import pygame
import platform

#User Defined Packages
from ATC import ATC
from Plane import Plane
import datagen
import GUI
import console

#Global definitions

#Classes
class AirTrafficControl:
    def __init__(self):
        self.simulate()
    def simulate(self):
        cl = 'cls' if (platform.system() == 'Windows') else 'clear'
        clear = lambda: os.system(cl)
        while 1:
            clear()
            view = input('\nChoose view\n1. GUI\n2. Console\n\nView: ')
            if view == 1 or view == 2:
                break
        traffic = input('Enter the traffic density (Number of planes): ')
        initset = datagen.generateset(traffic)
        planes = list()
        #c = collision(traffic)
        for i in xrange(traffic):
            temp = Plane(initset.pid[i],i)
            planes.append(temp)
        planes.append(ATC())
        if view == 1:
        	gui = GUI.gui()
        	gui.gui(planes)
        else:
        	con = console.console(planes)
        
if __name__ == "__main__":
    AirTrafficControl()
