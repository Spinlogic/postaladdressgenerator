'''
Name generator

Parses the names and surnames files and generates random names from them.
'''

import random

class NameGenerator(object):

    def __init__(self, namesfilename, surnamesfilename):
        self._names = []
        self._surnames = []
        self._parse(namesfilename, self._names)
        self._parse(surnamesfilename, self._surnames)

    def _parse(self, filename, namearray):
        with open(filename, mode="r", encoding='UTF8') as names:
            for name in names:
                namearray.append(name)

    def generateRandomNames(self, count, num_surnames=1):
        names = []
        for i in range(count):
            selected_name = self._names[random.randrange(len(self._names) - 1)]
            for i in range(num_surnames):
                selected_name += " " + self._surnames[random.randrange(len(self._surnames) - 1)]
            names.append(selected_name)
        return names