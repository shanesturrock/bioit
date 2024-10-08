%define priority 2310
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bedtools2
Version:	2.31.0
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
  --install %{_bindir}/bedtools bedtools /opt/bioit/%{name}/%{version}/bin/bedtools %{priority} \
  --slave %{_bindir}/annotateBed annotateBed /opt/bioit/%{name}/%{version}/bin/annotateBed \
  --slave %{_bindir}/bamToBed bamToBed /opt/bioit/%{name}/%{version}/bin/bamToBed \
  --slave %{_bindir}/bamToFastq bamToFastq /opt/bioit/%{name}/%{version}/bin/bamToFastq \
  --slave %{_bindir}/bed12ToBed6 bed12ToBed6 /opt/bioit/%{name}/%{version}/bin/bed12ToBed6 \
  --slave %{_bindir}/bedpeToBam bedpeToBam /opt/bioit/%{name}/%{version}/bin/bedpeToBam \
  --slave %{_bindir}/bedToBam bedToBam /opt/bioit/%{name}/%{version}/bin/bedToBam \
  --slave %{_bindir}/bedToIgv bedToIgv /opt/bioit/%{name}/%{version}/bin/bedToIgv \
  --slave %{_bindir}/closestBed closestBed /opt/bioit/%{name}/%{version}/bin/closestBed \
  --slave %{_bindir}/clusterBed clusterBed /opt/bioit/%{name}/%{version}/bin/clusterBed \
  --slave %{_bindir}/complementBed complementBed /opt/bioit/%{name}/%{version}/bin/complementBed \
  --slave %{_bindir}/coverageBed coverageBed /opt/bioit/%{name}/%{version}/bin/coverageBed \
  --slave %{_bindir}/expandCols expandCols /opt/bioit/%{name}/%{version}/bin/expandCols \
  --slave %{_bindir}/fastaFromBed fastaFromBed /opt/bioit/%{name}/%{version}/bin/fastaFromBed \
  --slave %{_bindir}/flankBed flankBed /opt/bioit/%{name}/%{version}/bin/flankBed \
  --slave %{_bindir}/genomeCoverageBed genomeCoverageBed /opt/bioit/%{name}/%{version}/bin/genomeCoverageBed \
  --slave %{_bindir}/getOverlap getOverlap /opt/bioit/%{name}/%{version}/bin/getOverlap \
  --slave %{_bindir}/groupBy groupBy /opt/bioit/%{name}/%{version}/bin/groupBy \
  --slave %{_bindir}/intersectBed intersectBed /opt/bioit/%{name}/%{version}/bin/intersectBed \
  --slave %{_bindir}/linksBed linksBed /opt/bioit/%{name}/%{version}/bin/linksBed \
  --slave %{_bindir}/mapBed mapBed /opt/bioit/%{name}/%{version}/bin/mapBed \
  --slave %{_bindir}/maskFastaFromBed maskFastaFromBed /opt/bioit/%{name}/%{version}/bin/maskFastaFromBed \
  --slave %{_bindir}/mergeBed mergeBed /opt/bioit/%{name}/%{version}/bin/mergeBed \
  --slave %{_bindir}/multiBamCov multiBamCov /opt/bioit/%{name}/%{version}/bin/multiBamCov \
  --slave %{_bindir}/multiIntersectBed multiIntersectBed /opt/bioit/%{name}/%{version}/bin/multiIntersectBed \
  --slave %{_bindir}/nucBed nucBed /opt/bioit/%{name}/%{version}/bin/nucBed \
  --slave %{_bindir}/pairToBed pairToBed /opt/bioit/%{name}/%{version}/bin/pairToBed \
  --slave %{_bindir}/pairToPair pairToPair /opt/bioit/%{name}/%{version}/bin/pairToPair \
  --slave %{_bindir}/randomBed randomBed /opt/bioit/%{name}/%{version}/bin/randomBed \
  --slave %{_bindir}/shiftBed shiftBed /opt/bioit/%{name}/%{version}/bin/shiftBed \
  --slave %{_bindir}/shuffleBed shuffleBed /opt/bioit/%{name}/%{version}/bin/shuffleBed \
  --slave %{_bindir}/slopBed slopBed /opt/bioit/%{name}/%{version}/bin/slopBed \
  --slave %{_bindir}/sortBed sortBed /opt/bioit/%{name}/%{version}/bin/sortBed \
  --slave %{_bindir}/subtractBed subtractBed /opt/bioit/%{name}/%{version}/bin/subtractBed \
  --slave %{_bindir}/tagBam tagBam /opt/bioit/%{name}/%{version}/bin/tagBam \
  --slave %{_bindir}/unionBedGraphs unionBedGraphs /opt/bioit/%{name}/%{version}/bin/unionBedGraphs \
  --slave %{_bindir}/windowBed windowBed /opt/bioit/%{name}/%{version}/bin/windowBed \
  --slave %{_bindir}/windowMaker windowMaker /opt/bioit/%{name}/%{version}/bin/windowMaker

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove bedtools /opt/bioit/%{name}/%{version}/bin/bedtools
fi


%files

%changelog
* Wed May 03 2023 Shane Sturrock <shane.sturrock@gmail.com> - 2.31.0-1
- Added new summary tool for basic sanity checks and quality control of
  interval files. Documentation
- Added support for gzipp'ed FASTA files to getfasta and nuc. Thanks to
  @brentp.
- Various typo and minor bug fixes from @38 and @jmarshall.

