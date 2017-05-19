28 April 2006
========================


Three TECkit mapping files are included in this package. Both mapping files can
be used where text has been input "phonetically" as a syllable.

     SILEthAmharic
     SILEthCushitic
     LatinToFidel (multiple)

For example, a text in Amharic looks like this:

     "kvxrsum yvsvmanat lvxnantvm yvmnawvralachu mvlxkt:-
     xgzixvbHer brhan nvw Cvlvmam bvxrsu zvnd kvto yvlvm
     yvmtl yhc nat."

where "kv" will be converted to ETHIOPIC SYLLABLE QA (U+1240).
The SILEthAmharic mapping file should be used in this situation and for most
Semitic languages of Ethiopia.


SILEthCushitic uses a slightly different format than the Amharic. It typically
will show vowel length. An example text might look like this:

     "yesusiici mac'onomiihu, ki`ne'e kunaami sohinutii <<maganu c'aaka
     'ikotane 'isibaani tunisuti horani yoba'a>> yitaataa."

where "sii" will be converted to ethiopic_syllable_si (U+1232) and "si" will be
converted to ethiopic_syllable_se (U+1235).


LatinToFidel (multiple) illustrates the use gemination as well as vowel length.
So "ppii" is converted to ethiopic_syllable_pi(U+1352).


Since it is nearly always necessary to adapt the latin for usage these three
tables give a starting place form modifying for a specific need.

CONTACT
========
For more information on TECkit mapping files, please visit our website at:
http://scripts.sil.org/TECkitIntro or for support concerning these particular
mapping files you may send an email to <computer_ethiopia AT sil DOT org>



