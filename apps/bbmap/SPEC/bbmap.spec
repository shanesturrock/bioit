%define priority 3741
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bbmap
Version:	37.41
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
   --install %{_bindir}/bbmap.sh bbmap /opt/bioit/%{name}/%{version}/bbmap.sh %{priority} \
   --slave %{_bindir}/addadapters.sh addadapters.sh /opt/bioit/%{name}/%{version}/addadapters.sh \
   --slave %{_bindir}/a_sample_mt.sh a_sample_mt.sh /opt/bioit/%{name}/%{version}/a_sample_mt.sh \
   --slave %{_bindir}/bbcountunique.sh bbcountunique.sh /opt/bioit/%{name}/%{version}/bbcountunique.sh \
   --slave %{_bindir}/bbduk2.sh bbduk2.sh /opt/bioit/%{name}/%{version}/bbduk2.sh \
   --slave %{_bindir}/bbduk.sh bbduk.sh /opt/bioit/%{name}/%{version}/bbduk.sh \
   --slave %{_bindir}/bbest.sh bbest.sh /opt/bioit/%{name}/%{version}/bbest.sh \
   --slave %{_bindir}/bbfakereads.sh bbfakereads.sh /opt/bioit/%{name}/%{version}/bbfakereads.sh \
   --slave %{_bindir}/bbmapskimmer.sh bbmapskimmer.sh /opt/bioit/%{name}/%{version}/bbmapskimmer.sh \
   --slave %{_bindir}/bbmask.sh bbmask.sh /opt/bioit/%{name}/%{version}/bbmask.sh \
   --slave %{_bindir}/bbmerge-auto.sh bbmerge-auto.sh /opt/bioit/%{name}/%{version}/bbmerge-auto.sh \
   --slave %{_bindir}/bbmergegapped.sh bbmergegapped.sh /opt/bioit/%{name}/%{version}/bbmergegapped.sh \
   --slave %{_bindir}/bbmerge.sh bbmerge.sh /opt/bioit/%{name}/%{version}/bbmerge.sh \
   --slave %{_bindir}/bbnorm.sh bbnorm.sh /opt/bioit/%{name}/%{version}/bbnorm.sh \
   --slave %{_bindir}/bbrealign.sh bbrealign.sh /opt/bioit/%{name}/%{version}/bbrealign.sh \
   --slave %{_bindir}/bbsketch.sh bbsketch.sh /opt/bioit/%{name}/%{version}/bbsketch.sh \
   --slave %{_bindir}/bbsplitpairs.sh bbsplitpairs.sh /opt/bioit/%{name}/%{version}/bbsplitpairs.sh \
   --slave %{_bindir}/bbsplit.sh bbsplit.sh /opt/bioit/%{name}/%{version}/bbsplit.sh \
   --slave %{_bindir}/bbversion.sh bbversion.sh /opt/bioit/%{name}/%{version}/bbversion.sh \
   --slave %{_bindir}/bbwrap.sh bbwrap.sh /opt/bioit/%{name}/%{version}/bbwrap.sh \
   --slave %{_bindir}/calcmem.sh calcmem.sh /opt/bioit/%{name}/%{version}/calcmem.sh \
   --slave %{_bindir}/calctruequality.sh calctruequality.sh /opt/bioit/%{name}/%{version}/calctruequality.sh \
   --slave %{_bindir}/callpeaks.sh callpeaks.sh /opt/bioit/%{name}/%{version}/callpeaks.sh \
   --slave %{_bindir}/callvariants2.sh callvariants2.sh /opt/bioit/%{name}/%{version}/callvariants2.sh \
   --slave %{_bindir}/callvariants.sh callvariants.sh /opt/bioit/%{name}/%{version}/callvariants.sh \
   --slave %{_bindir}/clumpify.sh clumpify.sh /opt/bioit/%{name}/%{version}/clumpify.sh \
   --slave %{_bindir}/commonkmers.sh commonkmers.sh /opt/bioit/%{name}/%{version}/commonkmers.sh \
   --slave %{_bindir}/comparesketch.sh comparesketch.sh /opt/bioit/%{name}/%{version}/comparesketch.sh \
   --slave %{_bindir}/comparevcf.sh comparevcf.sh /opt/bioit/%{name}/%{version}/comparevcf.sh \
   --slave %{_bindir}/consect.sh consect.sh /opt/bioit/%{name}/%{version}/consect.sh \
   --slave %{_bindir}/countbarcodes.sh countbarcodes.sh /opt/bioit/%{name}/%{version}/countbarcodes.sh \
   --slave %{_bindir}/countgc.sh countgc.sh /opt/bioit/%{name}/%{version}/countgc.sh \
   --slave %{_bindir}/countsharedlines.sh countsharedlines.sh /opt/bioit/%{name}/%{version}/countsharedlines.sh \
   --slave %{_bindir}/crossblock.sh crossblock.sh /opt/bioit/%{name}/%{version}/crossblock.sh \
   --slave %{_bindir}/crosscontaminate.sh crosscontaminate.sh /opt/bioit/%{name}/%{version}/crosscontaminate.sh \
   --slave %{_bindir}/cutprimers.sh cutprimers.sh /opt/bioit/%{name}/%{version}/cutprimers.sh \
   --slave %{_bindir}/decontaminate.sh decontaminate.sh /opt/bioit/%{name}/%{version}/decontaminate.sh \
   --slave %{_bindir}/dedupe2.sh dedupe2.sh /opt/bioit/%{name}/%{version}/dedupe2.sh \
   --slave %{_bindir}/dedupebymapping.sh dedupebymapping.sh /opt/bioit/%{name}/%{version}/dedupebymapping.sh \
   --slave %{_bindir}/dedupe.sh dedupe.sh /opt/bioit/%{name}/%{version}/dedupe.sh \
   --slave %{_bindir}/demuxbyname.sh demuxbyname.sh /opt/bioit/%{name}/%{version}/demuxbyname.sh \
   --slave %{_bindir}/ecc.sh ecc.sh /opt/bioit/%{name}/%{version}/ecc.sh \
   --slave %{_bindir}/estherfilter.sh estherfilter.sh /opt/bioit/%{name}/%{version}/estherfilter.sh \
   --slave %{_bindir}/filterassemblysummary.sh filterassemblysummary.sh /opt/bioit/%{name}/%{version}/filterassemblysummary.sh \
   --slave %{_bindir}/filterbarcodes.sh filterbarcodes.sh /opt/bioit/%{name}/%{version}/filterbarcodes.sh \
   --slave %{_bindir}/filterbycoverage.sh filterbycoverage.sh /opt/bioit/%{name}/%{version}/filterbycoverage.sh \
   --slave %{_bindir}/filterbyname.sh filterbyname.sh /opt/bioit/%{name}/%{version}/filterbyname.sh \
   --slave %{_bindir}/filterbysequence.sh filterbysequence.sh /opt/bioit/%{name}/%{version}/filterbysequence.sh \
   --slave %{_bindir}/filterbytaxa.sh filterbytaxa.sh /opt/bioit/%{name}/%{version}/filterbytaxa.sh \
   --slave %{_bindir}/filterbytile.sh filterbytile.sh /opt/bioit/%{name}/%{version}/filterbytile.sh \
   --slave %{_bindir}/filterlines.sh filterlines.sh /opt/bioit/%{name}/%{version}/filterlines.sh \
   --slave %{_bindir}/filtersubs.sh filtersubs.sh /opt/bioit/%{name}/%{version}/filtersubs.sh \
   --slave %{_bindir}/filtervcf.sh filtervcf.sh /opt/bioit/%{name}/%{version}/filtervcf.sh \
   --slave %{_bindir}/fuse.sh fuse.sh /opt/bioit/%{name}/%{version}/fuse.sh \
   --slave %{_bindir}/getreads.sh getreads.sh /opt/bioit/%{name}/%{version}/getreads.sh \
   --slave %{_bindir}/gi2ancestors.sh gi2ancestors.sh /opt/bioit/%{name}/%{version}/gi2ancestors.sh \
   --slave %{_bindir}/gi2taxid.sh gi2taxid.sh /opt/bioit/%{name}/%{version}/gi2taxid.sh \
   --slave %{_bindir}/gitable.sh gitable.sh /opt/bioit/%{name}/%{version}/gitable.sh \
   --slave %{_bindir}/grademerge.sh grademerge.sh /opt/bioit/%{name}/%{version}/grademerge.sh \
   --slave %{_bindir}/gradesam.sh gradesam.sh /opt/bioit/%{name}/%{version}/gradesam.sh \
   --slave %{_bindir}/idmatrix.sh idmatrix.sh /opt/bioit/%{name}/%{version}/idmatrix.sh \
   --slave %{_bindir}/idtree.sh idtree.sh /opt/bioit/%{name}/%{version}/idtree.sh \
   --slave %{_bindir}/kcompress.sh kcompress.sh /opt/bioit/%{name}/%{version}/kcompress.sh \
   --slave %{_bindir}/khist.sh khist.sh /opt/bioit/%{name}/%{version}/khist.sh \
   --slave %{_bindir}/kmercountexact.sh kmercountexact.sh /opt/bioit/%{name}/%{version}/kmercountexact.sh \
   --slave %{_bindir}/kmercountmulti.sh kmercountmulti.sh /opt/bioit/%{name}/%{version}/kmercountmulti.sh \
   --slave %{_bindir}/kmercoverage.sh kmercoverage.sh /opt/bioit/%{name}/%{version}/kmercoverage.sh \
   --slave %{_bindir}/loadreads.sh loadreads.sh /opt/bioit/%{name}/%{version}/loadreads.sh \
   --slave %{_bindir}/loglog.sh loglog.sh /opt/bioit/%{name}/%{version}/loglog.sh \
   --slave %{_bindir}/makechimeras.sh makechimeras.sh /opt/bioit/%{name}/%{version}/makechimeras.sh \
   --slave %{_bindir}/mapPacBio.sh mapPacBio.sh /opt/bioit/%{name}/%{version}/mapPacBio.sh \
   --slave %{_bindir}/matrixtocolumns.sh matrixtocolumns.sh /opt/bioit/%{name}/%{version}/matrixtocolumns.sh \
   --slave %{_bindir}/mergebarcodes.sh mergebarcodes.sh /opt/bioit/%{name}/%{version}/mergebarcodes.sh \
   --slave %{_bindir}/mergeOTUs.sh mergeOTUs.sh /opt/bioit/%{name}/%{version}/mergeOTUs.sh \
   --slave %{_bindir}/mergesam.sh mergesam.sh /opt/bioit/%{name}/%{version}/mergesam.sh \
   --slave %{_bindir}/msa.sh msa.sh /opt/bioit/%{name}/%{version}/msa.sh \
   --slave %{_bindir}/mutate.sh mutate.sh /opt/bioit/%{name}/%{version}/mutate.sh \
   --slave %{_bindir}/muxbyname.sh muxbyname.sh /opt/bioit/%{name}/%{version}/muxbyname.sh \
   --slave %{_bindir}/partition.sh partition.sh /opt/bioit/%{name}/%{version}/partition.sh \
   --slave %{_bindir}/phylip2fasta.sh phylip2fasta.sh /opt/bioit/%{name}/%{version}/phylip2fasta.sh \
   --slave %{_bindir}/pileup.sh pileup.sh /opt/bioit/%{name}/%{version}/pileup.sh \
   --slave %{_bindir}/plotgc.sh plotgc.sh /opt/bioit/%{name}/%{version}/plotgc.sh \
   --slave %{_bindir}/postfilter.sh postfilter.sh /opt/bioit/%{name}/%{version}/postfilter.sh \
   --slave %{_bindir}/printtime.sh printtime.sh /opt/bioit/%{name}/%{version}/printtime.sh \
   --slave %{_bindir}/processfrag.sh processfrag.sh /opt/bioit/%{name}/%{version}/processfrag.sh \
   --slave %{_bindir}/processspeed.sh processspeed.sh /opt/bioit/%{name}/%{version}/processspeed.sh \
   --slave %{_bindir}/randomreads.sh randomreads.sh /opt/bioit/%{name}/%{version}/randomreads.sh \
   --slave %{_bindir}/readlength.sh readlength.sh /opt/bioit/%{name}/%{version}/readlength.sh \
   --slave %{_bindir}/reducesilva.sh reducesilva.sh /opt/bioit/%{name}/%{version}/reducesilva.sh \
   --slave %{_bindir}/reformat.sh reformat.sh /opt/bioit/%{name}/%{version}/reformat.sh \
   --slave %{_bindir}/removebadbarcodes.sh removebadbarcodes.sh /opt/bioit/%{name}/%{version}/removebadbarcodes.sh \
   --slave %{_bindir}/removesmartbell.sh removesmartbell.sh /opt/bioit/%{name}/%{version}/removesmartbell.sh \
   --slave %{_bindir}/renameimg.sh renameimg.sh /opt/bioit/%{name}/%{version}/renameimg.sh \
   --slave %{_bindir}/rename.sh rename.sh /opt/bioit/%{name}/%{version}/rename.sh \
   --slave %{_bindir}/repair.sh repair.sh /opt/bioit/%{name}/%{version}/repair.sh \
   --slave %{_bindir}/rename.sh rename.sh /opt/bioit/%{name}/%{version}/rename.sh \
   --slave %{_bindir}/replaceheaders.sh replaceheaders.sh /opt/bioit/%{name}/%{version}/replaceheaders.sh \
   --slave %{_bindir}/rqcfilter.sh rqcfilter.sh /opt/bioit/%{name}/%{version}/rqcfilter.sh \
   --slave %{_bindir}/samtoroc.sh samtoroc.sh /opt/bioit/%{name}/%{version}/samtoroc.sh \
   --slave %{_bindir}/seal.sh seal.sh /opt/bioit/%{name}/%{version}/seal.sh \
   --slave %{_bindir}/sendsketch.sh sendsketch.sh /opt/bioit/%{name}/%{version}/sendsketch.sh \
   --slave %{_bindir}/shred.sh shred.sh /opt/bioit/%{name}/%{version}/shred.sh \
   --slave %{_bindir}/shrinkaccession.sh shrinkaccession.sh /opt/bioit/%{name}/%{version}/shrinkaccession.sh \
   --slave %{_bindir}/shuffle.sh shuffle.sh /opt/bioit/%{name}/%{version}/shuffle.sh \
   --slave %{_bindir}/sketchblacklist.sh sketchblacklist.sh /opt/bioit/%{name}/%{version}/sketchblacklist.sh \
   --slave %{_bindir}/sketch.sh sketch.sh /opt/bioit/%{name}/%{version}/sketch.sh \
   --slave %{_bindir}/sortbyname.sh sortbyname.sh /opt/bioit/%{name}/%{version}/sortbyname.sh \
   --slave %{_bindir}/splitbytaxa.sh splitbytaxa.sh /opt/bioit/%{name}/%{version}/splitbytaxa.sh \
   --slave %{_bindir}/splitnextera.sh splitnextera.sh /opt/bioit/%{name}/%{version}/splitnextera.sh \
   --slave %{_bindir}/splitsam6way.sh splitsam6way.sh /opt/bioit/%{name}/%{version}/splitsam6way.sh \
   --slave %{_bindir}/splitsam.sh splitsam.sh /opt/bioit/%{name}/%{version}/splitsam.sh \
   --slave %{_bindir}/stats.sh stats.sh /opt/bioit/%{name}/%{version}/stats.sh \
   --slave %{_bindir}/statswrapper.sh statswrapper.sh /opt/bioit/%{name}/%{version}/statswrapper.sh \
   --slave %{_bindir}/streamsam.sh streamsam.sh /opt/bioit/%{name}/%{version}/streamsam.sh \
   --slave %{_bindir}/summarizecrossblock.sh summarizecrossblock.sh /opt/bioit/%{name}/%{version}/summarizecrossblock.sh \
   --slave %{_bindir}/summarizemerge.sh summarizemerge.sh /opt/bioit/%{name}/%{version}/summarizemerge.sh \
   --slave %{_bindir}/summarizequast.sh summarizequast.sh /opt/bioit/%{name}/%{version}/summarizequast.sh \
   --slave %{_bindir}/summarizescafstats.sh summarizescafstats.sh /opt/bioit/%{name}/%{version}/summarizescafstats.sh \
   --slave %{_bindir}/summarizeseal.sh summarizeseal.sh /opt/bioit/%{name}/%{version}/summarizeseal.sh \
   --slave %{_bindir}/synthmda.sh synthmda.sh /opt/bioit/%{name}/%{version}/synthmda.sh \
   --slave %{_bindir}/tadpipe.sh tadpipe.sh /opt/bioit/%{name}/%{version}/tadpipe.sh \
   --slave %{_bindir}/tadpole.sh tadpole.sh /opt/bioit/%{name}/%{version}/tadpole.sh \
   --slave %{_bindir}/tadwrapper.sh tadwrapper.sh /opt/bioit/%{name}/%{version}/tadwrapper.sh \
   --slave %{_bindir}/taxonomy.sh taxonomy.sh /opt/bioit/%{name}/%{version}/taxonomy.sh \
   --slave %{_bindir}/taxserver.sh taxserver.sh /opt/bioit/%{name}/%{version}/taxserver.sh \
   --slave %{_bindir}/taxtree.sh taxtree.sh /opt/bioit/%{name}/%{version}/taxtree.sh \
   --slave %{_bindir}/testformat.sh testformat.sh /opt/bioit/%{name}/%{version}/testformat.sh \
   --slave %{_bindir}/textfile.sh textfile.sh /opt/bioit/%{name}/%{version}/textfile.sh \
   --slave %{_bindir}/translate6frames.sh translate6frames.sh /opt/bioit/%{name}/%{version}/translate6frames.sh

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bbmap /opt/bioit/%{name}/%{version}/bbmap.sh
fi

