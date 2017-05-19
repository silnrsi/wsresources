Microsoft Word data that is formatted using a symbol-encoded font such as SIL
Galatia or SIL IPA93 is stored using a range of PUA characters, typically U+F020
.. U+F0FF. When using File / Save As... to create an 8-bit plain-text version of
the data, such PUA characters are converted to question marks ('?'). One
solution is to use this Unicode-to-Unicode mapping file, called a
transliterator, to convert the PUA character codes to codepage 1252 before
saving to plain text. 