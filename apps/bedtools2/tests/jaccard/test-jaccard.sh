module load bedtools2
module load samtools
BT=`which bedtools`
#BT=${BT-/bin/bedtools}

check()
{
	if diff $1 $2; then
    	echo ok
	else
    	echo fail
	fi
}

###########################################################
#  Test a basic self intersection
###########################################################
echo "    jaccard.t01...\c"
echo \
"intersection	union-intersection	jaccard	n_intersections
110	110	1	2" > exp
$BT jaccard -a a.bed -b a.bed > obs
check obs exp
rm obs exp


echo "    jaccard.t02...\c"
echo \
"intersection	union-intersection	jaccard	n_intersections
10	140	0.0714286	1" > exp
$BT jaccard -a a.bed -b b.bed > obs
check obs exp
rm obs exp

echo "    jaccard.t03...\c"
echo \
"intersection	union-intersection	jaccard	n_intersections
10	200	0.05	1" > exp
$BT jaccard -a a.bed -b c.bed > obs
check obs exp
rm obs exp

# TEST #4 IS DEPRECATED

###########################################################
#  Test stdin
###########################################################
echo "    jaccard.t05...\c"
echo \
"intersection	union-intersection	jaccard	n_intersections
10	140	0.0714286	1" > exp
cat a.bed | $BT jaccard -a - -b b.bed > obs
check obs exp
rm obs exp


###########################################################
#  Test symmetry
###########################################################
echo "    jaccard.t06...\c"
$BT jaccard -a a.bed -b b.bed > obs1
$BT jaccard -a b.bed -b a.bed > obs2
check obs1 obs2
rm obs1 obs2

###########################################################
#  Test partially matching blocks without -split option.
###########################################################
echo "    jaccard.t07...\c"
echo \
"intersection	union-intersection	jaccard	n_intersections
10	50	0.2	1" > exp
$BT jaccard -a three_blocks_match.bed -b e.bed > obs
check obs exp
rm obs exp


###########################################################
#  Test partially matching blocks with -split option.
###########################################################
echo "    jaccard.t08...\c"
echo \
"intersection	union-intersection	jaccard	n_intersections
5	35	0.142857	1" > exp
$BT jaccard -a three_blocks_match.bed -b e.bed -split > obs
check obs exp
rm obs exp

###########################################################
#  Test jaccard of Bam with Bam
###########################################################
echo "    jaccard.t09...\c"
echo \
"intersection	union-intersection	jaccard	n_intersections
10	150	0.0666667	1" > exp
$BT jaccard -a a.bam -b three_blocks_match.bam -bed > obs
check exp obs
rm exp obs

###########################################################
#  Test jaccard with mixed strand files
###########################################################
echo "    jaccard.t10...\c"
echo \
"intersection	union-intersection	jaccard	n_intersections
145	180	0.805556	2" >exp
$BT jaccard -a aMixedStrands.bed -b bMixedStrands.bed > obs
check obs exp
rm obs exp

###########################################################
#  Test jaccard with mixed strand files, -s option
#  (match strand, either forward or reverse)
###########################################################
echo "    jaccard.t11...\c"
echo \
"intersection	union-intersection	jaccard	n_intersections
120	290	0.413793	4" >exp
$BT jaccard -a aMixedStrands.bed -b bMixedStrands.bed -s > obs
check obs exp
rm obs exp

###########################################################
#  Test jaccard with mixed strand files, -S + option
#  (match strand, forward only)
###########################################################
echo "    jaccard.t12...\c"
echo \
"intersection	union-intersection	jaccard	n_intersections
40	135	0.296296	2" >exp
$BT jaccard -a aMixedStrands.bed -b bMixedStrands.bed -S + > obs
check obs exp
rm obs exp

###########################################################
#  Test jaccard with mixed strand files, -S - option
#  (match strand, reverse only)
###########################################################
echo "    jaccard.t13...\c"
echo \
"intersection	union-intersection	jaccard	n_intersections
80	155	0.516129	2" > exp
$BT jaccard -a aMixedStrands.bed -b bMixedStrands.bed -S - > obs
check obs exp
rm obs exp

