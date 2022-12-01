'''
Postal address generator

Parses the streets file and generates random addresses from it.
'''

import random
from geocoder import GeoCoder

GEOREPORT_COUNT = 100  # output the count every this number of created contacts

# Acceptable address type with the maximum number that will be used to randomise
STREET_REFS = {
    "avenida": 100,
    "calle": 100,
    "glorieta": 5,
    "pasaje": 10,
    "paseo": 20,
    "plaza": 5,
    "ronda": 50,
    "travesia": 50
}

class PostalAddressGenerator(object):

    def __init__(self, streetsfilename, isgetgeo):
        self._streets = []
        self._parse(streetsfilename)
        if isgetgeo:
            self._geocoder = GeoCoder()
        else:
            self._geocoder = None

    def _parse(self, filename):
        '''
        Parses the input file to extract valid street names.
        Extracted streets are pushed into the class _streets array.
        :param filename: file that contains the list of streets / ways
        :return: void
        '''
        with open(filename, mode="r", encoding='UTF8') as ways:
            valid_ways = list(STREET_REFS.keys())
            for way in ways:
                way_split = way.split("(")  # splits into [way , municipality]
                way_parts = way_split[0].split(" ")
                if way_parts[0].lower() in valid_ways:
                    municipality = way_split[1][:-2] # Remove the last char (")")
                    # Check if municipality is broken in two strings separated by commas
                    municipality_parts = municipality.split(",")
                    if len(municipality_parts) > 1:
                        municipality = f"{municipality_parts[1]} {municipality_parts[0]}"
                    way_type = way_parts[0]
                    way_name = way_split[0][len(way_type) + 1:]
                    way_final = {
                        "type": way_type.strip(),
                        "name": way_name.strip(),
                        "municipality": municipality.strip()
                    }
                    self._streets.append(way_final)
                    # print(f"Tipo: {way_final['type']} , Nombre: {way_final['name']}, Municipio: {way_final['municipality']}")

    def _reportGeoResults(self):
        print(f"\nGeocoding API Failures: {self._geocoder.getNumFailures()}\nGeocoding API Errors: {self._geocoder.getNumErrors()}\n")

    def generateRandomAddresses(self, count):
        '''
        Generates random addresses
        :param count: Number of random addresses to generate
        :return: List of strings
        '''
        addresses = []
        n = 0
        while n < count:
            selected_way = self._streets[random.randrange(len(self._streets) - 1)]
            selected_way_number = random.randrange(STREET_REFS[selected_way["type"].lower()])
            address = f"{selected_way['type']} {selected_way['name']} {selected_way_number},{selected_way['municipality']},Madrid,ES"
            if self._geocoder is not None:
                loc = self._geocoder.resolvePostalAddress(address)
                if loc is not None:
                    address += f",{loc[0]},{loc[1]}"
                    addresses.append(address)
                    if n % GEOREPORT_COUNT == 0:
                        print(f"Current count: {n} of {count}")
                    n += 1
            else:
                n += 1
                addresses.append(address)
        if self._geocoder is not None:
            self._reportGeoResults()
        return addresses