* Fri Jan 29 2021 Shane Sturrock <shane.sturrock@gmail.com> - 2.30.0-1
- Thanks to Hao Hou (github: @38), we have made substantial improvements in the
  speed associated with parsing input files and in printing results. It turns
  out that these tasks consume a large proportion of run time, especially as
  input files increase in size. These changes result in a 2-3X improvement in
  speed, depending on input types, options, etc.
- Thanks to John Marshall (github: @jmarshall), who improved the stability and
  cleanliness of the code used for random number generation. These changes also
  squash a bug that arises on Debian systems.
- John Marshall cleaned up some lingering data type problems in the slop tool.
- Thanks to @gringer for adding the -ignoreD option to the genomecov tool,
  which allows D CIGAR operations to be ignored when calculating coverage. This
  is useful for long-read technologies with high INDEL error rates.
- Added a fix for a bug that did not properly handle the splitting of intervals
  in BED12 records with one block.
- Thanks to John Marshall (github: @jmarshall), we have addressed numerical
  instability issues in the fisher tool.
- Thanks to Hao Hou (github: @38), reference genomes can be read as an
  environment variable (CRAM_REFERENCE) when using CRAM input files.
- Added a -rna option to the getfasta tool to allow support for RNA genomes.
- Thanks to Hao Hou (github: @38), we fixed input file format detection bugs
  arising in ZSH.
- Thanks to Josh Shapiro (github:@jashapiro) for clarifying a confusing
  inconsistency in the documentation for the coverage tool.
- Thanks to Hao Hou (github: @38), we suppressed unnecessary warnings when
  reading GZIPP'ed files.
- Thanks to Hao Hou (github: @38), we fixed an overflow bug in the shuffle
  tool.
- Thanks to Hao Hou (github: @38), we fixed a data type bug in the shift tool.
- Thanks to John Marshall (github: @jmarshall) and Hao Hou (github: @38), we
  have cleaned up the internal support for htslib.

* Fri Jan 24 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.29.2-1
- Fixed a bug (#803) that mistakenly removed a BAM/CRAM header line (sorting
  criteria).

* Fri Dec 13 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.29.1-1
- Fixed a bug that now allows blocked intersection to be counted based on
  unique base pairs of overlap. The resolution for issue 750 in version 2.29.0
  mistakenly allowed for fractional overlap to be counted based upon redundant
  overlap.
- Moved to Github Continuous Integration for automatic testing.
- Fixed a bug that injected erroneous quality values with BAM records had no
  valid quality values.
- Fixed a bug that destroyed backwards compatibility in the getfasta tool.
  Thanks to Torsten Seeman for reporting this.
- Fixed a corner case bug in the reldist tool.
- Fixed a bug in the bedtobam tool that caused the last character in read names
  to be removed.
- Fixed a bug causing a segfault in the jaccard tool.
- Fixed a bug causing a corner case issue in the way coordinates are reported
  in the flank tool.

* Fri Sep 13 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.29.0-1
- Added a new -C option to the intersect tool that separately reports the count
  of intersections observed for each database (-b) file given. Formerly, the -c
  option reported to sum of all intersections observed across all database 
  files.
- Fixed an important bug in intersect that prevented some split reads from
  being counted properly with using the -split option with the -f option.
- Fixed a bug in shuffle such that shuffled regions should have the same strand
  as the chose -incl region.
- Added a new -L option to L`imit the output of the `complement tool to solely
  the chromosomes that are represented in the -i file.
- Fixed a regression in the multicov tool introduced in 2.28 that caused
  incorrect counts.
- Added support for multi-mapping reads in the bamtofastq tool.
- Fixed a bug that prevented the “window” tool from properly adding interval
  “slop” to BAM records.
- Fixed a bug that caused the slop tool to not truncate an interval’s end
  coordinate when it overlapped the end of a chromosome.
- Added support for the “=” and “X” CIGAR operations to bamtobed.
- Various other minor bug fixes and improvements to documentation.

* Fri Mar 29 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.28.0-1
- Included support for htslib to enable CRAM support and long-term stability
  (Thanks to Hao Hou!)
- Included support for genomes with large chromosomes by moving to 64-bit
  integers throughout the code base. Thanks to Brent Pedersen and John
  Marshall!
- We now provide a statically-linked binary for LINUX (not OSX) systems (see
  "bedtools" link below).
- As a result of 1-3, tools are ~10% faster.
- Various minor bug fixes.

* Mon Dec 18 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.27.1-1
- Fixed a bug in the Makefile that caused a substantial penalty in performance.

* Thu Dec 07 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.27.0-1
- Fixed a big memory leak and algorithmic flaw in the split option. Thanks to
  Neil Kindlon!
- Resolved compilation errors on OSX High Sierra. Many thanks to @jonchang!
- Fixed a bug in the shift tool that caused some intervals to exceed the end of
  the chromosome. Thanks to @wlholtz
- Fixed major bug in groupby that prevented proper functionality.
- Speed improvements to the shuffle tool.
- Bug fixes to the p-value calculation in the fisher tool. Thanks to Brent
  Pedersen.
- Allow BED headers to start with chrom or chr
- Fixes to the "k-closest" functionality in the closest tool. Thanks to Neil
  Kindlon.
- Fixes to the output of the freqasc, freqdesc, distinct_sort_num and
  distinct_sort, and num_desc operations in the groupby tool. Thanks to @ghuls.
- Many minor bug fixes and compilation improvements from Luke Goodsell.
- Added the -fullHeader option to the maskfasta tool. Thanks to @ghuls.
- Many bug fixes and performance improvements from John Marshall.
- Fixed bug in the -N/-f behavior in subtract.
- Full support for .fai files as genome (-g) files.
- Many other minor bug fixes and functionality improvements.

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
