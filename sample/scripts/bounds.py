#import os, sys; sys.path.insert(0, os.path.join("..", ".."))
from math import radians, cos, sin, asin, atan2, degrees
from pprint import pprint

def bounds(lat, lon, distance):
	radius = 3963.1
	north = 0
	south = 180
	east = 90
	west = 270
	
	lat_r = radians(lat)
	lon_r = radians(lon)
	
	northmost = degrees( asin( sin(lat_r) * cos( distance / radius ) + cos(lat_r) * sin( distance / radius ) * cos(north) ) )
	southmost = degrees( asin( sin(lat_r) * cos( distance / radius ) + cos(lat_r) * sin( distance / radius ) * cos(south) ) )
	
	eastmost = degrees( lon_r + atan2( sin(east) * sin( distance / radius ) * cos(lat_r), cos( distance / radius ) - sin(lat_r) *sin(lat_r) ) )
	westmost = degrees( lon_r + atan2( sin(west) * sin( distance / radius ) * cos(lat_r), cos( distance / radius ) - sin(lat_r) *sin(lat_r) ) )
	
	if( northmost > southmost):
		lat1 = southmost
		lat2 = northmost
	else:
		lat1 = northmost
		lat2 = southmost
	
	if( eastmost > westmost ):
		lon1 = westmost
		lon2 = eastmost
	else:
		lon1 = eastmost
		lon2 = westmost
		
	return {'nw' : [lat1, lon1], 'se' :[lat2, lon2]}
	
if __name__ == '__main__':
	#print bounds(lat, lon, distance)