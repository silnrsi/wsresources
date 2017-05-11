# wsresources

A catch bag of writing system resource files organised by writing system tag

This repository is organized by:
1) langs (languages) using ISO 639-3 codes, 
2) regions and countries (using ISO 3166-1 alpha-2)
3) scripts (using ISO 15924 codes)

It is expected that most resources should fit into the first repo (1). However, it is 
possible that resources are more geared to a region (2) or a script (3). If you put a
resource into "regions" or "scripts" it is highly unlikely there would be a hunspell dictionary.

Each resource should be placed in a folder named by the language's two- or three-letter code.

Examples of possible resource files for a language with code xxx.

```
wsresources
+-- langs
¦   +-- a
¦   ¦   +-- xxx-Arab
¦   ¦   ¦   +-- hunspell
¦   ¦   ¦   ¦   +-- xxx-Arab.aff
¦   ¦   ¦   ¦   +-- xxx-Arab.dic
¦   ¦   ¦   +-- keyboards
¦   ¦   ¦   ¦   +-- msklc
¦   ¦   ¦   ¦   ¦   +-- files .klc, .zip
¦   ¦   ¦   ¦   +-- ukelele
¦   ¦   ¦   ¦   ¦   +-- files .txt, keylayout
¦   ¦   ¦   +-- mappings_custom
¦   ¦   ¦   ¦   ¦   +-- files .map, .tec
¦   ¦   ¦   +-- mappings_unicode
¦   ¦   ¦   ¦   ¦   +-- files .map, .tec
¦   ¦   +-- xxx-Latn
¦   +-- b
¦   +-- ..
¦   +-- z
+-- regions
¦   +-- Africa
¦   ¦   +-- CM
¦   ¦   ¦   +-- keyboards
¦   ¦   ¦   ¦   +-- msklc
¦   ¦   ¦   ¦   ¦   +-- files .klc, .zip
¦   ¦   ¦   ¦   +-- ukelele
¦   ¦   ¦   ¦   ¦   +-- files .txt, keylayout
¦   ¦   ¦   +-- mappings_custom
¦   ¦   ¦   ¦   ¦   +-- files .map, .tec
¦   ¦   ¦   +-- mappings_unicode
¦   ¦   ¦   ¦   ¦   +-- files .map, .tec
¦   ¦   +-- TG
¦   +-- Americas
¦   ¦   +-- BO
¦   ¦   +-- CO
¦   +-- Asia
¦   +-- Europe
¦   +-- Oceania
+-- scripts
    +-- Arab
    +-- Deva
    +-- Gujr
    +-- Latn
        +-- keyboards
        ¦   +-- msklc
        ¦   ¦   +-- sil-ipa
        ¦   ¦   ¦   +-- files .klc, .zip
        ¦   +-- ukelele
        ¦   ¦   +-- sil-ipa
        ¦   ¦   ¦   +-- files .txt, keylayout
        +-- mappings_custom
        ¦   ¦   +-- asap-ipa
        ¦   ¦   ¦   +-- files .map, .tec
        ¦   ¦   +-- sil-ipa-1993
        ¦   ¦   ¦   +-- files .xml, .map, .tec
        ¦   ¦   +-- sil-ipa-1990
        ¦   ¦   ¦   +-- files .map, .tec
        +-- mappings_unicode
```


