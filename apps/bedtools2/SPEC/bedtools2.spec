%define priority 2260
%define dir_exists() (if [ ! -d /opt/biology/%{name}/%{version} ]; then \
  echo "/opt/biology/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bedtools2
Version:	2.26.0
Release:	1%{?dist}
Summary:	Tools for handing BED files
Group:		Applications/Engineering
License:	GPL
URL:		https://github.com/arq5x/bedtools2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
BEDTools is a suite of utilities for comparing genomic features in BED format. 
These utilities allow one to quickly address tasks such as: 1. Intersecting 
two BED files. 2. Merge overlapping features. 3. Paired-end overlaps.

%pre
%dir_exists

%post
alternatives \
  --install %{_bindir}/bedtools bedtools /opt/biology/%{name}/%{version}/bin/bedtools %{priority} \
  --slave %{_bindir}/annotateBed annotateBed /opt/biology/%{name}/%{version}/bin/annotateBed \
  --slave %{_bindir}/bamToBed bamToBed /opt/biology/%{name}/%{version}/bin/bamToBed \
  --slave %{_bindir}/bamToFastq bamToFastq /opt/biology/%{name}/%{version}/bin/bamToFastq \
  --slave %{_bindir}/bed12ToBed6 bed12ToBed6 /opt/biology/%{name}/%{version}/bin/bed12ToBed6 \
  --slave %{_bindir}/bedpeToBam bedpeToBam /opt/biology/%{name}/%{version}/bin/bedpeToBam \
  --slave %{_bindir}/bedToBam bedToBam /opt/biology/%{name}/%{version}/bin/bedToBam \
  --slave %{_bindir}/bedToIgv bedToIgv /opt/biology/%{name}/%{version}/bin/bedToIgv \
  --slave %{_bindir}/closestBed closestBed /opt/biology/%{name}/%{version}/bin/closestBed \
  --slave %{_bindir}/clusterBed clusterBed /opt/biology/%{name}/%{version}/bin/clusterBed \
  --slave %{_bindir}/complementBed complementBed /opt/biology/%{name}/%{version}/bin/complementBed \
  --slave %{_bindir}/coverageBed coverageBed /opt/biology/%{name}/%{version}/bin/coverageBed \
  --slave %{_bindir}/expandCols expandCols /opt/biology/%{name}/%{version}/bin/expandCols \
  --slave %{_bindir}/fastaFromBed fastaFromBed /opt/biology/%{name}/%{version}/bin/fastaFromBed \
  --slave %{_bindir}/flankBed flankBed /opt/biology/%{name}/%{version}/bin/flankBed \
  --slave %{_bindir}/genomeCoverageBed genomeCoverageBed /opt/biology/%{name}/%{version}/bin/genomeCoverageBed \
  --slave %{_bindir}/getOverlap getOverlap /opt/biology/%{name}/%{version}/bin/getOverlap \
  --slave %{_bindir}/groupBy groupBy /opt/biology/%{name}/%{version}/bin/groupBy \
  --slave %{_bindir}/intersectBed intersectBed /opt/biology/%{name}/%{version}/bin/intersectBed \
  --slave %{_bindir}/linksBed linksBed /opt/biology/%{name}/%{version}/bin/linksBed \
  --slave %{_bindir}/mapBed mapBed /opt/biology/%{name}/%{version}/bin/mapBed \
  --slave %{_bindir}/maskFastaFromBed maskFastaFromBed /opt/biology/%{name}/%{version}/bin/maskFastaFromBed \
  --slave %{_bindir}/mergeBed mergeBed /opt/biology/%{name}/%{version}/bin/mergeBed \
  --slave %{_bindir}/multiBamCov multiBamCov /opt/biology/%{name}/%{version}/bin/multiBamCov \
  --slave %{_bindir}/multiIntersectBed multiIntersectBed /opt/biology/%{name}/%{version}/bin/multiIntersectBed \
  --slave %{_bindir}/nucBed nucBed /opt/biology/%{name}/%{version}/bin/nucBed \
  --slave %{_bindir}/pairToBed pairToBed /opt/biology/%{name}/%{version}/bin/pairToBed \
  --slave %{_bindir}/pairToPair pairToPair /opt/biology/%{name}/%{version}/bin/pairToPair \
  --slave %{_bindir}/randomBed randomBed /opt/biology/%{name}/%{version}/bin/randomBed \
  --slave %{_bindir}/shiftBed shiftBed /opt/biology/%{name}/%{version}/bin/shiftBed \
  --slave %{_bindir}/shuffleBed shuffleBed /opt/biology/%{name}/%{version}/bin/shuffleBed \
  --slave %{_bindir}/slopBed slopBed /opt/biology/%{name}/%{version}/bin/slopBed \
  --slave %{_bindir}/sortBed sortBed /opt/biology/%{name}/%{version}/bin/sortBed \
  --slave %{_bindir}/subtractBed subtractBed /opt/biology/%{name}/%{version}/bin/subtractBed \
  --slave %{_bindir}/tagBam tagBam /opt/biology/%{name}/%{version}/bin/tagBam \
  --slave %{_bindir}/unionBedGraphs unionBedGraphs /opt/biology/%{name}/%{version}/bin/unionBedGraphs \
  --slave %{_bindir}/windowBed windowBed /opt/biology/%{name}/%{version}/bin/windowBed \
  --slave %{_bindir}/windowMaker windowMaker /opt/biology/%{name}/%{version}/bin/windowMaker

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove bedtools /opt/biology/%{name}/%{version}/bin/bedtools
fi


%files

%changelog
* Tue Jun 27 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.26.0-1
- Fixed a major memory leak when using -sorted. Thanks to Emily Tsang and
  Stephen Montgomery.
- Fixed a bug for BED files containing a single record with no newline. Thanks
  to @jmarshall.
- The getfasta tool includes name, chromosome and position in fasta headers
  when the -name option is used. Thanks to @rishavray.
- Fixed a bug that now forces the coverage tool to process every record in the
  -a file.
- Fixed a bug preventing proper processing of BED files with consecutive tabs.
- VCF files containing structural variants now infer SV length from either the
  SVLEN or END INFO fields. Thanks to Zev Kronenberg.
- Resolve off by one bugs when intersecting GFF or VCF files with BED files.
- The shuffle tool now uses roulette wheel sampling to shuffle to -incl regions
  based upon the size of the interval. Thanks to Zev Kronenberg and Michael
  Imbeault.
- Fixed a bug in coverage that prevented correct calculation of depth when
  using the -split option.
- The shuffle tool warns when an interval exceeds the maximum chromosome
  length.
- The complement tool better checks intervals against the chromosome lengths.
- Fixes for stddev, min, and max operations. Thanks to @jmarshall.
- Enabled stdev, sstdev, freqasc, and freqdesc options for groupby.
- Allow -s and -w to be used in any order for makewindows.
- Added new -bedOut option to getfasta.
- The -r option forces the -F value for intersect.
- Add -pc option to the genomecov tool, allowing coverage to be calculated
  based upon paired-end fragments.
