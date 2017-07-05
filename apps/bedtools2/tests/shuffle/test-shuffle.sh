BT=${BT-/bin/bedtools}
check()
{
	if diff $1 $2; then
    	echo ok
		return 1
	else
    	echo fail
		return 0
	fi
}


###########################################################
# test basic shuffle
###########################################################
echo "    shuffle.t1...\c"
echo \
"chr20	61832106	61832574	trf	789
chr6	115569999	115570172	trf	346
chr12	19014188	19014428	trf	434
chrX	149678273	149678495	trf	273
chr13	6248722	6248899	trf	187
chr4	35820891	35821056	trf	199
chr6	169069340	169069478	trf	242
chr1	222543425	222543460	trf	70
chr1	48470369	48470466	trf	79
chr14	64011984	64012025	trf	73" > exp
$BT shuffle -seed 42 -i simrep.bed  \
            -g ../genomes/human.hg19.genome | head > obs
check obs exp
rm obs exp

###########################################################
# test basic shuffle with -incl (choose intervals randomly)
###########################################################
echo "    shuffle.t2...\c"
echo \
"chr1	2815874	2816342	trf	789
chr1	529762	529935	trf	346
chr3	451246	451486	trf	434
chr1	3354492	3354714	trf	273
chr4	323049	323226	trf	187
chr1	2274273	2274438	trf	199
chr2	108019	108157	trf	242
chr1	4924467	4924502	trf	70
chr1	4623059	4623156	trf	79
chr5	247430	247471	trf	73
chr1	4156954	4156986	trf	64
chr2	395802	395907	trf	149
chr1	2964641	2964679	trf	58
chr4	287685	288155	trf	278
chr2	489835	490305	trf	339
chr3	719832	720260	trf	202
chr1	4463477	4463520	trf	59
chr5	180120	180160	trf	62
chr1	3459259	3459294	trf	52
chr1	4647380	4647557	trf	302" > exp
$BT shuffle -incl incl.bed -seed 42 -i simrep.bed  \
            -g ../genomes/human.hg19.genome | head -20 > obs
check obs exp
rm obs exp

##############################################################
# test basic shuffle with -incl (choose chroms randomly first)
##############################################################
echo "    shuffle.t3...\c"
echo \
"chr1	2815874	2816342	trf	789
chr1	529762	529935	trf	346
chr3	451246	451486	trf	434
chr1	3354492	3354714	trf	273
chr4	323049	323226	trf	187
chr1	2274273	2274438	trf	199
chr2	108019	108157	trf	242
chr1	4924467	4924502	trf	70
chr1	4623059	4623156	trf	79
chr5	247430	247471	trf	73
chr1	4156954	4156986	trf	64
chr2	395802	395907	trf	149
chr1	2964641	2964679	trf	58
chr4	287685	288155	trf	278
chr2	489835	490305	trf	339
chr3	719832	720260	trf	202
chr1	4463477	4463520	trf	59
chr5	180120	180160	trf	62
chr1	3459259	3459294	trf	52
chr1	4647380	4647557	trf	302" > exp
$BT shuffle -incl incl.bed -chromFirst -seed 42 -i simrep.bed  \
            -g ../genomes/human.hg19.genome | head -20 > obs
check obs exp
rm obs exp


##############################################################
# test basic shuffle with -excl
##############################################################
echo "    shuffle.t4...\c"
echo -n "" > exp
$BT shuffle -seed 42 -i simrep.bed  \
            -g ../genomes/human.hg19.genome \
            -excl excl.bed \
| $BT intersect -a - -b excl.bed > obs
check obs exp
rm obs exp

##############################################################
# test basic shuffle with 
##############################################################
echo "    shuffle.t5...\c"
echo \
"chr4	35820891	35821056	trf	199
chr1	222543425	222543460	trf	70
chr1	222543425	222543460	trf	70
chr1	48470369	48470466	trf	79
chr1	48470369	48470466	trf	79
chr3	70445746	70445851	trf	149
chr3	58195572	58196000	trf	202
chr3	90048150	90048533	trf	712
chr4	33975723	33975766	trf	86
chr2	84439645	84439715	trf	104" > exp
$BT shuffle -seed 42 -i simrep.bed  \
            -g ../genomes/human.hg19.genome \
| $BT intersect -a - -b excl.bed | head > obs
check obs exp
rm obs exp
