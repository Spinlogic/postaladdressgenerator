#!/usr/bin/env python

__version__ = '0.1.0'

import os, argparse
from pathlib import Path
from postaladdress import PostalAddressGenerator
from names import NameGenerator

def main(count, numsurnames, streetsfn, namesfn, surnamesfn, outfn):
    streets = PostalAddressGenerator(streetsfn)
    names = NameGenerator(namesfn, surnamesfn)
    random_addresses = streets.generateRandomAddresses(count)
    random_names = names.generateRandomNames(count, num_surnames=numsurnames)
    with open(outfn, mode="w", encoding='UTF8') as outputdata:
        for i in range(count):
            s = f"{random_names[i]}, {random_addresses[i]}"
            # outputdata.write(''.join(s.splitlines()) + os.linesep)
            outputdata.write(''.join(s.splitlines()) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action="store", dest="count", default=100,
                        help='Number of addresses to generate, default = 100')
    parser.add_argument('-s', action="store", dest="numsurnames", default=1,
                        help='Number of surnames for a person, default = 1')
    parser.add_argument('streets_file', type = str, help = 'File with list of streets and municipality')
    parser.add_argument('names_file', type=str, help='File with common names')
    parser.add_argument('surnames_file', type=str, help='File with common surnames')
    parser.add_argument('out_file', type = str, help = 'output file (CSV)')

    args = parser.parse_args()
    assert (Path(args.streets_file).exists())
    assert (Path(args.names_file).exists())
    assert (Path(args.surnames_file).exists())
    main(args.count, args.numsurnames, args.streets_file, args.names_file, args.surnames_file, args.out_file)
