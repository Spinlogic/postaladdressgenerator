#!/usr/bin/env python
'''
This is a version of "main" that creates contact with a random geo-location instead of and address.
In this case, contacts have coordinates but do not have an address.

You need to provide the coordinates of the top left corner and button right corner of the square inside which the
contacts will be located.

The distribution of contacts is uniform accross the square area.

Command line example:

python .\geoloc.py -t 51.3819493 25.3259598 -b 51.5445458 25.2087047 -ct es -c 5 -d 1 .\data\ArabicNames.txt .\data\ArabicFamilyNames.txt test_out.csv

For the -t you must input longitude and latitude, in that order, of the top left corner.
For the -b you must input longitude and latitude, in that order, of the bottom right corner.
'''

__version__ = '0.1.0'

import argparse
from pathlib import Path
from contacts import ContactGenerator
from location_generator import LocationGenerator

CSVHEADER = "firstnames,surnames,country_code, prefix_number, number, email,locations1:line1,locations1:city,locations1:state,locations1:country,locations1:latitude,locations1:longitude"

def createContacts(count, distrib, tleft, bright, numsurnames, namesfn, surnamesfn, outfn, groups, countries):
    contacts = ContactGenerator(namesfn, surnamesfn, countries)
    locgen = LocationGenerator(tleft, bright, distrib)
    random_locs = locgen.generateRandomLocations(count)
    random_contacts = contacts.generateRandomContacts(count, num_surnames=numsurnames)
    with open(outfn, mode="w", encoding='UTF8') as outputdata:
        # CSV file header
        outputdata.write(CSVHEADER + "\n")
        for i in range(count):
            line = f"{random_contacts[i]},,,,,{random_locs[i][1]},{random_locs[i][0]}".strip()
            outputdata.write(''.join(line.splitlines()) + '\n')
    print(f"{count} locations created.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="ContactsGenerator",
        description="Generates random contact data for import tools"
    )
    parser.add_argument('-c', action="store", type=int, dest="count", default=100,
                        help='Number of contacts to generate, default = 100')
    parser.add_argument('-t', action="store", nargs='+', type=float, dest="tleft",
                        help='Top left coordinate')
    parser.add_argument('-b', action="store", nargs='+', type=float, dest="bright",
                        help='Button right coordinate')
    parser.add_argument('-d', action="store", type=int, choices=[0, 1], dest="dist",
                        help='0: Uniform distribution, 1: Gaussian with peak in centre of the square', default=0)
    parser.add_argument('-s', action="store", choices=[1, 2], dest="numsurnames", default=1,
                        help='Number of surnames for a person, default = 1')
    parser.add_argument('-g', action="store", nargs='*', type=str, dest="groups",
                        help='List of groups for the generated contacts')
    parser.add_argument('--ct', action="store", nargs='*', type=str, dest="countries",
                        help='List of countries for the')
    parser.add_argument('names_file', type=str, help='File with common names')
    parser.add_argument('surnames_file', type=str, help='File with common surnames')
    parser.add_argument('out_file', type = str, help = 'output file (CSV)')

    args = parser.parse_args()
    assert (Path(args.names_file).exists())
    assert (Path(args.surnames_file).exists())
    distribution = "Uniform" if (args.dist == 0) else "Gaussian"
    print(f"Count: {args.count}\nNumSurnames: {args.numsurnames}\nGroups: {args.groups}\nGeocoordinates: [{args.tleft} , {args.bright}]\nDistribution: {distribution}")
    createContacts(args.count, args.dist, args.tleft, args.bright, args.numsurnames, args.names_file, args.surnames_file, args.out_file, args.groups, args.countries)
