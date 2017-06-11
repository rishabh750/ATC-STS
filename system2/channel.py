#System packages
import re

#User Defined Packages
import audio

#Global definitions
reciever = None
transmitter = None
query = None
alert = None
runway = False

#Classes
class channel:
    reciever = None
    transmitter = None
    query = None
    def sendquery(self,query):
        if query == '' or query == None:
            return
        query = query.upper()
        print query
        querys = query.split()
        try:
            self.reciever = 'AI-'+str(int(querys[0]))
            self.query = query[query.index(querys[0])+4:]
            self.transmitter = 'TOWER'
            audio.speak(self.transmitter)
            audio.speak(self.reciever)
            audio.speak(self.query)
            self.globalsave()
        except:
            pass
    def globalsave(self):
        global reciever
        reciever = self.reciever
        global transmitter
        transmitter = self.transmitter
        global query
        query = self.query
        #print query 
    def clearchannel(self):
        global reciever
        reciever = None
        global transmitter
        transmitter = None
        global query
        query = None
    def printlast(self):
        global transmitter
        global reciever
        global query
        print '\nLatest transmission on the channel\nTo:\t%s\nFrom:\t%s\nQuery:\t%s'%(reciever,transmitter,query)
        print '\nAlert:',alert
    def getquery(self,requester):
        global reciever
        return query if (reciever == requester) else 'NULL'
    def lockrunway(self):
        global runway
        runway = True
    def releaserunway(self):
        global runway
        runway = False
    def getrunway(self):
        global runway
        return runway