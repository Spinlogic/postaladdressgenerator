#!/usr/bin/env python

__version__ = '0.1.0'

import argparse
from pathlib import Path
from postaladdress import PostalAddressGenerator
from contacts import ContactGenerator
from geocoder import GeoCoder

CSVHEADER = "firstnames,surnames,country_code, prefix_number, number, email,locations1:line1,locations1:city,locations1:state,locations1:country,locations1:latitude,locations1:longitude"

def main(count, numsurnames, streetsfn, namesfn, surnamesfn, outfn):
    streets = PostalAddressGenerator(streetsfn)
    contacts = ContactGenerator(namesfn, surnamesfn)
    geocoder = GeoCoder()
    random_addresses = streets.generateRandomAddresses(count)
    random_contacts = contacts.generateRandomContacts(count, num_surnames=numsurnames)
    with open(outfn, mode="w", encoding='UTF8') as outputdata:
        # CSV file header
        outputdata.write(CSVHEADER + "\n")
        for i in range(count):
            s = f"{random_contacts[i]},{random_addresses[i]}".strip()
            # outputdata.write(''.join(s.splitlines()) + os.linesep)
            loc = geocoder.resolvePostalAddress(random_addresses[i])
            if loc != None:
                line = f"{s},{loc[0]},{loc[1]}"
            else:
                line = None
                print(f"Geocode Failure for: {random_addresses[i]}")
            # outputdata.write((''.join(s.splitlines())).strip() + '\n')
            if line != None: # only geocoded ones
                outputdata.write(''.join(line.splitlines()) + '\n')
    print(f"{count} records created.\nGeocoding API Failures: {geocoder.getNumFailures()}\nGeocoding API Errors: {geocoder.getNumErrors()}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action="store", type = int, dest="count", default=100,
                        help='Number of addresses to generate, default = 100')
    parser.add_argument('-s', action="store", type = int, dest="numsurnames", default=1,
                        help='Number of surnames for a person, default = 1')
    parser.add_argument('streets_file', type = str, help = 'File with list of streets and municipality')
    parser.add_argument('names_file', type=str, help='File with common names')
    parser.add_argument('surnames_file', type=str, help='File with common surnames')
    parser.add_argument('out_file', type = str, help = 'output file (CSV)')

    args = parser.parse_args()
    assert (Path(args.streets_file).exists())
    assert (Path(args.names_file).exists())
    assert (Path(args.surnames_file).exists())
    print(f"Count: {args.count} , NumSurnames: {args.numsurnames}")
    main(args.count, args.numsurnames, args.streets_file, args.names_file, args.surnames_file, args.out_file)
