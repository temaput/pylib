#!/bin/env python3

"""
recode.py inputfile [outputfile] --source=utf-8 --destination=utf-16le
"""

import argparse
import sys, os

def recode(args):
    if args.line_separator == 'windows':
        linesep = '\r\n'
    elif args.line_separator == 'unix':
        linesep = '\n'

    try:
        with open(args.infile.fileno(), args.infile.mode,
                encoding=args.source_encoding, errors='replace') as infile, \
            open(args.outfile.fileno(), args.outfile.mode, newline=linesep,
                    encoding=args.destination_encoding) as outfile:
                for line in infile:
                    outfile.write(line)
    except LookupError:
        print("Unknown encoding")
        sys.exit(1)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout)
    parser.add_argument('-s', '--source_encoding', default="utf-8", help="Кодировка источника")
    parser.add_argument('-d', '--destination_encoding', default="utf-8", 
            help="Целевая кодировка")
    parser.add_argument('-r', '--line_separator', default=os.linesep, 
            help="Разделитель строк")
    args = parser.parse_args()
    recode(args)


