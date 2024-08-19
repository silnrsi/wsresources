#!/usr/bin/python

# cjm-Latn2Cham.py
# Latin to Cham script conversion for the Eastern Cham language.
#   This script is designed to after a dictionary lookup is performed
#   to convert words that do not conform to the usual spelling rules.
#   The dictionary lookup may be done using usfmtec. 
# Written by Jim Brase, SIL International, 2014
#            jim_brase@sil.org
# Copyright SIL International 2014
# #######################################################################################
#
# KNOWN BUGS:
#
# ***************************************************************************************
# History:
# ***************************************************************************************
# Future
#   xxx     Add dictionary lookup
# Version 1.0.0 reversioned from Version 0.2.0:
#   Revised command line parsing
#   Added config file
# Version 0.1.10:
#   Modify segment() to fix degenerate syllables.
# Version 0.1.9:
#   Revised getword() so that hyphen is treated as alphabetic only between letters.
# Version 0.1.8:
#   Improved ErrorFlag suffixes to clarify source of parsing errors.
#   Corrected handling of verse number bridges.
#   Enabled specification of ignored fields (currently hard coded).
# Version 0.1.7:
#   "isnasal" function modified to return False for null string.
#   Switched from calling this script from usfmtec, to running it as a standalone
#   process after the usfmtec/dictionary process. (Calling the script from usfmtec
#   results in the dictionary and algorithmic processes being done in the wrong order.)
# Version 0.1.6:
#   Treat syllable before a hyphen as ultimate syllable. 
# Version 0.1.5:
#   Numerous corrections to spelling rules. Major revisions are to:
#       - final NG rules
#       - O+Circumflex rule
#       - Syllable initial Nasals
# Version 0.1.4:
#   Eliminated incorrect and unnecessary vowel adjustment in syllable "ao"
# Version 0.1.3:
#   Minor bug fixes
# Version 0.1.2:
#   Pre-release/evaluation version, regular expressions and other code cleaned up;
#   ready for integration with dictionary lookup/usfmtec.
# Version 0.0.8:
#   Pre-release/evaluation version prior to integration with dictionary lookup process.
# ###########################################################################

import sys, codecs, unicodedata, os, argparse, string, re

# Dictionary and Config files
##dictFileName = 'L2cDict.csv'
confFileName = 'L2cConf.txt'

# Config settings
ignoreFields = [ ]


# Process Control Flags
# These control the conversion of digits and punctuation.
# It may be best to turn all of these off, and deal with
# these items in a pre-printing process.
LatnChamSpecials = {}       # Dictionary for digits and punctuation
convDigits = True           # Must be off if moving data into Paratext
convPunctuation = True      # Converts
                            #   comma > Danda
                            #   period > Double Danda
                            # Best to insert other Cham puncutation by hand
removePunctuation = False   # Haven't determined yet what punctuation to remove
                            #   - Cham probably retains question mark
                            #   - probably omits quote marks
                            #   - exclamation pt, colon are unknowns

# Global Variables
ErrorFlag = u'\uFFFD'
EFsyllable = u'[Syll]'      # Error Flag suffix: unable to segment word into syllables
EFfinal = u'[FinCl]'        # Error Flag suffix: unable to parse final cluster
EFconsonant = u'[Cons]'     # Error Flag suffix: unable to identify consonant
EFvowel = u'[Vow]'          # Error Flag suffix: unable to identify vowel
TypoCount = 0
# For debugging
dcA = 0     # Debug Counter A

