Latin to Cham spelling conversion program for Eastern Cham (cjm)
19 July 2018

This zip archive contains the Latin-to-Cham spelling conversion program as it existed at the time Dave Blood passed away. 

NOTES:

    All Python scripts in this archive were written for Python 2.7, and need to be updated before they can be used in Python 3.
    
    Note that the Cham script uses many historic spellings that do not follow the spelling algorithm implemented in Python. Some of the historic spellings underdifferentiate the current pronunciation of the language, and some overdifferentiate. Thus, a dictionary lookup process is required to correctly apply the historic spellings to the text. For this, we use the dictionary file "L2cDict.ods". The dictionary dated 20 December 2017 is the latest version that Dave Blood left us.
    
    While the spelling conversion is designed to work with any plain text file or file with SFM markup, the implementation represented by this archive has been fine tuned to work with a Paratext translation project, in which the source (Latin script) text is in the folder "c:\My Paratext Projects\CHAM". The converted (Cham script) text is written to the folder "c:\My Paratext Projects\ChamScr". For more help on setting up and using the program for this specific purpse, see the file "Latin-to-Cham Users Guide.docx".
    
    This implementation uses four Python scripts, run in succession. These are documented in the REM lines of the L2c.bat file.
        1. pre-usfm.py makes changes the USFM markup used by Paratext so it is compatible with usfmtec.
        2. usfmtec runs the dictionary lookup process to insert the historic Cham spellings into the text.
        3. post-usfm.py removes the tweaks that pre-usfm.py created, so that the USFM markup is again compatible with Paratext.
        4. cjm-Latn2Cham-[versionNumber].py runs the Latin to Cham spelling algorithm for those words which were not converted by the dictionary lookup.

Jim Brase
SIL International
NRSI