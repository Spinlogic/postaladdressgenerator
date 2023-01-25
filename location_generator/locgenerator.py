'''
Location coordinates generator

Genarates random locations within the given square.
'''

import random

GEOREPORT_COUNT = 100  # output the count every this number of created contacts

class LocationGenerator(object):
    def __init__(self, tleft, bright, distrib=0):
        '''
        Constructor
        :param tleft: vector with coordinates [lon, lat] of the top left corner
        :param bright: vector with coordinates [lon, lat] of the button right corner
        :param distrib: 0 -> Uniform, 1 -> Gaussian centered in the center of the square
        '''
        print(f"DEBUG - top left: {tleft} , bottom right: {bright}")
        self._topleft = [float(tleft[0]), float(tleft[1])]
        self._bottomright = [float(bright[0]), float(bright[1])]
        if( distrib > 1 or distrib < 0):
            raise ValueError('Unsuported distribution.')
        # if( len(tleft) < 2 or
        #     len(bright) < 2 or
        #     type(tleft[0]) is not float or
        #     tleft[0] < 0.0 or
        #     tleft[0] > 360.0 or
        #     type(tleft[1]) is not float or
        #     tleft[1] < 0.0 or
        #     tleft[1] > 360.0 or
        #     type(bright[0]) is not float or
        #     bright[0] < 0.0 or
        #     bright[0] > 360.0 or
        #     type(bright[0]) is not float or
        #     bright[1] < 0.0 or
        #     bright[1] > 360.0 ):
        #     raise ValueError('Invalid coordinates.')
        if len(tleft) < 2:
            raise ValueError('Invalid coordinates 1.')
        if len(bright) < 2:
            raise ValueError('Invalid coordinates 2.')
        if tleft[0] < 0.0:
            raise ValueError('Invalid coordinates 3.')
        if tleft[0] > 360.0:
            raise ValueError('Invalid coordinates 4.')
        if bright[1] < 0.0:
            raise ValueError('Invalid coordinates 5.')
        if bright[1] > 360.0:
            raise ValueError('Invalid coordinates 6.')
        self._topleft = tleft
        self._bottomright = bright
        self._distribution = distrib

    def __generateUniformRandomLocs(self, count):
        '''
        Returns a "count" number of random locations distributed uniformly accross
        the square
        :param count: number of locations to generate
        :return: list of uniformly distributed locations
        '''
        locslist = []
        for i in range(count):
            lon = random.uniform(self._bottomright[0], self._topleft[0])
            lat = random.uniform(self._topleft[1], self._bottomright[1])
            # print(f"DEBUG - i: {i} - lon: {lon} , lat: {lat}")
            locslist.append([lon, lat])
        return locslist

    def __generateGaussianRandomLocs(self, count):
        '''
        Returns a "count" number of random locations distributed using a Normally
        inside the square. mu = center of the square and sigma = 1 / 4 of the
        side of the square.
        :param count: number of locations to generate
        :return: list of uniformly distributed locations
        '''
        locslist = []
        lon_mu = self._topleft[0] + ((self._bottomright[0] - self._topleft[0]) / 2)
        lat_mu = self._bottomright[1] + ((self._topleft[1] - self._bottomright[1]) / 2)
        lon_sigma = (self._bottomright[0] - self._topleft[0]) / 4
        lat_sigma = (self._topleft[1] - self._bottomright[1]) / 4
        print(f"DEBUG - lon_mu: {lon_mu} \tlon_sigma: {lon_sigma}")
        print(f"DEBUG - lat_mu: {lat_mu} \tlat_sigma: {lat_sigma}")
        i = 0
        while i < count:
            lon = random.gauss(lon_mu, lon_sigma)
            lat = random.gauss(lat_mu, lat_sigma)
            # print(f"DEBUG - i: {i} - lon: {lon} , lat: {lat}")
            if lon > self._bottomright[0] or lat > self._topleft[1]:
                continue
            locslist.append([lon, lat])
            i = i + 1
        return locslist

    def generateRandomLocations(self, count):
        '''
        Generates a "count" number of random locations distributed according to
        the configured probability distribution
        :param count: number of locations to generate
        :return: list of locations
        '''
        if( self._distribution == 0):
            return self.__generateUniformRandomLocs(count)
        else:
            return self.__generateGaussianRandomLocs(count)