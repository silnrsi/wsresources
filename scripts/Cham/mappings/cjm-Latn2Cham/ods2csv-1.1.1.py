#!/usr/bin/python

# ods2csv.py
# convert a dictionary lookup file from .ods format to .csv format
# Written by Jim Brase, SIL International, 2015
#            jim_brase@sil.org
# Copyright SIL International 2015
# #######################################################################################
#
# KNOWN BUGS:
#
# ***************************************************************************************
# History:
# ***************************************************************************************
# Version 1.1.1
#	Reports version number.
# Version 1.1.0:
#	Permits a dictionary record to be turned off. 
# Version 1.0.0:
#   Initial release.
# ###########################################################################


import sys, codecs, os, unicodedata, string, re
import pyexcel
import pyexcel.ext.ods

version = '1.1.1'

def commandLine():
	print "ODS to CSV dictionary converter; Version " + version
	print "Convert a dictionary lookup file from .ods format to .csv format"
	print
	print "Syntax:"
	print "    python ods2csv.py [-st=M/N/S] FILE.ods "
	print "where"
	print "    \"FILE.ods\" is the name of input file"
	print "        + The extension must be \".ods\""
	print "        + Output will be written to \"FILE.csv\""
	print "        + I/o files are in UTF-8."
	print "    \"M/N/S\" are decimal digits specifying the column numbers for source, replacement, and status:"
	print "        + Do not put any spaces in this string."
	print "        + M = source column number (default = 0)"
	print "        + N = replacement column number (default = 1)"
	print "        + S = status column number (default = 2)"
	print
	print "Source and Replacement columns must not contain commas."
	print "Source text will be written to column 0 in the CSV file."
	print "Replacement text will be written to column 1 in the CSV file."
	print "Status is ON (default), or OFF."
	print "    + case insensitive."
	print "    + OFF disables entry (i.e. the line is not written to the CSV file)."
	print "    + A blank cell is equivalent to ON"
	print "Other columns from the ODS file will be ignored."
	return

def programHelp():
	commandLine()
	print
	print "Ods2csv is a command line filter that can be used convert an "
	print "ODS file to a CSV file for use by tools such as USFMTEC. "
	print "Many script-to-script transliteration processes require a "
	print "dictionary lookup process. The dictionary is most easily edited "
	print " in ODS format, but USFMTEC requires the dictionary to be "
	print "in CSV format. It is recommended that ods2csv be used in a "
	print "batch process to ensure that the CSV file is always up to "
	print "date relative to the ODS file on which it depends."
	print
	print "Example:"
	print "The following code will run ods2csv whenever the ODS file "
	print "is newer than the CSV file."
	print "    REM Confirm Latin2ScriptX.csv is up to date..."
	print "    for /F %%f in ('dir /b /OD Latin2ScriptX.csv Latin2ScriptX.ods ^| more +1') do set NEWER=%%f"
	print "    if /I not %NEWER%==Latin2ScriptX.ods goto dependenciesOK"
	print "    python ods2csv.py Latin2ScriptX.ods"
	print "    :dependenciesOK"
	print "    ..."
	return


if __name__ == "__main__" :

	sc = 0	# default source column
	tc = 1  # default target column
	statc = 2 # default status column
	
	# Check command line
	if len(sys.argv) < 2:
		programHelp()
		exit()
	else:
		i = 1
		if sys.argv[i].startswith('-st='):
			c = sys.argv[i].strip('-st=').split('/')
			if len(c) < 3:
				print "ERROR: invalid source/target column specification"
				commandLine()
				exit()
			sc = int(c[0])
			tc = int(c[1])
			statc = int(c[2])
			i += 1
		inName = sys.argv[i]
		outName = inName.rsplit('.',1)[0] + '.csv'

	if os.path.exists(inName) :
		outf = codecs.open(outName, "w", encoding="utf-8")
		array = pyexcel.get_array(file_name=inName)
		for row in array:
			if row[statc].lower().strip() != 'off':
				outf.write(row[sc] + u',' + row[tc] + u'\r\n')
		outf.close()
	else:
		print "ERROR: Unable to find input file."
		commandLine()