%files

%changelog
* Tue Aug 08 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.41-1
- CompareSketch now allows first parameter to be a file name without in=.
- Wrote LongHashMap and LongHeapMap.
- Refactored SketchHeap to support LongHashMap when minkeycount>1.
- SketchHeap can now be temporarily longer than the desired sketch length when
  min keycount>1.
- Added usage query tracking to TaxServer.
- Added correct sketch blacklists to public distribution.
- Fixed incorrect insert size with renamebyinsert flag in RandomReads when
  reads are longer than insert size.
- RQCFilter now resets Sketch statics prior to subsequent SendSketch runs.
- SketchObject minkKeyCount moved to DisplayParams.
- SketchObject minCount field replaced.
- DisplayParams.minCount renamed minHits.
- BlacklistMaker.minCount renamed to MinTaxCount.
- RQCFilter now uses minkeycount=t for Silva.
- Changed SketchObject.size to targetSketchSize.
- TaxServer now makes a new SketchTool as needed when minKeyCount is different
  in local mode.
- Made some improvements to assemblyPipeline.sh.
- Fixed a tiny bug in parsing Sketch single kmer lengths of under 31.

* Fri Aug 04 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.38-1
- Fixed a read orientation bug in CalcTrueQuality when using a VCF file.
- Simplified some calls to short and long match string conversion.
- Added a variant-calling script to /pipelines.
- Fixed a null pointer exception in Sketch when using sam files.
- Investigated recalibration of R2.  Turns out the graph just looks odd because
  of low-quality unmapped reads.
