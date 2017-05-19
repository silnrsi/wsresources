2007-06-26

These are experimental mapping files for the PitchContours
fonts. Nine codepoints for the pitches were placed in
SIL Corporate PUA at U+F1F1..U+F1F9. Each of these 
mapping files require the use of 
Charis SIL (http://scripts.sil.org/CharisSILfont) or 
Doulos SIL (http://scripts.sil.org/DoulosSILfont) 
version 4.1 or greater. They will turn into contours 
if used in Graphite applications. It is unlikely that 
any other fonts will contain these codepoints. 


It is possible these mapping files will not work for
you since the fonts sometimes were used inconsistently. At
times data from one melody was placed on two lines in order
to make it stretched out. With that anomaly, the brackets
in the fonts were also much larger to span several lines.

In order for these mapping files to work, data for a melody 
*must* be on one line, it cannot be on two separate lines 
or the data will not be converted properly. If you put your
data on several lines we have no way to automatically convert
that data for you.

It is also important to remember that some of these fonts 
had very large square brackets. It is impossible to maintain
the large size of the brackets in an encoding conversion.
If you wish to have large brackets you will have to 
manually go through your document and resize the brackets
by changing the font size.


MAPPING FILES

The "PitchContours" TECkit mapping is intended for
converting data which used the "PitchContours" or 
"PitchContoursSymbol" fonts. It will convert the
pitch contours to the SIL Corporate PUA codepoints. 

The "ContourContour" TECkit mapping is intended for
converting data which used the 
"Contour Contour SILDoulos" font. It will convert the
pitch contours to the SIL Corporate PUA codepoints. 

The "Contour4Contour4" TECkit mapping is intended for
converting data which used the 
"Contour4 Contour4 SILDoulos" and 
"Cont12 Cont12 SILDoulos" font. It will convert the
pitch contours to the SIL Corporate PUA codepoints. 

The "Contour6Contour6" TECkit mapping is intended for
converting data which used the 
"Contour6 Contour6 SILDoulos" font. It will convert the
pitch contours to the SIL Corporate PUA codepoints. 

The PitchContours2Num TECkit mapping should be used
if you want to convert from the pitches to numbers. The
lowest bar is number 1 and the highest is number 9.

The PitchContours2NumSup TECkit mapping should be used
if you want to convert from the pitches to superscript numbers.
The lowest bar is number 1 and the highest is number 9.


SUPPORT

These maps have been minimally tested and feedback
is encouraged. Please contact lorna_priest@sil.org
if you have feedback or suggestions.