# Cham Script Dictionary:
cs = {
    'a' : u"\uaa00",
    'i' : u"\uaa01",
    'u' : u"\uaa02",
    'e' : u"\uaa03",
    'ai' : u"\uaa04",
    'o' : u"\uaa05",
    'ka' : u"\uaa06",
    'kha' : u"\uaa07",
    'ga' : u"\uaa08",
    'gha' : u"\uaa09",
    'ngue' : u"\uaa0a",
    'nga' : u"\uaa0b",
    'cha' : u"\uaa0c",
    'chha' : u"\uaa0d",
    'j' : u"\uaa0e",
    'jha' : u"\uaa0f",
    'nhue' : u"\uaa10",
    'nha' : u"\uaa11",
    'nhja' : u"\uaa12",
    'ta' : u"\uaa13",
    'tha' : u"\uaa14",
    'da' : u"\uaa15",
    'dha' : u"\uaa16",
    'nue' : u"\uaa17",
    'na' : u"\uaa18",
    'dda' : u"\uaa19",
    'pa' : u"\uaa1a",
    'ppa' : u"\uaa1b",
    'pha' : u"\uaa1c",
    'ba' : u"\uaa1d",
    'bha' : u"\uaa1e",
    'mue' : u"\uaa1f",
    'ma' : u"\uaa20",
    'bba' : u"\uaa21",
    'ya' : u"\uaa22",
    'ra' : u"\uaa23",
    'la' : u"\uaa24",
    'va' : u"\uaa25",
    'ssa' : u"\uaa26",
    'sa' : u"\uaa27",
    'ha' : u"\uaa28",
    'Vaa' : u"\uaa29",
    'Vi' : u"\uaa2a",
    'Vii' : u"\uaa2b",
    'Vei' : u"\uaa2c",
    'Vu' : u"\uaa2d",
    'Voe' : u"\uaa2e",
    'Vo' : u"\uaa2f",
    'Vai' : u"\uaa30",
    'Vau' : u"\uaa31",
    'Vue' : u"\uaa32",
    'Cya' : u"\uaa33",
    'Cra' : u"\uaa34",
    'Cla' : u"\uaa35",
    'Cwa' : u"\uaa36",
    'Fk' : u"\uaa40",
    'Fg' : u"\uaa41",
    'Fng' : u"\uaa42",
    'CsignFng' : u"\uaa43",
    'Fch' : u"\uaa44",
    'Ft' : u"\uaa45",
    'Fn' : u"\uaa46",
    'Fp' : u"\uaa47",
    'Fy' : u"\uaa48",
    'Fr' : u"\uaa49",
    'Fl' : u"\uaa4a",
    'Fss' : u"\uaa4b",
    'CsignFm' : u"\uaa4c",
    'CsignFh' : u"\uaa4d",
    '0' : u"\uaa50",
    '1' : u"\uaa51",
    '2' : u"\uaa52",
    '3' : u"\uaa53",
    '4' : u"\uaa54",
    '5' : u"\uaa55",
    '6' : u"\uaa56",
    '7' : u"\uaa57",
    '8' : u"\uaa58",
    '9' : u"\uaa59",
    'spiral' : u"\uaa5c",
    'danda' : u"\uaa5d",
    'danda2' : u"\uaa5e",
    'danda3' : u"\uaa5f"
}

def getConfig(cf):
    # Read the contents of the configuration file.
    global ignoreFields
    lp = re.compile(ur'\\(?P<marker>\w+)\s+(?P<content>.*)')
    for l in cf.readlines():
        m = lp.match(l)
        if m:
            if m.group('marker') == 'ignoreFields':
                ignoreFields = m.group('content').split()
##    print ignoreFields
    return

def tolist(l) :
    """ convert space separated list into an actual list, and normalize on the way"""
    res = unicodedata.normalize('NFD', l).split()
    return res

def getword(s):
    pWord = re.compile(ur'(?P<word>([a-zA-Z\u0243\u0180\u0110\u0111\u0302\u0306\u031B\u0323]+)(\-[a-zA-Z\u0243\u0180\u0110\u0111\u0302\u0306\u031B\u0323]+)*)')
    m = pWord.search(s)
    if m:
        return s[:m.start('word')], m.group('word'), s[m.end('word'):]
    else:
        return s, u'', u''

def initLatnChamSpecials():
    # Classes of non-word characters (i.e. word-boundary characters)...
    #   1. digits
    ChamDigits = u'\uaa50\uaa51\uaa52\uaa53\uaa54\uaa55\uaa56\uaa57\uaa58\uaa59'
    LatnDigits = u'0123456789'
    #   2. punctuation to convert
    ChamConvPunct = u'\uaa5d\uaa5e'
    LatnConvPunct = u',.'
    #   3. punctuation to omit
    LatnRemPunct = u'"\u0027\u2018\u2019\u201c\u201d'
    # Now concatenate all three classes into a dictionary
    LatnChamSpecials = {}
    if convDigits :
        LatnChamSpecials.update(zip(LatnDigits, ChamDigits))
    if convPunctuation :
        LatnChamSpecials.update(zip(LatnConvPunct, ChamConvPunct))
    if removePunctuation :
        LatnChamSpecials.update(zip(LatnRemPunct, (u'',) * len(LatnRemPunct)))
    
def getSpecial(x):
    # If Latin char x is found in LatnChamSpecials, return its Cham equivalent,
    # otherwise return x
    return LatnChamSpecials.get(x,x)

def convnonword(nonword):
    # "nonword" is a string of non-word-forming chars that precede or separate words.
    # Map any Latin digits and punctuation to Cham digits and punctuation, and
    # return the results.
    return u''.join(map(getSpecial, nonword))

def segment(w):
    # Segment word w into syllables and return the list of syllables
    # Presyllables are always open syllables. (I.e. a consonant string
    # between two vowels always belongs to the second vowel.)

    # Degenerate syllables:
    # The presyllable 'ha' can degenerate to 'h', the 'h' then forming a cluster
    # with the consonants of the following syllable.
    # Degenerate syllables can be identified as an 'h' followed by another
    # initial consonanat, execpt 'r', 'l', 'i', or 'u'.
    # That is:
    #   - 'hi' and 'hu' represent clusters 'h'+'y' and 'h'+'w', respectively.
    #   - 'hr' and 'hl' are ambiguous. They can represent clusters 'h'+'r' and
    #     'h'+'w', respectively, or presyllable "ha" + main syllable starting
    #     with 'r' or 'l'. These must be resolved by dictionary lookup.
    #   - 'h' + any other consonant represents the presyllable "ha" + main
    #     syllable starting with the other consonant.
    # These degenerate syllables need to be expanded to a full presyllable.
    # Fix degenerate syllables by adding an 'a' after the 'h'.
    dp = re.compile(ur'\Ah(?P<tail>[b\u0180cd\u0111gjkmnpstwy].*)')
    w = dp.sub(u'ha\g<tail>', w)

    # pattern to match vowel group
    vgp = re.compile(u'[aeiou\u0302\u0306\u031b]+')
    # pattern to match consonant cluster + vowel
    ccvp = re.compile(u'[bcdfghjklmnpqrstvwxyz\u0180\u0111-]+[aeiou]')

