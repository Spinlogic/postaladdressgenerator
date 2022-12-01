#!/usr/bin/env python

__version__ = '0.1.0'

import argparse
from pathlib import Path
from postaladdress import PostalAddressGenerator
from contacts import ContactGenerator
from geocoder import GeoCoder

CSVHEADER = "firstnames,surnames,country_code, prefix_number, number, email,locations1:line1,locations1:city,locations1:state,locations1:country,locations1:latitude,locations1:longitude"

def main(count, numsurnames, isgetgeo, streetsfn, namesfn, surnamesfn, outfn):
    streets = PostalAddressGenerator(streetsfn, isgetgeo)
    contacts = ContactGenerator(namesfn, surnamesfn)
    random_addresses = streets.generateRandomAddresses(count)
    random_contacts = contacts.generateRandomContacts(count, num_surnames=numsurnames)
    with open(outfn, mode="w", encoding='UTF8') as outputdata:
        # CSV file header
        outputdata.write(CSVHEADER + "\n")
        for i in range(count):
            line = f"{random_contacts[i]},{random_addresses[i]}".strip()
            outputdata.write(''.join(line.splitlines()) + '\n')
    print(f"{count} records created.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="ContactsGenerator",
        description="Generates random contact data for import tools"
    )
    parser.add_argument('-g', '--geocode', action="store_true", help='Retrieve geocoordinates for all postal addresses')
    parser.add_argument('-c', action="store", type = int, dest="count", default=100,
                        help='Number of addresses to generate, default = 100')
    parser.add_argument('-s', action="store", choices=[1, 2], dest="numsurnames", default=1,
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
    main(args.count, args.numsurnames, args.geocode, args.streets_file, args.names_file, args.surnames_file, args.out_file)
