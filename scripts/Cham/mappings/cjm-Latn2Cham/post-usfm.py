#!/usr/bin/python

# post-usfm.py
# Part of the Latin to Cham script conversion for the Eastern Cham language.
# Run after usfmtec to remove the tweaks created by pre-usfm.py.

import codecs, os, re, string, sys, unicodedata, argparse

# ##############
# M A I N
# ##############

parser = argparse.ArgumentParser(description='Post-USFM filter: Run after usfmtec to remove the tweaks created by pre-usfm.py')
parser.add_argument('inFile')
parser.add_argument('outFile')
args = parser.parse_args()

if os.path.exists(args.inFile) :
    inf = codecs.open(args.inFile, encoding="utf-8")
    outf = codecs.open(args.outFile, "w", encoding="utf-8")
    for l in inf.readlines() :
        # Remove " z" flags from \v lines.
        # Note: usfmtec may capitalize the 'z'.
        zPattern = re.compile(ur'\A(?P<marker>\\v[ 0-9\-]+) [zZ](?P<tail>[,abcdef].*)')
        l = zPattern.sub(ur'\g<marker>\g<tail>', l)
        # Remove triple Cham Spiral from \v lines that are meant to be empty.
        spiralPattern = re.compile(ur'\A(?P<marker>\\v[ 0-9]+)(?P<spiral>\uAA5C\uAA5C\uAA5C)(?P<tail>.*)')
        l = spiralPattern.sub(ur'\g<marker>\g<tail>', l)
        outf.write(l)
    inf.close()
    outf.close()
else:
    print
    print "ERROR!"
    print "Cannot open input file: " + args.inFile
    print
    parser.print_help()
    print
    exit()
