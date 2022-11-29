#!/usr/bin/env python

__version__ = '0.1.0'

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('streets_file', type = str, help = 'File with list of streets and municipality')
    parser.add_argument('names_file', type=str, help='File with common names')
    parser.add_argument('surnames_file', type=str, help='File with common surnames')
    parser.add_argument('out_file', type = str, help = 'output file (CSV)')
    args = parser.parse_args()
    main(args.streets_file, args.out_file)