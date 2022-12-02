#!/usr/bin/env python

__version__ = '0.1.0'

import argparse
from pathlib import Path
from postaladdress import PostalAddressGenerator
from contacts import ContactGenerator

CSVHEADER = "firstnames,surnames,country_code,prefix_number,number,email,locations1:line1,locations1:city,locations1:state,locations1:country,locations1:latitude,locations1:longitude"
STEP = 10   # number of contacts written in each iteration

def main(count, numsurnames, isgetgeo, streetsfn, namesfn, surnamesfn, outfn):
    streets = PostalAddressGenerator(streetsfn, isgetgeo, count)
    contacts = ContactGenerator(namesfn, surnamesfn)
    with open(outfn, mode="w", encoding='UTF8') as outputdata:
        # CSV file header
        outputdata.write(CSVHEADER + "\n")
        n = 0
        while n < count:
            iter_count = STEP
            if n + iter_count > count:
                iter_count = count - n
            random_addresses = streets.generateRandomAddresses(iter_count)
            random_contacts = contacts.generateRandomContacts(iter_count, num_surnames=numsurnames)
            for i in range(iter_count):
                line = f"{random_contacts[i]},{random_addresses[i]}".strip()
                outputdata.write(''.join(line.splitlines()) + '\n')
            n += STEP
    streets.reportGeoResults()
    print(f"{count} records created.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="ContactsGenerator",
        description="Generates random contact data for import tools"
    )
    parser.add_argument('-g', '--geocode', action="store_true", help='Retrieve geocoordinates for all postal addresses')
    parser.add_argument('-c', action="store", type = int, dest="count", default=100,
                        help='Number of addresses to generate, default = 100')
    parser.add_argument('-s', action="store", choices=['1', '2'], dest="numsurnames", default=1,
                        help='Number of surnames for a person, default = 1')
    parser.add_argument('streets_file', type = str, help = 'File with list of streets and municipality')
    parser.add_argument('names_file', type=str, help='File with common names')
    parser.add_argument('surnames_file', type=str, help='File with common surnames')
    parser.add_argument('out_file', type = str, help = 'output file (CSV)')

    args = parser.parse_args()
    assert (Path(args.streets_file).exists())
    assert (Path(args.names_file).exists())
    assert (Path(args.surnames_file).exists())
    print(f"Count: {args.count} , NumSurnames: {args.numsurnames}, Get Geocoordinates: {args.geocode}")
    main(args.count, int(args.numsurnames), args.geocode, args.streets_file, args.names_file, args.surnames_file, args.out_file)
