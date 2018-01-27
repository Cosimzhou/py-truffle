#coding: utf-8

import math
earth_radius=6371004
cons = math.pi/180

def arc_points(p1,p2):
    x1, y1, x2, y2 = p1 + p2
    rlon1, rlat1, rlon2, rlat2 = float(x1) * cons, float(y1) * cons, float(x2) * cons, float(y2) *cons
    vcos = math.cos(rlat1) * math.cos(rlat2) * math.cos(rlon1 - rlon2) + math.sin(rlat1) * math.sin(rlat2)
    vcos = 1.0 if vcos > 1.0 else (vcos if vcos > -1.0 else -1.0)
    return math.acos(vcos) 
    
def ll2xyz(p):
    x, y = p[0]*cons, p[1]*cons
    return (math.sin(x)*math.cos(y)*earth_radius, math.cos(x)*math.cos(y)*earth_radius, math.sin(y)*earth_radius)

def xyz2ll(p):
    x, y, z = p[0]/earth_radius, p[1]/earth_radius, p[2]/earth_radius
    lat = math.asin(z)
    lng = math.asin(x/math.cos(lat))
    
    return (lng/cons, lat/cons)