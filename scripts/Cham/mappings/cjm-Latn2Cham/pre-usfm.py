#!/usr/bin/python

# pre-usfm.py
# Part of the Latin to Cham script conversion for the Eastern Cham language.
# To be used with cjm-Latn2Cham.py and usfmtec.
# Run this script before usfmtec to clean up the data markup so it is
# acceptable to usfmtec.

import codecs, os, re, string, sys, unicodedata, argparse

def paragraphCheck(line, inPar):
    # The following usfm tags identify the start of some kind of paragraph structure,
    # within which a \v marker must reside:
    # \d, \li, \li1, \li2, \li3, \li4, \m, \mi, \nb, \p, \pc, \ph, \phi, \pi, \pi1, \pi2, \pi3,
    # \pm, \pmc, \pmo, \pmr, \pr, \q, \q1, \q2, \q3, \q4, \qc, \qm, \qm1, \qm2, \qm3, \qm4, \qr,
    # \sp, \tc1, \tc2, \tc3, \tc4, \tcr1, \tcr2, \tcr3, \tcr4
    startParagraphMarker = re.compile(ur'\\(d|li[1234]?|m|mi|nb|p|pc|ph|phi|pi[123]?|pm[cor]?|pr|q[1234]?|qc|qm[1234]?|qr|sp|tc[1234]|tcr[1234])')
    if startParagraphMarker.match(line):
        return True
    # The following usfm tags will end a paragraph
    # \c, \s
    endParagraphMarker = re.compile(ur'\\[cs] ')
    if endParagraphMarker.match(line):
        return False
    return inPar
    
def vNumberListCheck(line):
    # If \v has subverses or commas, insert ' z' before the first occurance.
    # 'z' is used as a flag here because it does not occur in the Cham Latin orthography.
    # Remove these tweaks in post-usfm by searching for and removing ' z'.
    vnPattern1 = re.compile(ur'(?P<vNum>\\v +\d+)(?P<subv>[abcdef])(?P<tail>.*)', re.DOTALL)
    m = vnPattern1.match(line)
    if m:
        line = m.group('vNum') + u' z' + m.group('subv') + m.group('tail')
    else:
        vnPattern2 = re.compile(ur'(?P<vNum>\\v +\d+),(?P<tail>.*)', re.DOTALL)
        m = vnPattern2.match(line)
        if m:
            line = m.group('vNum') + u' z,' + m.group('tail')
        else:
            vnPattern3 = re.compile(ur'(?P<vNum>\\v +\d+-\d+)(?P<subv>[abcdef])(?P<tail>.*)', re.DOTALL)
            m = vnPattern3.match(line)
            if m:
                line = m.group('vNum') + u' z' + m.group('subv') + m.group('tail')
##    # If a verse list has commas in it, insert ' z' before the first comma
##    vListPattern = re.compile(ur'\A\\v[ ]+(?P<vNum>\d*),(?P<tail>.*)')
##    line = vListPattern.sub(ur'\\v \g<vNum> z,\g<tail>', line)
    return line

def emptyVerseCheck(line):
    # If a verse has no text, insert a string of 3 Cham Spirals
    # (This is because usfmtec doesn't handle empty verses well.)
    # Remove this tweak in post-usfm by searching for the string of Cham Spirals.
    emptyVerse = re.compile(ur'\A\\v\s*(?P<vNum>[0-9,\- ]*)(?P<tail>\r\n)')
    return emptyVerse.sub(ur'\\v \g<vNum> \uAA5C\uAA5C\uAA5C\g<tail>', line)
    
def orphanedVerseCheck(line, inPar):
    if line.startswith(u'\\v ') and not inPar:
        return True
    else:
        return False

# ##############
# M A I N
# ##############

parser = argparse.ArgumentParser(description='Run before usfmtec to clean up the data markup.')
parser.add_argument('--noorphan', dest='orphanedVerseFlag', action='store_false', help='Don\'t run the orphaned \\v check.')
parser.add_argument('--novnum', dest='verseNumberFlag', action='store_false', help='Don\'t run the verse number check.')
parser.add_argument('--noempty', dest='emptyVerseFlag', action='store_false', help='Don\'t run the empty verse check.')
parser.add_argument('inFile')
parser.add_argument('outFile')
args = parser.parse_args()

if os.path.exists(args.inFile) :
    inf = codecs.open(args.inFile, encoding="utf-8")
    outf = codecs.open(args.outFile, "w", encoding="utf-8")
    inPar = False
    for l in inf.readlines() :
        inPar = paragraphCheck(l, inPar)
        if l.startswith(u'\\v'):
            if args.verseNumberFlag:
                l = vNumberListCheck(l)
            if args.emptyVerseFlag:
                l = emptyVerseCheck(l)
            if args.orphanedVerseFlag:
                if orphanedVerseCheck(l, inPar):
                    outf.write(u'\\m\r\n')
                    inPar = True
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