##    # DEBUG
##    print u'word = \u00ab' + w + u'\u00bb'


    syll = []
    l = len(w)
    while l > 0:
        # search for the first vowel group
        vg = vgp.search(w)
        if vg:
            # Is the vowel group followed by a consonat cluster + another vowel
            ccv = ccvp.match(w[vg.end():])
            if ccv:
                # we have a syllable break
                # check for hyphen
                if u'-' in ccv.group():
                    # Hyphenated word: find hyphen and make break before it
                    # Then check the remainder of word
                    i = vg.end() + w[vg.end():].find(u'-')
                    syll = syll + [ w[:i] ]
                    w = w[i:]
                    l = len(w)
                else:
                    # Make syllable break at the end of the vowel group.
                    # Then check remainder of word.
                    syll = syll + [ w[:vg.end()] ]
                    w = w[vg.end():]
                    l = len(w)
##                # DEBUG
##                print u'  syllable break found'
##                print u'    syllable list = ' + str(syll)
##                print u'    remainder = \u00ab' + w + u'\u00bb'
            else:
                # we're on the last syllable
                # include the rest of the word in this syllable
                syll = syll + [ w ]
                # set length of word to 0 -- we're done
                l = 0
##                # DEBUG
##                print u'  No syllable break found'
##                print u'    syllable list = ' + str(syll)
##                print u'    remainder = \u00ab' + w + u'\u00bb'

        else:
            # The word remnant does not contain a valid syllable
            # start with error flag and append remnant to syllable list
            syll = syll + [ ( ErrorFlag + EFsyllable + w ) ]
            # Set length of word to 0 -- we're done.
            l = 0
##            # DEBUG
##            print u'  Invalid syllable'
##            print u'    segment = \u00ab' + w + u'\u00bb'
            
    return syll

def AnalyzeInitialCluster(s):
    # Split the syllable into Hyphen + Initial Consonant + Medial Consonant + Final Cluster (i.e. vowel + final consonant)
    # Any Hyphen that is found can be discarded, since we are now dealing with a single syllable.

    # this works because it will pick up the u and i (if alone) before the rl followed by a vowel.
    pInitAll = re.compile(ur'''(-?(?P<init>[bcdfghjklmnpqrstvwxyz\u0180\u0111]?(?:hh?|g|j)?)(?:(?:(?P<medIUP>u|lu|ru|[rl]?)(?P<finClusIUP>iup))|(?:(?P<med>i|li|u|lu|ru|[rl]?)(?P<finClus>[aeiou][a-z\u0180\u0111\u0302\u0306\u031b]*))))''')
    m = pInitAll.match(s)
    if m:
        initial = m.group('init')
        medial = m.group('med') if m.group('medIUP')==None else m.group('medIUP')
        finalCluster = m.group('finClus') if m.group('finClusIUP')==None else m.group('finClusIUP')
    else:
        # Treat this as a vowel-initial syllable. If there is no vowel, that will be picked up in AnalyzeFinalCluster().
        initial = u''
        medial = u''
        finalCluster = s
    return initial, medial, finalCluster

def AnalyzeFinalCluster(finalCluster):
    # RE patterns for the final cluster
    pVowelAll = re.compile(u'(?P<vowel>[aeiou](?:\u0302|\u0306|\u031b\u0306|\u031b)?)(?P<final>(?:(?:up|[uoyi])$)?)')
    m = pVowelAll.match(finalCluster)
    if m:
        vowel = m.group('vowel')
        final = finalCluster[m.span('vowel')[1]:]
    else:
        # No vowel = Error
        vowel = ErrorFlag + EFfinal + finalCluster
        final = u''
    return vowel, final

LatnCiString = u'b      bh     \u0180 ch     chh    d      dh     dj     \u0111 g      gh     h      j      jh     k      kh     l      m      n      ng     nh     p      ph     r      s      t      th     w      y'
ChamCiString = u'\uaa1d \uaa1e \uaa21 \uaa0c \uaa0d \uaa15 \uaa16 \uaa12 \uaa19 \uaa08 \uaa09 \uaa28 \uaa0e \uaa0f \uaa06 \uaa07 \uaa24 \uaa1f \uaa17 \uaa0a \uaa10 \uaa1a \uaa1c \uaa23 \uaa26 \uaa13 \uaa14 \uaa25 \uaa22'
LatnChamCi = dict(zip(tolist(LatnCiString), tolist(ChamCiString)))
LatnChamCi[''] = ''

