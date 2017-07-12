%define priority 3736
%define dir_exists() (if [ ! -d /opt/biology/%{name}/%{version} ]; then \
  echo "/opt/biology/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bbmap
Version:	37.36
Release:	1%{?dist}
Summary:	BBMap short read aligner, and other bioinformatic tools.
Group:		Applications/Engineering
License:	BSD
URL:		https://sourceforge.net/projects/bbmap/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
This package includes BBMap, a short read aligner, as well as various other
bioinformatic tools. It is written in pure Java, can run on any platform, and
has no dependencies other than Java being installed (compiled for Java 6 and
higher). All tools are efficient and multithreaded.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/bbmap.sh bbmap /opt/biology/%{name}/%{version}/bbmap.sh %{priority} \
   --slave %{_bindir}/addadapters.sh addadapters.sh /opt/biology/%{name}/%{version}/addadapters.sh \
   --slave %{_bindir}/a_sample_mt.sh a_sample_mt.sh /opt/biology/%{name}/%{version}/a_sample_mt.sh \
   --slave %{_bindir}/bbcountunique.sh bbcountunique.sh /opt/biology/%{name}/%{version}/bbcountunique.sh \
   --slave %{_bindir}/bbduk2.sh bbduk2.sh /opt/biology/%{name}/%{version}/bbduk2.sh \
   --slave %{_bindir}/bbduk.sh bbduk.sh /opt/biology/%{name}/%{version}/bbduk.sh \
   --slave %{_bindir}/bbest.sh bbest.sh /opt/biology/%{name}/%{version}/bbest.sh \
   --slave %{_bindir}/bbfakereads.sh bbfakereads.sh /opt/biology/%{name}/%{version}/bbfakereads.sh \
   --slave %{_bindir}/bbmapskimmer.sh bbmapskimmer.sh /opt/biology/%{name}/%{version}/bbmapskimmer.sh \
   --slave %{_bindir}/bbmask.sh bbmask.sh /opt/biology/%{name}/%{version}/bbmask.sh \
   --slave %{_bindir}/bbmerge-auto.sh bbmerge-auto.sh /opt/biology/%{name}/%{version}/bbmerge-auto.sh \
   --slave %{_bindir}/bbmergegapped.sh bbmergegapped.sh /opt/biology/%{name}/%{version}/bbmergegapped.sh \
   --slave %{_bindir}/bbmerge.sh bbmerge.sh /opt/biology/%{name}/%{version}/bbmerge.sh \
   --slave %{_bindir}/bbnorm.sh bbnorm.sh /opt/biology/%{name}/%{version}/bbnorm.sh \
   --slave %{_bindir}/bbrealign.sh bbrealign.sh /opt/biology/%{name}/%{version}/bbrealign.sh \
   --slave %{_bindir}/bbsketch.sh bbsketch.sh /opt/biology/%{name}/%{version}/bbsketch.sh \
   --slave %{_bindir}/bbsplitpairs.sh bbsplitpairs.sh /opt/biology/%{name}/%{version}/bbsplitpairs.sh \
   --slave %{_bindir}/bbsplit.sh bbsplit.sh /opt/biology/%{name}/%{version}/bbsplit.sh \
   --slave %{_bindir}/bbversion.sh bbversion.sh /opt/biology/%{name}/%{version}/bbversion.sh \
   --slave %{_bindir}/bbwrap.sh bbwrap.sh /opt/biology/%{name}/%{version}/bbwrap.sh \
   --slave %{_bindir}/calcmem.sh calcmem.sh /opt/biology/%{name}/%{version}/calcmem.sh \
   --slave %{_bindir}/calctruequality.sh calctruequality.sh /opt/biology/%{name}/%{version}/calctruequality.sh \
   --slave %{_bindir}/callpeaks.sh callpeaks.sh /opt/biology/%{name}/%{version}/callpeaks.sh \
   --slave %{_bindir}/callvariants2.sh callvariants2.sh /opt/biology/%{name}/%{version}/callvariants2.sh \
   --slave %{_bindir}/callvariants.sh callvariants.sh /opt/biology/%{name}/%{version}/callvariants.sh \
   --slave %{_bindir}/clumpify.sh clumpify.sh /opt/biology/%{name}/%{version}/clumpify.sh \
   --slave %{_bindir}/commonkmers.sh commonkmers.sh /opt/biology/%{name}/%{version}/commonkmers.sh \
   --slave %{_bindir}/comparesketch.sh comparesketch.sh /opt/biology/%{name}/%{version}/comparesketch.sh \
   --slave %{_bindir}/comparevcf.sh comparevcf.sh /opt/biology/%{name}/%{version}/comparevcf.sh \
   --slave %{_bindir}/consect.sh consect.sh /opt/biology/%{name}/%{version}/consect.sh \
   --slave %{_bindir}/countbarcodes.sh countbarcodes.sh /opt/biology/%{name}/%{version}/countbarcodes.sh \
   --slave %{_bindir}/countgc.sh countgc.sh /opt/biology/%{name}/%{version}/countgc.sh \
   --slave %{_bindir}/countsharedlines.sh countsharedlines.sh /opt/biology/%{name}/%{version}/countsharedlines.sh \
   --slave %{_bindir}/crossblock.sh crossblock.sh /opt/biology/%{name}/%{version}/crossblock.sh \
   --slave %{_bindir}/crosscontaminate.sh crosscontaminate.sh /opt/biology/%{name}/%{version}/crosscontaminate.sh \
   --slave %{_bindir}/cutprimers.sh cutprimers.sh /opt/biology/%{name}/%{version}/cutprimers.sh \
   --slave %{_bindir}/decontaminate.sh decontaminate.sh /opt/biology/%{name}/%{version}/decontaminate.sh \
   --slave %{_bindir}/dedupe2.sh dedupe2.sh /opt/biology/%{name}/%{version}/dedupe2.sh \
   --slave %{_bindir}/dedupebymapping.sh dedupebymapping.sh /opt/biology/%{name}/%{version}/dedupebymapping.sh \
   --slave %{_bindir}/dedupe.sh dedupe.sh /opt/biology/%{name}/%{version}/dedupe.sh \
   --slave %{_bindir}/demuxbyname.sh demuxbyname.sh /opt/biology/%{name}/%{version}/demuxbyname.sh \
   --slave %{_bindir}/ecc.sh ecc.sh /opt/biology/%{name}/%{version}/ecc.sh \
   --slave %{_bindir}/estherfilter.sh estherfilter.sh /opt/biology/%{name}/%{version}/estherfilter.sh \
   --slave %{_bindir}/filterassemblysummary.sh filterassemblysummary.sh /opt/biology/%{name}/%{version}/filterassemblysummary.sh \
   --slave %{_bindir}/filterbarcodes.sh filterbarcodes.sh /opt/biology/%{name}/%{version}/filterbarcodes.sh \
   --slave %{_bindir}/filterbycoverage.sh filterbycoverage.sh /opt/biology/%{name}/%{version}/filterbycoverage.sh \
   --slave %{_bindir}/filterbyname.sh filterbyname.sh /opt/biology/%{name}/%{version}/filterbyname.sh \
   --slave %{_bindir}/filterbysequence.sh filterbysequence.sh /opt/biology/%{name}/%{version}/filterbysequence.sh \
   --slave %{_bindir}/filterbytaxa.sh filterbytaxa.sh /opt/biology/%{name}/%{version}/filterbytaxa.sh \
   --slave %{_bindir}/filterbytile.sh filterbytile.sh /opt/biology/%{name}/%{version}/filterbytile.sh \
   --slave %{_bindir}/filterlines.sh filterlines.sh /opt/biology/%{name}/%{version}/filterlines.sh \
   --slave %{_bindir}/filtersubs.sh filtersubs.sh /opt/biology/%{name}/%{version}/filtersubs.sh \
   --slave %{_bindir}/filtervcf.sh filtervcf.sh /opt/biology/%{name}/%{version}/filtervcf.sh \
   --slave %{_bindir}/fuse.sh fuse.sh /opt/biology/%{name}/%{version}/fuse.sh \
   --slave %{_bindir}/getreads.sh getreads.sh /opt/biology/%{name}/%{version}/getreads.sh \
   --slave %{_bindir}/gi2ancestors.sh gi2ancestors.sh /opt/biology/%{name}/%{version}/gi2ancestors.sh \
   --slave %{_bindir}/gi2taxid.sh gi2taxid.sh /opt/biology/%{name}/%{version}/gi2taxid.sh \
   --slave %{_bindir}/gitable.sh gitable.sh /opt/biology/%{name}/%{version}/gitable.sh \
   --slave %{_bindir}/grademerge.sh grademerge.sh /opt/biology/%{name}/%{version}/grademerge.sh \
   --slave %{_bindir}/gradesam.sh gradesam.sh /opt/biology/%{name}/%{version}/gradesam.sh \
   --slave %{_bindir}/idmatrix.sh idmatrix.sh /opt/biology/%{name}/%{version}/idmatrix.sh \
   --slave %{_bindir}/idtree.sh idtree.sh /opt/biology/%{name}/%{version}/idtree.sh \
   --slave %{_bindir}/kcompress.sh kcompress.sh /opt/biology/%{name}/%{version}/kcompress.sh \
   --slave %{_bindir}/khist.sh khist.sh /opt/biology/%{name}/%{version}/khist.sh \
   --slave %{_bindir}/kmercountexact.sh kmercountexact.sh /opt/biology/%{name}/%{version}/kmercountexact.sh \
   --slave %{_bindir}/kmercountmulti.sh kmercountmulti.sh /opt/biology/%{name}/%{version}/kmercountmulti.sh \
   --slave %{_bindir}/kmercoverage.sh kmercoverage.sh /opt/biology/%{name}/%{version}/kmercoverage.sh \
   --slave %{_bindir}/loadreads.sh loadreads.sh /opt/biology/%{name}/%{version}/loadreads.sh \
   --slave %{_bindir}/loglog.sh loglog.sh /opt/biology/%{name}/%{version}/loglog.sh \
   --slave %{_bindir}/makechimeras.sh makechimeras.sh /opt/biology/%{name}/%{version}/makechimeras.sh \
   --slave %{_bindir}/mapPacBio.sh mapPacBio.sh /opt/biology/%{name}/%{version}/mapPacBio.sh \
   --slave %{_bindir}/matrixtocolumns.sh matrixtocolumns.sh /opt/biology/%{name}/%{version}/matrixtocolumns.sh \
   --slave %{_bindir}/mergebarcodes.sh mergebarcodes.sh /opt/biology/%{name}/%{version}/mergebarcodes.sh \
   --slave %{_bindir}/mergeOTUs.sh mergeOTUs.sh /opt/biology/%{name}/%{version}/mergeOTUs.sh \
   --slave %{_bindir}/mergesam.sh mergesam.sh /opt/biology/%{name}/%{version}/mergesam.sh \
   --slave %{_bindir}/msa.sh msa.sh /opt/biology/%{name}/%{version}/msa.sh \
   --slave %{_bindir}/mutate.sh mutate.sh /opt/biology/%{name}/%{version}/mutate.sh \
   --slave %{_bindir}/muxbyname.sh muxbyname.sh /opt/biology/%{name}/%{version}/muxbyname.sh \
   --slave %{_bindir}/partition.sh partition.sh /opt/biology/%{name}/%{version}/partition.sh \
   --slave %{_bindir}/phylip2fasta.sh phylip2fasta.sh /opt/biology/%{name}/%{version}/phylip2fasta.sh \
   --slave %{_bindir}/pileup.sh pileup.sh /opt/biology/%{name}/%{version}/pileup.sh \
   --slave %{_bindir}/plotgc.sh plotgc.sh /opt/biology/%{name}/%{version}/plotgc.sh \
   --slave %{_bindir}/postfilter.sh postfilter.sh /opt/biology/%{name}/%{version}/postfilter.sh \
   --slave %{_bindir}/printtime.sh printtime.sh /opt/biology/%{name}/%{version}/printtime.sh \
   --slave %{_bindir}/processfrag.sh processfrag.sh /opt/biology/%{name}/%{version}/processfrag.sh \
   --slave %{_bindir}/processspeed.sh processspeed.sh /opt/biology/%{name}/%{version}/processspeed.sh \
   --slave %{_bindir}/randomreads.sh randomreads.sh /opt/biology/%{name}/%{version}/randomreads.sh \
   --slave %{_bindir}/readlength.sh readlength.sh /opt/biology/%{name}/%{version}/readlength.sh \
   --slave %{_bindir}/reducesilva.sh reducesilva.sh /opt/biology/%{name}/%{version}/reducesilva.sh \
   --slave %{_bindir}/reformat.sh reformat.sh /opt/biology/%{name}/%{version}/reformat.sh \
   --slave %{_bindir}/removebadbarcodes.sh removebadbarcodes.sh /opt/biology/%{name}/%{version}/removebadbarcodes.sh \
   --slave %{_bindir}/removesmartbell.sh removesmartbell.sh /opt/biology/%{name}/%{version}/removesmartbell.sh \
   --slave %{_bindir}/renameimg.sh renameimg.sh /opt/biology/%{name}/%{version}/renameimg.sh \
   --slave %{_bindir}/rename.sh rename.sh /opt/biology/%{name}/%{version}/rename.sh \
   --slave %{_bindir}/repair.sh repair.sh /opt/biology/%{name}/%{version}/repair.sh \
   --slave %{_bindir}/rename.sh rename.sh /opt/biology/%{name}/%{version}/rename.sh \
   --slave %{_bindir}/replaceheaders.sh replaceheaders.sh /opt/biology/%{name}/%{version}/replaceheaders.sh \
   --slave %{_bindir}/rqcfilter.sh rqcfilter.sh /opt/biology/%{name}/%{version}/rqcfilter.sh \
   --slave %{_bindir}/samtoroc.sh samtoroc.sh /opt/biology/%{name}/%{version}/samtoroc.sh \
   --slave %{_bindir}/seal.sh seal.sh /opt/biology/%{name}/%{version}/seal.sh \
   --slave %{_bindir}/sendsketch.sh sendsketch.sh /opt/biology/%{name}/%{version}/sendsketch.sh \
   --slave %{_bindir}/shred.sh shred.sh /opt/biology/%{name}/%{version}/shred.sh \
   --slave %{_bindir}/shrinkaccession.sh shrinkaccession.sh /opt/biology/%{name}/%{version}/shrinkaccession.sh \
   --slave %{_bindir}/shuffle.sh shuffle.sh /opt/biology/%{name}/%{version}/shuffle.sh \
   --slave %{_bindir}/sketchblacklist.sh sketchblacklist.sh /opt/biology/%{name}/%{version}/sketchblacklist.sh \
   --slave %{_bindir}/sketch.sh sketch.sh /opt/biology/%{name}/%{version}/sketch.sh \
   --slave %{_bindir}/sortbyname.sh sortbyname.sh /opt/biology/%{name}/%{version}/sortbyname.sh \
   --slave %{_bindir}/splitbytaxa.sh splitbytaxa.sh /opt/biology/%{name}/%{version}/splitbytaxa.sh \
   --slave %{_bindir}/splitnextera.sh splitnextera.sh /opt/biology/%{name}/%{version}/splitnextera.sh \
   --slave %{_bindir}/splitsam6way.sh splitsam6way.sh /opt/biology/%{name}/%{version}/splitsam6way.sh \
   --slave %{_bindir}/splitsam.sh splitsam.sh /opt/biology/%{name}/%{version}/splitsam.sh \
   --slave %{_bindir}/stats.sh stats.sh /opt/biology/%{name}/%{version}/stats.sh \
   --slave %{_bindir}/statswrapper.sh statswrapper.sh /opt/biology/%{name}/%{version}/statswrapper.sh \
   --slave %{_bindir}/streamsam.sh streamsam.sh /opt/biology/%{name}/%{version}/streamsam.sh \
   --slave %{_bindir}/summarizecrossblock.sh summarizecrossblock.sh /opt/biology/%{name}/%{version}/summarizecrossblock.sh \
   --slave %{_bindir}/summarizemerge.sh summarizemerge.sh /opt/biology/%{name}/%{version}/summarizemerge.sh \
   --slave %{_bindir}/summarizequast.sh summarizequast.sh /opt/biology/%{name}/%{version}/summarizequast.sh \
   --slave %{_bindir}/summarizescafstats.sh summarizescafstats.sh /opt/biology/%{name}/%{version}/summarizescafstats.sh \
   --slave %{_bindir}/summarizeseal.sh summarizeseal.sh /opt/biology/%{name}/%{version}/summarizeseal.sh \
   --slave %{_bindir}/synthmda.sh synthmda.sh /opt/biology/%{name}/%{version}/synthmda.sh \
   --slave %{_bindir}/tadpipe.sh tadpipe.sh /opt/biology/%{name}/%{version}/tadpipe.sh \
   --slave %{_bindir}/tadpole.sh tadpole.sh /opt/biology/%{name}/%{version}/tadpole.sh \
   --slave %{_bindir}/tadwrapper.sh tadwrapper.sh /opt/biology/%{name}/%{version}/tadwrapper.sh \
   --slave %{_bindir}/taxonomy.sh taxonomy.sh /opt/biology/%{name}/%{version}/taxonomy.sh \
   --slave %{_bindir}/taxserver.sh taxserver.sh /opt/biology/%{name}/%{version}/taxserver.sh \
   --slave %{_bindir}/taxtree.sh taxtree.sh /opt/biology/%{name}/%{version}/taxtree.sh \
   --slave %{_bindir}/testformat.sh testformat.sh /opt/biology/%{name}/%{version}/testformat.sh \
   --slave %{_bindir}/textfile.sh textfile.sh /opt/biology/%{name}/%{version}/textfile.sh \
   --slave %{_bindir}/translate6frames.sh translate6frames.sh /opt/biology/%{name}/%{version}/translate6frames.sh

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bbmap /opt/biology/%{name}/%{version}/bbmap.sh
fi

%files

%changelog
* Thu Jul 13 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.36-1
- Clarified TaxServer error message for incompatible settings.
- Added deleteinput flag for Reformat and Clumpify.
- Updated BBSketchGuide.

* Tue Jul 04 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.33-1
- Added parsing for comment.
- Clumpify with groups>1 now works with paired fasta files, though 
  interleaved fasta files need interleaved to be explicitly set.
- Wrote MultiBitSet and improved AbstractBitSet.
- Refactored comparison formating into DisplayParams.
- TaxServer no longer dies when receiving an unexpected parameter.
- TaxServer no longer terminates when failing to kill an old instance.
- SendSketch now passes printRefDivisor and so forth.
- Added Unique, uContam, and noHit Sketch results columns.
- Added taxonomy-based Sketch results coloring.
- Added TaxTree.extendedToLevel for reverse lookup.
- Added counters for tracking TaxServer statistics.
- Improved server help messages; added Sketch usage info.
- Added Tadpole extra flag and clarified the documentation.

* Tue Jun 27 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.31-1
- Wrote SplitSam6Way.
- Removed obsolete tryAllExtensions option from TextFile/ByteFile.
- Added histbefore flag to BBDuk, and option to generate histograms after
  processing.
- Added fname metadata to Sketch header.
- Changed Sketch results query formatting to include more metadata.
