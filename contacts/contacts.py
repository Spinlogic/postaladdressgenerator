'''
Name generator

Parses the names and surnames files and generates random names from them.
'''

import random
import json
from pathlib import Path

PREFIXES_FILE = "data/mobileprefixes.json"
DOMAINS = ["gmail.com", "outlook.com", "protonmail.com", "icloud.com", "gmx.com", "yahoo.com", "aol.com", "tutanota.com"]

class ContactGenerator(object):

    def __init__(self, namesfilename, surnamesfilename, countries=["es"]):
        '''
        Contructor
        :param namesfilename:
        :param surnamesfilename:
        :param countries: ISO two letter country codes to use for the mobile phone prefixes
        '''
        self._names = []
        self._surnames = []
        self._mobilePrefixes = []
        self._parse(namesfilename, self._names)
        self._parse(surnamesfilename, self._surnames)
        self._getPhonePrefixes(countries)

    def _parse(self, filename, namearray):
        '''
        Extracts data from filename into namearray.
        :param filename: points to a file that contains one entry (name or surname) per line
        :param namearray: list in which to push the extracted data
        :return:
        '''
        with open(filename, mode="r", encoding='UTF8') as names:
            for name in names:
                namearray.append(name)

    def _getPhonePrefixes(self, countries):
        '''
        Populates class list _mobilePrefixes with the mobile prefixes extracted from JSON PREFIXES_FILE
        :param countries: list of ISO country codes to consider
        :return: list of prefixes in form "+cc" + mobile_prefix
        '''
        prefixesPath = Path.cwd() / PREFIXES_FILE
        with open(prefixesPath) as prefixesFile:
            prefixes_data = json.load(prefixesFile)
            # Normalise all the ISO codes to lowercase
            present_countries = [key.lower() for key in list(prefixes_data.keys())]
            paises = [country.lower() for country in countries]
            for country in paises:
                if country in present_countries:
                    mnos = prefixes_data[country]["mnos"]
                    for mno in mnos:
                        mno_data = prefixes_data[country]["mnos"][mno]
                        for prefix in mno_data["prefixes"]:
                            self._mobilePrefixes.append({
                                "country": country,
                                "code": prefixes_data[country]['cc'],
                                "prefix": prefix
                            })

    def generateRandomContacts(self,
                               count,
                               num_surnames=1,
                               domains=DOMAINS,
                               msisdn_ext_len=6):
        '''
        Generates a list of contacts with random names, surnames, email and phone numbers
        :param count: number of contacts to generate
        :param num_surnames: number of surnames (e.g. 2 in Spain or Mexico, 1 in most other countries)
        :param domains: list of domain names used for email address generation
        :param msisdn_ext_len: length of the phone number excluding the prefix
        :return: list of contacts with the csv format valid for the header in "main.py"
        '''
        contacts = []
        for i in range(count):
            surnames = ""
            name = ""
            for j in range(num_surnames):
                surnames += " " + self._surnames[random.randrange(len(self._surnames) - 1)]
            name = self._names[random.randrange(len(self._names) - 1)]
            selected_contact = name + "," + surnames
            # Generate random phone number
            msisdn = {}
            if len(self._mobilePrefixes) > 0:
                selected_prefix = random.randrange(len(self._mobilePrefixes) - 1)
                selected_contact += "," + self._mobilePrefixes[selected_prefix]["country"].upper()
                selected_contact += "," + self._mobilePrefixes[selected_prefix]["code"]
                # Add prefix + 6 digits extension
                selected_contact += "," + self._mobilePrefixes[selected_prefix]["prefix"] + str(random.randrange((10**msisdn_ext_len) - 1)).zfill(6)
            else:
                selected_contact += ",,,"   # Empty phone info
            # Generate random email
            email = name + ".".join(surnames.split(" ")) + "@" + domains[random.randrange(len(domains) - 1)]
            selected_contact += "," + email
            contacts.append(selected_contact)
        return contacts