- BBDuk can now accept ref=phix or adapters or artifacts, and automatically
  locates the file in /resources.
- Read identity calculation was crashing with fixvariants (from a VCF file).
- Removed bbduk2.sh as deprecated; only BBDuk is maintained.
- Adjusted Sketch hash function; cycleMask is now a constant.
- Made Sketch hashing variables private.
- Made Sketch hashCycles variable; speeds up shorter kmer lengths and makes k2
  codes compatible with k codes of same length.
- SortByName now uses compression level 2 for temp files.
- RenameImg now also reports the number of files, sequences, bases, and TaxIDs
  used.
- IMG naming is now in the old NCBI style, e.g. tid|1234|img|56789
- IMG header parsing methods and lookup table moved from TaxServer and
  ImgRecord2 to TaxTree.
- IMG header parsing is now automatic.
- Updated some descriptions in commonMicrobes filter directory.
- RQCFilter now by default queries nt, RefSeq, and Silva when Sketching.
- Wrote TestFilesystem and testfilesystem.sh to monitor filesystem performance.
- SendSketch now automatically sets k and k2 for nt, silva, and refseq.
- Changed RefSeq and nt sketch servers and scripts to k=31,24 (needs restart).
- Modified KmerCount7MTA increment routine slightly; it can now store hashed
  kmers .
- gi2taxid now runs in silva mode without requiring a gi or accession file.
- Altered BlacklistMaker to fix an issue of redundant hash codes.
- Fixed DisplayParams clone method.
- Fixed order of parsing imghq and setting the default img file.
- Fixed a bug in taxa coloring using parent instead of current node.
- Added dark purple to Colors.
- Taxa coloring now underlines records with the same color but different taxa
  compared to above.
- Updated SketchGuide to explain underlining.
- Added a second genome repeat content estimation method.
- Genome repeat content now considers one copy of a repeat to be non-repeat.
  For example, a genome with 1% duplicated would be considered 1% repeat
  instead of 2%.
- Added pipelines/assemblyPipeline.sh.
- Increased maximum samtools compression threads to 64.
- Clarified descriptions of outm and BBDuk kmer-matching modes.
- Revised Reformat trimrname handling to include all whitespace, and clarified
  description to include bam files.
- Restarted RefSeq and nt servers with k=31,24.
- CallVariants and FilterVCF can now enable/disable SNPs, insertions,
  deletions.
- ReadStats histogram lengths can now be adjusted with the maxhistlen flag.

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
