

open(PINYIN, '>:utf8', 'YiPinyinMap.map') or die "cannot open YiPinyinMap.map\n";
open(IPA, '>YiIPAMap.map') or die "cannot open YiIPAMap.map\n";
open(YIDATA,'<:utf8','YI_DATA.TXT') or die "cannot open YI_DATA.TXT\n";


print PINYIN <<EOT;

EncodingName        "Simple Yi to YiPinyin Unicode"
DescriptiveName     "Simple Yi to YiPinyin Unicode"
Version             "0.1"
LHSName             "Unicode"
RHSName             "Unicode"

Pass(Unicode)

EOT

print IPA <<EOS;

EncodingName        "Yi to IPA Unicode"
DescriptiveName     "Yi to IPA Unicode"
Version             "0.1"
LHSName             "Unicode"
RHSName             "Unicode"

Pass(Unicode)

EOS

while (<YIDATA>) {
	next if not /^U\+/; 

	/^U\+(A...)\s*\S\s*(\S+)\s*(\S+)\s*/;

	#printf "U+%s\t%s\t%s\n",$1,lc($2),$3;
	printf PINYIN "U+%s > %s %s\n",$1,tohex(lc($2)), tohex(" ");
	printf PINYIN "U+%s / _ # > %s\n",$1,tohex(lc($2));

	printf IPA "U+%s > %s \n",$1,tohex($3);

}


close(PINYIN);
close(IPA);
close(YIDATA);

sub tohex {
	my($s) = @_;

    return  join(" ", map { sprintf("U+%04X", $_) } unpack("U*", $s) );

}