LatnCmString = u'i      l      li           lu           r      ru           u'
ChamCmString = u'\uaa33 \uaa35 \uaa35\uaa33 \uaa35\uaa36 \uaa34 \uaa34\uaa36 \uaa36'
LatnChamCm = dict(zip(tolist(LatnCmString), tolist(ChamCmString)))
LatnChamCm[''] = ''

LatnCfList = [ u'c',     u'ch',     u'h',          u'i',     u'k',     u'l',     u'm',          u'n',     u'ng',          u'o',     u'p',     u'r',     u's',      u't',     u'u',     u'up',    u'y',     u'' ]
ChamCfList = [ cs['Fg'], cs['Fch'], cs['CsignFh'], cs['Fy'], cs['Fk'], cs['Fl'], cs['CsignFm'], cs['Fn'], cs['CsignFng'], cs['va'], cs['Fp'], cs['Fr'], cs['Fss'], cs['Ft'], cs['va'], cs['Fp'], cs['Fy'], u'' ]
LatnChamCf = dict(zip(LatnCfList, ChamCfList))

def GetChamC (LatnC, lookup = LatnChamCi):
    global TypoCount, ErrorFlag, EFconsonant
    try :
        return lookup[LatnC]
    except KeyError :
        TypoCount += 1
        return ErrorFlag + EFconsonant + LatnC

