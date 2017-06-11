#System packages

#User Defined Packages
import channel

#Global definitions
planes = list()
lats = list()
lons = list()
alts = list()
def updatecluster(plane):
	if plane.name in planes:
		pos = planes.index(plane.name)
		lats[pos] = plane.latitude
		lons[pos] = plane.longitude
		alts[pos] = plane.altitude
	else:
		planes.append(plane.name)
		lats.append(plane.latitude)
		lons.append(plane.longitude)
		alts.append(plane.altitude)
def checkcollision(plane):
	plane.collision = 0
	for i in planes:
		if i == plane.name:
			pass
		else:
			pos = planes.index(i)
			lat = lats[pos]
			lon = lons[pos]
			alt = alts[pos]
			gap = (((plane.latitude-lat)*69*5280)**2 + ((plane.longitude-lon)*69*5280)**2 + ((plane.altitude-alt))**2)**0.5
			if gap <1700 and gap > 1200:
				plane.collision = 1
				channel.alert = '%s and %s colliding'%(plane.name,i)
				break
			elif gap < 1200:
				plane.collision = 2
				channel.alert = '%s and %s colliding'%(plane.name,i)
				break
			else:
				channel.alert = None
				pass
	return plane.collision

#Classes