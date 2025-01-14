module load bedtools2
module load samtools
BT=`which bedtools`
#BT=${BT-/bin/bedtools}
DATA=${DATA-../data}

check()
{
	if diff $1 $2; then
    	echo ok
	else
    	echo fail
	fi
}

###########################################################
#  Test a basic self intersection. The relative distances
# should all be 0 in this case.
############################################################
echo "    reldist.t01...\c"
echo \
"reldist	count	total	fraction
0.00	43424	43424	1.000" > exp
$BT reldist -a $DATA/refseq.chr1.exons.bed.gz \
            -b $DATA/refseq.chr1.exons.bed.gz > obs
check obs exp
rm obs exp

###########################################################
#  Test intervaks that are randomly distributed. 
# The relative distances should equally represented .
############################################################
echo "    reldist.t02...\c"
echo \
"reldist	count	total	fraction
0.00	164	43424	0.004
0.01	551	43424	0.013
0.02	598	43424	0.014
0.03	637	43424	0.015
0.04	793	43424	0.018
0.05	688	43424	0.016
0.06	874	43424	0.020
0.07	765	43424	0.018
0.08	685	43424	0.016
0.09	929	43424	0.021
0.10	876	43424	0.020
0.11	959	43424	0.022
0.12	861	43424	0.020
0.13	851	43424	0.020
0.14	903	43424	0.021
0.15	893	43424	0.021
0.16	883	43424	0.020
0.17	828	43424	0.019
0.18	917	43424	0.021
0.19	875	43424	0.020
0.20	897	43424	0.021
0.21	986	43424	0.023
0.22	903	43424	0.021
0.23	944	43424	0.022
0.24	904	43424	0.021
0.25	868	43424	0.020
0.26	943	43424	0.022
0.27	933	43424	0.021
0.28	1132	43424	0.026
0.29	881	43424	0.020
0.30	851	43424	0.020
0.31	963	43424	0.022
0.32	950	43424	0.022
0.33	965	43424	0.022
0.34	907	43424	0.021
0.35	885	43424	0.020
0.36	965	43424	0.022
0.37	945	43424	0.022
0.38	911	43424	0.021
0.39	939	43424	0.022
0.40	921	43424	0.021
0.41	951	43424	0.022
0.42	935	43424	0.022
0.43	920	43424	0.021
0.44	916	43424	0.021
0.45	935	43424	0.022
0.46	844	43424	0.019
0.47	852	43424	0.020
0.48	1009	43424	0.023
0.49	939	43424	0.022" > exp
$BT reldist -a $DATA/refseq.chr1.exons.bed.gz \
            -b $DATA/aluY.chr1.bed.gz > obs
check obs exp
rm obs exp


###########################################################
#  Test intervaks that are consistently closer to one another
# than expected.  The distances should be biased towards 0.=
############################################################
echo "    reldist.t03...\c"
echo \
"reldist	count	total	fraction
0.00	20629	43424	0.475
0.01	2629	43424	0.061
0.02	1427	43424	0.033
0.03	985	43424	0.023
0.04	898	43424	0.021
0.05	756	43424	0.017
0.06	667	43424	0.015
0.07	557	43424	0.013
0.08	603	43424	0.014
0.09	488	43424	0.011
0.10	461	43424	0.011
0.11	423	43424	0.010
0.12	427	43424	0.010
0.13	435	43424	0.010
0.14	375	43424	0.009
0.15	367	43424	0.008
0.16	379	43424	0.009
0.17	371	43424	0.009
0.18	346	43424	0.008
0.19	389	43424	0.009
0.20	377	43424	0.009
0.21	411	43424	0.009
0.22	377	43424	0.009
0.23	352	43424	0.008
0.24	334	43424	0.008
0.25	315	43424	0.007
0.26	370	43424	0.009
0.27	330	43424	0.008
0.28	330	43424	0.008
0.29	280	43424	0.006
0.30	309	43424	0.007
0.31	326	43424	0.008
0.32	287	43424	0.007
0.33	294	43424	0.007
0.34	306	43424	0.007
0.35	307	43424	0.007
0.36	309	43424	0.007
0.37	271	43424	0.006
0.38	293	43424	0.007
0.39	311	43424	0.007
0.40	331	43424	0.008
0.41	320	43424	0.007
0.42	299	43424	0.007
0.43	327	43424	0.008
0.44	321	43424	0.007
0.45	326	43424	0.008
0.46	306	43424	0.007
0.47	354	43424	0.008
0.48	365	43424	0.008
0.49	336	43424	0.008
0.50	38	43424	0.001" > exp
$BT reldist -a $DATA/refseq.chr1.exons.bed.gz \
            -b $DATA/gerp.chr1.bed.gz > obs
check obs exp
rm obs exp