def GetChamV (vowel, final, ult, ChamCi):
    # WARNING      WARNING     WARNING
    #       This function returns the MOST COMMON Cham spelling.
    #       Cleanup needs to be done by the calling routine.
    # "vowel" is the Latin vowel
    # Boolean "ult" indicates whether the syllable is an ultimate syllable.
    # Return the most common Cham equivallent of "vowel"

    global TypoCount, ErrorFlag, EFvowel

    #Latin Vowel List:
    # Abbreviations:
    #   Hi=high, Mi=mid, Lo=low
    #   Fr=front, Ce=central, Ba=back
    #   Sh=short
    # phonemic:     HiFr  HiFrSh   MiFr     LoFr  LoFrSh   HiCe     HiCeSh         MiCe     MiCeSh         LoCe  LoCeSh   HiBa  HiBaSh  MiBa     LoBa  LoBaSh
    # orthographic: i     i+brev   e+circ   e     e+brev   u+horn   u+horn+brev    o+horn   o+honr+brev    a     a+breve  u     u+brev  o+circ   o     o+brev
    LatnVstring = u'i     i\u0306  e\u0302  e     e\u0306  u\u031b  u\u031b\u0306  o\u031b  o\u031b\u0306  a     a\u0306  u     u\u0306 o\u0302  o     o\u0306'
    LatnVlist = tolist(LatnVstring) + [u'']
    LatnVDict = dict(zip(LatnVlist, range(len(LatnVlist))))

    # Cham vowel table for vowel initial syllables
    # Latin:      i                  i+brev             e+circ   e                            e+brev                       u+horn                       u+horn+brev                  o+horn                       o+honr+brev                  a                  a+breve  u                  u+brev             o+circ             o                           o+brev
    ChamViOpen= [ cs['i']+cs['Vaa'], cs['i']+cs['Vaa'], cs['e'], cs['a']+cs['Vai']+cs['Vaa'], cs['a']+cs['Vai']+cs['Vaa'], cs['a']+cs['Vue']+cs['Vaa'], cs['a']+cs['Vue']+cs['Vaa'], cs['a']+cs['Voe']+cs['Vaa'], cs['a']+cs['Voe']+cs['Vaa'], cs['a']+cs['Vaa'], cs['a'], cs['u']+cs['Vaa'], cs['u']+cs['Vaa'], cs['o']+cs['Vaa'], cs['a']+cs['Vo']+cs['Vau'], cs['a']+cs['Vo']+cs['Vau'] ]
    ChamViP   = [ cs['i'],           cs['i'],           cs['e'], cs['a']+cs['Vai'],           cs['a']+cs['Vai'],           cs['a']+cs['Vue'],           cs['a']+cs['Vue'],           cs['a']+cs['Voe'],           cs['a']+cs['Voe'],           cs['a'],           cs['a'], cs['u'],           cs['u'],           cs['o'],           cs['a']+cs['Vo']+cs['Vau'], cs['a']+cs['Vo']+cs['Vau'] ]
    ChamViT   = [ cs['i'],           cs['i'],           cs['e'], cs['a']+cs['Vai'],           cs['a']+cs['Vai'],           cs['a']+cs['Vue'],           cs['a']+cs['Vue'],           cs['a']+cs['Voe'],           cs['a']+cs['Voe'],           cs['a'],           cs['a'], cs['u'],           cs['u'],           cs['o'],           cs['a']+cs['Vo']+cs['Vau'], cs['a']+cs['Vo']+cs['Vau'] ]
    ChamViK   = [ cs['i'],           cs['i'],           cs['e'], cs['a']+cs['Vai'],           cs['a']+cs['Vai'],           cs['a']+cs['Vue'],           cs['a']+cs['Vue'],           cs['a']+cs['Voe'],           cs['a']+cs['Voe'],           cs['a']+cs['Vaa'], cs['a'], cs['u'],           cs['u'],           cs['o'],           cs['a']+cs['Vo']+cs['Vau'], cs['a']+cs['Vo']+cs['Vau'] ]
    ChamViC   = [ cs['i'],           cs['i'],           cs['e'], cs['a']+cs['Vai'],           cs['a']+cs['Vai'],           cs['a']+cs['Vue'],           cs['a']+cs['Vue'],           cs['a']+cs['Voe'],           cs['a']+cs['Voe'],           cs['a']+cs['Vaa'], cs['a'], cs['u'],           cs['u'],           cs['o'],           cs['a']+cs['Vo']+cs['Vau'], cs['a']+cs['Vo']+cs['Vau'] ]
    ChamViCH  = [ cs['i'],           cs['i'],           cs['e'], cs['a']+cs['Vai'],           cs['a']+cs['Vai'],           cs['a']+cs['Vue'],           cs['a']+cs['Vue'],           cs['a']+cs['Voe'],           cs['a']+cs['Voe'],           cs['a'],           cs['a'], cs['u'],           cs['u'],           cs['o'],           cs['a']+cs['Vo']+cs['Vau'], cs['a']+cs['Vo']+cs['Vau'] ]
    ChamViShort=[ cs['i'],           cs['i'],           cs['e'], cs['a']+cs['Vai'],           cs['a']+cs['Vai'],           cs['a']+cs['Vue'],           cs['a']+cs['Vue'],           cs['a']+cs['Voe'],           cs['a']+cs['Voe'],           cs['a'],           cs['a'], cs['u'],           cs['u'],           cs['o'],           cs['a']+cs['Vo']+cs['Vau'], cs['a']+cs['Vo']+cs['Vau'] ]

    # Cham vowel table for vowel medial syllables
    # Latin:      i          i+brev     e+circ                        e                   e+brev              u+horn               u+horn+brev          o+horn               o+honr+brev          a          a+breve    u                   u+brev              o+circ              o                            o+brev
    ChamVmOpen= [ cs['Vii'], cs['Vii'], cs['Vo']+cs['Voe']+cs['Vaa'], cs['Vai']+cs['Fy'], cs['Vai']+cs['Fy'], cs['Vue']+cs['Vaa'], cs['Vue']+cs['Vaa'], cs['Voe']+cs['Vaa'], cs['Voe']+cs['Vaa'], cs['Vaa'], cs['Vaa'], cs['Vu']+cs['Vaa'], cs['Vu']+cs['Vaa'], cs['Vo']+cs['Vaa'], cs['Vo']+cs['Vau']+cs['va'], cs['Vo']+cs['Vau']+cs['va'] ]
    ChamVmP   = [ cs['Vi'],  cs['Vi'],  cs['Vo']+cs['Voe'],           cs['Vai'],          cs['Vai'],          cs['Vue'],           cs['Vue'],           cs['Voe'],           cs['Voe'],           u'',       cs['Voe'], cs['Vu'],           cs['Vu'],           cs['Vo'],           cs['Vo']+cs['Vau'],          cs['Vo']+cs['Vau']          ]
    ChamVmT   = [ cs['Vi'],  cs['Vi'],  cs['Vo']+cs['Voe'],           cs['Vai'],          cs['Vai'],          cs['Vue'],           cs['Vue'],           cs['Voe'],           cs['Voe'],           u'',       cs['Voe'], cs['Vu'],           cs['Vu'],           cs['Vo'],           cs['Vo']+cs['Vau'],          cs['Vo']+cs['Vau']          ]
    ChamVmK   = [ cs['Vi'],  cs['Vi'],  cs['Vo']+cs['Voe'],           cs['Vai'],          cs['Vai'],          cs['Vue'],           cs['Vue'],           cs['Voe'],           cs['Voe'],           cs['Vaa'], u'',       cs['Vu'],           cs['Vu'],           cs['Vo'],           cs['Vo']+cs['Vau'],          cs['Vo']+cs['Vau']          ]
    ChamVmC   = [ cs['Vi'],  cs['Vi'],  cs['Vo']+cs['Voe'],           cs['Vai'],          cs['Vai'],          cs['Vue'],           cs['Vue'],           cs['Voe'],           cs['Voe'],           cs['Vaa'], u'',       cs['Vu'],           cs['Vu'],           cs['Vo'],           cs['Vo']+cs['Vau'],          cs['Vo']+cs['Vau']          ]
    ChamVmCH  = [ cs['Vi'],  cs['Vi'],  cs['Vo']+cs['Voe'],           cs['Vai'],          cs['Vai'],          cs['Vue'],           cs['Vue'],           cs['Voe'],           cs['Voe'],           u'',       cs['Voe'], cs['Vu'],           cs['Vu'],           cs['Vo'],           cs['Vo']+cs['Vau'],          cs['Vo']+cs['Vau']          ]
    ChamVmShort=[ cs['Vi'],  cs['Vi'],  cs['Vo']+cs['Voe'],           cs['Vai'],          cs['Vai'],          cs['Vue'],           cs['Vue'],           cs['Voe'],           cs['Voe'],           u'',       cs['Voe'], cs['Vu'],           cs['Vu'],           cs['Vo'],           cs['Vo']+cs['Vau'],          cs['Vo']+cs['Vau']          ]

    # hmm some of the above arrays look repeated (esp. in ChamVis) . Just reference them more than once here and save the rows.
    ChamVis = {'' : ChamViOpen, 'p' : ChamViP, 't' : ChamViT, 'k' : ChamViK, 'c' : ChamViC, 'ch' : ChamViCH}
    ChamVms = {'' : ChamVmOpen, 'p' : ChamVmP, 't' : ChamVmT, 'k' : ChamVmK, 'c' : ChamVmC, 'ch' : ChamVmCH}

    try:
        ind = LatnVDict[vowel]
    except KeyError:
        TypoCount +=1
        return ErrorFlag + EFvowel + vowel

    if ChamCi == u'' :
        return ChamVis.get((final if ult else 'x'), ChamViShort)[ind]
    else :
        return ChamVms.get((final if ult else 'x'), ChamVmShort)[ind]


