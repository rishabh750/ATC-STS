#System packages
import json
import operator

#User Defined Packages
import channel as ch
import audio

#Global definitions

#Classes
class analysquery:
	cognates = dict()
	def __init__(self):
		with open('cognates.json','r') as j:
			try:
				self.cognates = json.load(j)
			except:
				pass
	def analysquery(self,plane):
	    	if not plane.query == 'NULL':
	    		query = plane.query.split()
	    	new = 0
	    	attr = 'NULL'
	    	try:
	    		if not set(self.cognates['change']).isdisjoint(set(query)):
	    			while 1:
	    				try:
	    					h = set(self.cognates['H']).isdisjoint(set(query))
			    			a = set(self.cognates['A']).isdisjoint(set(query))
			    			s = set(self.cognates['S']).isdisjoint(set(query))
			    			if not h:
			    				new = int(query[query.index(set(self.cognates['H']).intersection(set(query)).pop())+1])
			    				plane.newhead = new
			    				attr = 'H'
			    			elif not a:
			    				new = int(query[query.index(set(self.cognates['A']).intersection(set(query)).pop())+1])
			    				attr = 'A'
			    			elif not s:
			    				new = int(query[query.index(set(self.cognates['S']).intersection(set(query)).pop())+1])
			    				attr = 'S'
			    			else:
			    				pass
			    			break
			    		except:
			    			audio.speak('Did not understand, Tower please repeat')
			    			continue
	    		elif not set(self.cognates['T']).isdisjoint(set(query)):
	    			attr = 'T'
	    			new = 3000120
	    		elif not set(self.cognates['L']).isdisjoint(set(query)):
	    			attr = 'L'
	    			new = 0
	    		elif not set(self.cognates['G']).isdisjoint(set(query)):
	    			attr = 'G'
	    		else:
	    			pass
	    	except:
	    		if not plane.query == 'NULL':
	    			audio.speak('Sorry Tower, did not get that!')
	    		pass
	    	#except Exception as e:
	    	#	print 'error',e
	    	if attr == 'H':
	    		return (new,attr) if not (plane.heading == new) else (0,'NULL')
	    	elif attr == 'A':
	    		return (new,attr) if not (plane.altitude == new) else (0,'NULL')
	    	elif attr == 'S':
	    		return (new,attr) if not (plane.speed == new) else (0,'NULL')
	    	elif attr == 'T':
	    		plane.state = 'takeoff'
	    		if plane.speed < 150:
	    			plane.changespeed(150)
	    		elif plane.speed < 250:
	    			plane.changespeed(plane.speed+1)
	    		return (new,attr) if not ((plane.altitude == new/1000) and (plane.heading == new%1000)) else (0,'NULL')
	    	else:
	    		return (0,'NULL')