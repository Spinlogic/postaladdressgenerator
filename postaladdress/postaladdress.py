'''
Postal address generator

Parses the streets file and generates random addresses from it.
'''

import random

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

    def __init__(self, streetsfilename):
        self._streets = []
        self._parse(streetsfilename)

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
                        "type": way_type,
                        "name": way_name,
                        "municipality": municipality
                    }
                    self._streets.append(way_final)
                    # print(f"Tipo: {way_final['type']} , Nombre: {way_final['name']}, Municipio: {way_final['municipality']}")

    def generateRandomAddresses(self, count):
        '''
        Generates random addresses
        :param num_addresses: Number of random addresses to generate
        :return: List of strings
        '''
        addresses = []
        for i in range(count):
            selected_way = self._streets[random.randrange(len(self._streets) - 1)]
            selected_way_number = random.randrange(STREET_REFS[selected_way["type"].lower()])
            addresses.append(f"{selected_way['type']} {selected_way['name']} {selected_way_number}, {selected_way['municipality']}, Madrid")
        return addresses