Nasals = u"\uaa1f\uaa17\uaa0a\uaa10"
def isnasal(c):
    return (c != u'') and (c in Nasals)

def convsyll(s, ult):
    # Convert syllable s into Cham script. Return the converted syllable.
    # Boolean ult indicates whether s is an ultimate syllable.

    global TypoCount

    # ANALYSIS 
    initial, medial, finalCluster = AnalyzeInitialCluster(s)
    vowel, final = AnalyzeFinalCluster(finalCluster)

    # DEBUG...
##    return s
##    return (initial + medial + finalCluster)
##    return (initial + medial + vowel + str(int(LatnShort)) + final)
##    return (initial + medial + vowel + final)

    # CONVERSION
##    ChamCi = GetChamCi (initial)
##    ChamCm = GetChamCm (medial)
    ChamCi = GetChamC (initial, LatnChamCi)
    ChamCm = GetChamC (medial, LatnChamCm)
    # Adjust clusters Null + Ya/Wa (see Cham Vowel Rule 1c below)
    if (ChamCi == u'') and (ChamCm == u'\uaa33' or ChamCm == u'\uaa36') :
        ChamCi = cs['a']
##    # Debug
##    return (ChamCi + ChamCm + vowel + str(int(LatnShort)) + final)
##    return (ChamCi + ChamCm + vowel + final)

##    ChamCf = GetChamCf (final)
    ChamCf = GetChamC (final, LatnChamCf)

    # Get the Cham vowel...
        # Cham Vowel Rules
        # 1) Vowel letters (AA00-AA05) vs vowel signs (AA29-AA32):
        #    a) When a syllable starts with a consonant, the vowel signs are used.
        #       (These are referred to in the script as the "medial vowels".)
        #    b) When a syllable starts with a vowel, the vowel letters (AA00-AA05) are used.
        #       (These are referred to in the script as the "initial vowels".)
        #       Some syllable-initial vowels combine a vowel letter with vowels signs.
        #    c) When a syllable starts with a cluster consisting of a null initial consonant +
        #       the medial consonant /y/ or /w/ (Latn 'i' or 'u'), the Cham initial consonant becomes
        #       Cham Letter A, the Cham medial consonant remains Cham Consonant Sign Ya/Wa, and
        #       the vowel is spelled with the medial vowel.
        # 2) Length contrast:
        #    Whether the vowel has length contrast is affected by:
        #    a) In unstressed presyllables, only 'a' (low central vowel) has length contrast.
        #    b) In stressed, ultimate syllables, the presence of length contrast depends on how the syllable ends, and
        #       on exceptions to the length rules
        #       (1) The mid-front and mid-back vowels (Latn e+circumflex and o+circumflex) never have length contrast.
        #       (2) Unstopped, closed syllables never have length contrast. The default spelling uses the short vowel.
        #       (3) Stopped syllables (i.e. Latn spelling ends with p, t, k, c, or ch) may have length contrast, depending
        #           on the vowel and the final consonant. Thus we need independent rules for each final stop. 
        #       (4) Open syllables are often written with a long vowel.
        #       (5) There are two exceptions to the above rules:
        #           (a) Even when length contrasts exists, it will often be underdifferntiate in the written Cham form.
        #           (b) Rule 2b(4) may apply even to the mid-front and mid-back vowels (Latn e+circumflex and o+circumflex). 
        # 3) With the exception of the nasals, all consonants carry an inherrent short low-central vowel (Latn a + breve).
        #    a) There are two forms of each nasal. The default form carries an inherrent short high-central
        #       vowel (Latn u + horn + breve). The alternate form carries an inherrant short low-central vowel.

    # First get the most common Cham vowel spelling
    if ErrorFlag in vowel:
        ChamV = vowel
    else:
        ChamV = GetChamV (vowel, final, ult, ChamCi)

    # Vowel and Final Consonant adjustments: All returned values should be good for pre-syllables.
    # But vowels and final consonants need to be cleaned up in ultimates.
    if ult:
        if ChamCi == u'' :
            # #### CLEAN UP for initial vowels in ultimate syllables ####
            # Final Y
            if final == u'i' :
                if vowel == u'a\u0306' :
                    # short a + y
                    ChamV = cs['ai']
                    ChamCf = u''
                elif vowel == u'a' :
                    # long a + y
                    ChamV = cs['ai']+cs['Vai']
                    ChamCf = u''
            # Final NG
            elif final==u'ng' and (vowel==u'e\u0302' or vowel==u'e' or vowel==u'u'):
                # These vowels use the "Final NG" instead of the "Final Consonant Sign NG"
                ChamCf = cs['Fng']
