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
#  Test a basic file
###########################################################
echo -e "    spacing.t01...\c"
echo \
"chr1	20	30	.
chr1	25	40	-1
chr1	40	50	0
chr1	60	80	10
chr1	75	100	-1
chr1	105	110	5
chr2	115	130	.
chr2	120	160	-1
chr2	170	180	10" > exp
$BT spacing -i a.bed  > obs
check obs exp
rm obs exp
