# The conversion from WGS-84 to Cartesian has an analytical solution
import numpy as np
from math import atan2, radians, cos, sin, asin, sqrt , degrees, acos, pi

import math

class Convert:
    def __init__(self):
        pass 
    def lla2ecef(self,lat, lon, alt):
	    a = 6378137
	    a_sq = a**2
	    e = 8.181919084261345e-2
	    e_sq = e**2
	    b_sq = a_sq*(1 - e_sq)

	    lat = lat*np.pi/180
	    lon = lon*np.pi/180

	    N = a/np.sqrt(1 - e_sq*np.sin(lat)**2)
	    x = (N+alt)*np.cos(lat)*np.cos(lon)
	    y = (N+alt)*np.cos(lat)*np.sin(lon)
	    z = ((b_sq/a_sq)*N+alt)*np.sin(lat)

	    return float(x), float(y),float(z)


    def ecef2lla_hugues(self,x, y, z):
	    # x, y and z are scalars in meters (CANNOT use vectors for this method)
	    # Following "An analytical method to transform geocentric into geodetic coordinates"
	    # By Hugues Vermeille (2011)

	    a=6378137
	    a_sq=a**2
	    e = 8.181919084261345e-2
	    e_sq = 6.69437999014e-3

	    p = (x**2 + y**2)/a_sq
	    q = ((1 - e_sq)*(z**2))/a_sq
	    r = (p + q - e_sq**2)/6.

	    evolute = 8*r**3 + p*q*(e_sq**2)

	    if(evolute > 0):
		    u = r + 0.5*(np.sqrt(8*r**3 + p*q*e_sq**2) + np.sqrt(p*q*e_sq**2))**(2/3.) + \
				    0.5*(np.sqrt(8*r**3 + p*q*e_sq**2) - np.sqrt(p*q*e_sq**2))**(2/3.)
	    else:
		    u_term1 = np.sqrt(p*q*e_sq**2)/(np.sqrt(-8*r**3 - p*q*e_sq**2) + np.sqrt(-8*r**3))
		    u_term2 = (-4.*r)*np.sin((2./3.)*np.arctan(u_term1))
		    u_term3 = np.cos(np.pi/6. + (2./3.)*np.arctan(u_term1))
		    u       = u_term2*u_term3

	    v = np.sqrt(u**2 + q*e_sq**2)
	    w = e_sq*(u + v - q)/(2.*v)
	    k = (u + v)/(np.sqrt(w**2 + u + v) + w)
	    d = k*np.sqrt(x**2 + y**2)/(k + e_sq)
	    h = np.sqrt(d**2 + z**2)*(k + e_sq - 1)/k
	    phi = 2.*np.arctan(z/((np.sqrt(d**2 + z**2) + d)))

	    if((q == 0) and (p <= e_sq**2)):
		    h = -(a*np.sqrt(1 - e_sq)*np.sqrt(e_sq - p))/(e)
		    phi1 = 2*np.arctan(np.sqrt(e_sq**2 - p)/(e*(np.sqrt(e_sq - p)) + np.sqrt(1 - e_sq)*np.sqrt(p)))
		    phi2 = -phi1
		    phi = (phi1, phi2)


	    case1 = (np.sqrt(2) - 1)*np.sqrt(y**2) < np.sqrt(x**2 + y**2) + x
	    case2 = np.sqrt(x**2 + y**2) + y < (np.sqrt(2) + 1)*np.sqrt(x**2)
	    case3 = np.sqrt(x**2 + y**2) - y < (np.sqrt(2) + 1)*np.sqrt(x**2)

	    if(case1):
		    lambd = 2.*np.arctan(y/(np.sqrt(x**2 + y**2) + x))
		    return phi*180/np.pi, lambd*180/np.pi, h
	    if(case2):
		    lambd = (-np.pi/2) - 2.*np.arctan(x/(np.sqrt(x**2 + y**2) - y))
		    return phi*180/np.pi, lambd*180/np.pi, h
	    if(case3):
		    lambd = (np.pi/2) - 2.*np.arctan(x/(np.sqrt(x**2 + y**2) + y))
		    return phi*180/np.pi, lambd*180/np.pi, h

	    return phi*180/np.pi, lambd*180/np.pi, h

'''lat=27.00523412
lon=77.2345112
alt=12
print(lat,lon,alt)
x,y,z=lla2ecef(lat,lon,alt)

print(x,y,z)

redo= ecef2lla_hugues(x, y, z)
print(redo)'''