##            # Final W
##            elif final == u'o' and vowel == u'a' :
##                # long a + w
##                ChamV = cs['a']+cs['Vaa']
##            elif final == u'u' and vowel == u'a' :
##                # short a + w
##                ChamV = 
##                ChamCf = 
        else:
            # #### CLEAN UP for medial vowels in ultimate syllables ####
            if final == u'i' :
                if vowel == u'a\u0306' :
                    # short a + y
                    # " + u0306 + i" should not occur; correct spelling is "ay"
                    ChamV = cs['Vei']
                    ChamCf = u''
                elif vowel == u'a' :
                    # long a + y
                    ChamV = cs['Vai']
                    ChamCf = u''
                elif vowel == u'o\u0302' :
                    # o-circumflex + y
                    ChamV = cs['Cwa']+cs['Vai']
                    ChamCf = u''
            elif final == u'y' :
                if vowel == u'a' :
                    # short a + y
                    ChamV = cs['Vei']
                    ChamCf = u''
                elif vowel == u'u' :
                    # u + y -- this seems to be homophonous with "ui", but is transliterated differently
                    ChamV = cs['Cwa']+cs['Vei']
                    ChamCf = u''
##            elif final == u'ng' and (vowel == u'i' or vowel == u'i\u0306' or vowel==u'e' or vowel==u'u') :
##                # These vowels use the "Final NG" instead of the "Final Consonant Sign NG"
##                ChamCf = cs['Fng']
            elif final == u'o' and vowel == u'a' :
                # long a + w    ### It's about 50/50 as to whether to use this rule or not.
                ChamV = cs['Vo']+cs['Vau']
                ChamCf = u''
            elif final == u'u' and vowel == u'a' :
                # short a + w
                ChamV = cs['Vu']
                ChamCf = cs['va']
            elif final == u'ch' or final==u'l' or final==u'r':
                if vowel == u'o\u0302':
                    # o+circumflex with final -ch, -l, or -r
                    ChamV = cs['Cwa']+cs['Voe']
            elif final == u'' and medial == u'u' and vowel == u'i' :
##                # In the context "u" + vowel, the "u" represents a medial /w/, except when
##                # the vowel is a syllable final "i", in which case the "u" is the vowel
##                # and the "i" represents a syllable final /y/.
##                ChamCm = u''
##                ChamV = cs['Vu']
##                ChamCf = cs['Fy']
                # MEDIAL W + I is usually written W + EI.
                ChamV = cs['Vei']
            elif final == u'' and medial == u'i' and vowel == u'u' :
                # In the context "i" + vowel, the "i" represents a medial /y/, except when
                # the vowel is a syllable final "u", in which case the "i" is the vowel
                # and the "u" represents a syllable final /w/.
                ChamCm = u''
                ChamV = cs['Vi']
                ChamCf = cs['va']
## # I think the next block is redundant with the "OTHER CLEAN UP ... Nasal consonants" section below.
##            elif (initial==u'm' or initial==u'n' or initial==u'ng' or initial==u'nh') and (vowel==u'u\u031b' or vowel==u'u\u031b\u0306') :
##                # The high-central vowel is inherent in these consonants.
##                # Length needs to be marked in open syllables.
##                if final = u'':
##                    ChamV = u''
##                else:
##                    ChamV = cs['Vaa']
            elif final == u'up':
                if vowel == u'a' :
                    ChamV = cs['Voe']
                elif vowel == u'i' :
                    ChamCm = cs['Cya']
                    ChamV = cs['Vi']
##            elif final==u'ch' and vowel==u'o\u0302' :
##                # final "ch" changes the spelling of hatted o to medial wa + schwa
##                ChamCm = cs['Cwa']
##                ChamV = cs['Voe']

        # OTHER CLEAN UP in ultimate syllables...
        if vowel==u'u' and final==u's' :
            # Final 's' is pronounce /yh/, and when the vowel is 'u', the inherent /y/ is
            # written explicitly: the 'u' vowel is changed to a medial consonant + vowel 'i'.
            ChamCm = cs['Cwa']
            ChamV = cs['Vi']

    # OTHER CLEAN UP -- in all syllables...
    # Nasal consonants:
    if isnasal(ChamCi):
        # Change consonant to alternate form whenever the vowel is an *implied* low central vowel
        #    or an explicit Vowel AI.
        # Retain standard form for all other vowels.
        # Omit any high central vowel, since it is implied in the standard form of the consonant,
        #   but retain any length marker.
        if ChamV == u'' or ChamV == cs['Vaa'] or ChamV == cs['Vai']:
            # I.e. an implied low central vowel--change to alternate nasal consonant
            if ChamCi == u"\uaa1f" :
                ChamCi = cs['ma']
            elif ChamCi == u"\uaa17" :
                ChamCi = cs['na']
            elif ChamCi == u"\uaa0a" :
                ChamCi = cs['nga']
            elif ChamCi == u"\uaa10" :
                ChamCi = cs['nha']
        elif cs['Vue'] in ChamV:
            # Omit the implied high central vowel.
            if cs['Vaa'] in ChamV:
                ChamV = cs['Vaa']   # retain the length marker
            else:
                ChamV = u''

    return (ChamCi + ChamCm + ChamV + ChamCf)


