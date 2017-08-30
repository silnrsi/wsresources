Compiled and uncompiled TECkit conversion tables are included here.
The DevUni-LimUni12 mapping file gives the ability to convert between Devanagari script and Limbu script.

Notes on DevUni-LimUni10.map

1. candrabindu and anusvara both map to anusvara
2. visarga maps to kemphreng
3. halant maps to sa_i (unless on a cons with small final form) 
4. nothing maps to U+1928 (vowel o, titcha)
5. nothing maps to U+1940 (loo sign)
6. i: and ii both map to i+kemphreng. ii should never occur in Devanagari. If it does, the reverse map will reverse it as i:.
7. comma maps to dot. On reverse, dot is retained as dot if following a digit (eg, Scr refs Mat 1.10) but any other occurrence of dot will be changed to comma when converting in the reverse direction.

s.smith
08-May-2009

ver 1.1: 13-May-2009
Rewritten to scrap the initial pass that removed all ZW(N)J before doing anything else. We need to preserve ZW(N)J in certain contexts to distinguish 1/2C+glide from C-halant+glide, as they transfer differently. Need to preserve the distinction on the reverse too.

ver 1.2: 12-Jun-1009
Modified so that da+glide always converts to full Da + subjoined glide, even if the Devanagari has explicit halant (ZWJ or ZWNJ). On reverse, it always comes back as the conjunct dya/dra/dwa. Did this by removing da from [DevC] and [LimC] and adding explicit rules to handle da+glide. Also removed da from [DevCOther] and [LimCOther] so that ZWNJ on Dev side doesn't produce sa_i, and commented out dya/dwa conjunct blocking on reverse, so it will come back as conjunct.
