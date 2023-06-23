# wsresources

A catch bag of writing system resource files organised by language tag, region, or script. Writing system resources are things like dictionaries, keyboards, and data conversion mappings.

This repository is organized by:
1) langs (languages) - using [ISO 639-3 codes](https://iso639-3.sil.org/code_tables/639/data). Each resource should be placed in a folder named by the language's two- or three-letter code.
2) regions and countries - using [ISO 3166-1 alpha-2](https://www.iso.org/obp/ui/#search/code/)
3) scripts - using [ISO 15924 codes](http://www.unicode.org/iso15924/codelists.html)

It is expected that most resources should fit into the first repo (1). However, it is 
possible that resources are more geared to a region (2) or a script (3). If you put a
resource into "regions" or "scripts" it is highly unlikely there would be a hunspell dictionary.

## Structure

Examples of possible resource files for a language with code xxx. 

Regarding Keyman keyboards, this repo is likely a good home for legacy Keyman keyboards. However, for Unicode Keyman keyboards we encourage them to be submitted to the [Keyman repo](https://github.com/keymanapp/keyboards). Existing Keyman keyboards can be found here (search by language name or code): [Keyman](https://keyman.com/).

The .map files are source files for use with [TECkit](https://software.sil.org/teckit). The compiled `.map` files are `.tec`. The map files can be used directly with TECkit or with [SIL Converters](https://software.sil.org/silconverters). Mapping files can also be used with [OpenOffice Linguistic Tools](https://software.sil.org/oolt/). Instructions are found on those sites.

```
wsresources
├- langs
│   ├- a
│   ├- ..
│   ├- x
│   │  ├- xxx-Arab
│   │  │   ├- hunspell
│   │  │   │   ├- xxx-Arab.aff
│   │  │   │   └- xxx-Arab.dic
│   │  │   ├- keyboards
│   │  │   │   ├- msklc
│   │  │   │   │   └- files .klc, .zip
│   │  │   │   ├- xkb
│   │  │   │   │   └- files *.*
│   │  │   │   └- ukelele
│   │  │   │       └- files .txt, .keylayout
│   │  │   ├- legacy
│   │  │   │   └- encoding name
│   │  │   │       ├- mappings
│   │  │   │       │   └- files .map, .tec
│   │  │   │       └- keyboards
│   │  │   │           └- .kmn etc.
│   │  │   └- mappings
│   │  │           └- files .map, .tec
│   │  └- xxx-Latn
│   ├- y
│   └- z
├- regions
│   ├- Africa
│   │   ├- CM
│   │   │   ├- keyboards
│   │   │   │   ├- msklc
│   │   │   │   │   └─- files .klc, .zip
│   │   │   │   ├- xkb
│   │   │   │   │   └- files *.*
│   │   │   │   └─- ukelele
│   │   │   │       └─- files .txt, .keylayout
│   │   │   ├- legacy
│   │   │   │   └- encoding name
│   │   │   │       ├- mappings
│   │   │   │           └─- files .map, .tec
│   │   │   │       └- keyboards
│   │   │   │           └─- .kmn etc.
│   │   │   └- mappings
│   │   │       └─- files .map, .tec
│   │   └- TG
│   ├- Americas
│   │   ├- BO
│   │   └- CO
│   ├- Asia
│   ├- Europe
│   └- Oceania
└- scripts
    ├- Arab
    ├- Deva
    ├- Gujr
    └- Latn
        ├- keyboards
        │   ├- msklc
        │   │   └─- sil-ipa
        │   │       └─ files .klc, .zip
        │   ├- xkb
        │   │   └─- sil-ipa
        │   │       └─ files *.*
        │   └- ukelele
        │       └─- sil-ipa
        │           └─ files .txt, .keylayout
        ├- legacy
        │   ├- asap-ipa
        │   │   ├- mappings
        │   │   │   └─ files .map, .tec
        │   │   └─ keyboards
        │   │       └─ .kmn etc.
        │   ├- sil-ipa-1993
        │   └─ sil-ipa-1990
        └─ mappings
```

## Other resources

Please submit Keyman keyboards to the [Keyman repo](https://github.com/keymanapp/keyboards).

Please submit SIL Locale Data to the [SIL Locale Data Repository](https://github.com/silnrsi/sldr) or to [ScriptSource](https://scriptsource.org).

## License

Unless otherwise indicated, all resources are under [The MIT License (MIT)](LICENSE).