def convword(word):
    # Convert word (Latn script) to newword (Cham script), and return newword

##    # Debug...
##    global dcA
##    dcA = dcA + 1
##    debugWord = u'<' + str(dcA) + u'> ' + word
##    return debugWord
##    return word

    # Segment word into syllables
    syllables = segment(word)
    
    # Convert the syllables one at a time
    newword = u''
    syllcount = len(syllables)
    i = 0
    while i < syllcount:
##        # DEBUG
##        outf.write ('syllable(' + str(i) + ')=' + syllables[i] + '  ')
##        ###
        if syllables[i].startswith(ErrorFlag) :
            # append invalid syllables to the word unconverted
            newword = newword + syllables[i]
        else:
            # Determine if this is an ultimate syllable
            # Note: i==syllcount-1 indicates that we are on the ultimate syllable
            ult = (i==syllcount-1) or (syllables[i+1].startswith('-'))
            # convert and append syllable to new word
            newword = newword + convsyll(syllables[i], ult)
        i = i+1
        
    return newword

def oldtonew(instr):
    # parse the input string, convert it, and return results  

##    # Debug...
##    print instr
##    global dcA
##    dcA = dcA + 1
##    debugLine = u'<' + str(dcA) + u'> ' + instr
##    return debugLine

##    global convDigits, convPunctuation, removePunctuation

    initLatnChamSpecials()
    results = u''
    
    # First check for leading usfm. 
    pUsfm=re.compile(ur'\ufeff?\\(?P<marker>\S+)(?P<tail>\s([0-9,\-\s]*))')
    m = pUsfm.match(instr)
    if m:
        if m.group('marker') in ignoreFields:
            results = instr
            i = len(instr)
        else:
            results = u'\\' + m.group('marker') + m.group('tail')
            i = m.end('tail')
    else:
        i = 0
    if instr[i:] == u'':
        # nothing left to convert
        return results

    # Then normalize what's left and make sure it is in lower case.
    s = unicodedata.normalize('NFD',instr[i:]).lower()

    # Check the dictionary.
    ### Add checkDictionary() function here
    ### s = checkDictionary(s)
    ###
    
    while len(s) > 0:
        # Break s into nonword (all chars before the next word), the next word, and the rest of the line.
        nonword, word, s = getword(s)
        if nonword != u'':
            if convDigits or convPunctuation or removePunctuation :
                results = results + convnonword(nonword)
            else:
                results = results + nonword
        if word != u'':
            results = results + convword(word)
    return (results)

# #############################################
#
# M A I N
#
# #############################################

parser = argparse.ArgumentParser(prog='Latin-to-Cham Converter', epilog='%(prog)s will also look for L2C-ini.txt and L2cDict.csv, unless the initialization and/or dictionary lookup features are turned off.')
parser.add_argument('--noconf', dest='conf', action='store_false', help="Don't read the configuration file.")
##parser.add_argument('--nodict', dest='dict', action='store_false', help="Don't use dictionary lookup.")
parser.add_argument('inFile')
parser.add_argument('outFile')
args = parser.parse_args()

inOK = os.path.exists(args.inFile)
confOK = (args.conf==False) or os.path.exists(confFileName)
dictOK = True
##dictOK = (args.dict==False) or os.path.exists(dictFileName)

if inOK and confOK and dictOK:
    inf = codecs.open(args.inFile, encoding="utf-8")
    outf = codecs.open(args.outFile, "w", encoding="utf-8")
    if args.conf:
        cf = codecs.open(confFileName, encoding="utf-8")
        getConfig(cf)
        cf.close()
##    if args.dict:
##        df = codecs.open(dictFileName, encoding="utf-8")
        ###
        ### loadDictionary() goes here
        ###
##        df.close()

    for l in inf.readlines() :
        outf.write(unicodedata.normalize('NFC', u"".join(oldtonew(unicodedata.normalize('NFD', l)))))
    if TypoCount > 0 :
        print "WARNING: Spelling errors encountered"

    print u'The following fields have been ignored: ' + u' '.join(ignoreFields)
    print 'End of transliteration process'
    inf.close()
    outf.close()
else :
    if not inOK:
        print "Cannot open input file: " + args.inFile
    if not confOK:
        print "Cannot open configuration file: " + confFileName
##    if not dictOK:
##        print "Cannot open dictionary file: " + dictFileName
