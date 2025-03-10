%define priority 3901
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bbmap
Version:	39.01
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
   --slave %{_bindir}/addssu.sh addssu.sh /opt/bioit/%{name}/%{version}/addssu.sh \
   --slave %{_bindir}/adjusthomopolymers.sh adjusthomopolymers.sh /opt/bioit/%{name}/%{version}/adjusthomopolymers.sh \
   --slave %{_bindir}/alltoall.sh alltoall.sh /opt/bioit/%{name}/%{version}/alltoall.sh \
   --slave %{_bindir}/analyzeaccession.sh analyzeaccession.sh /opt/bioit/%{name}/%{version}/analyzeaccession.sh \
   --slave %{_bindir}/analyzegenes.sh analyzegenes.sh /opt/bioit/%{name}/%{version}/analyzegenes.sh \
   --slave %{_bindir}/analyzesketchresults.sh analyzesketchresults.sh /opt/bioit/%{name}/%{version}/analyzesketchresults.sh \
   --slave %{_bindir}/applyvariants.sh applyvariants.sh /opt/bioit/%{name}/%{version}/applyvariants.sh \
   --slave %{_bindir}/a_sample_mt.sh a_sample_mt.sh /opt/bioit/%{name}/%{version}/a_sample_mt.sh \
   --slave %{_bindir}/bbcms.sh bbcms.sh /opt/bioit/%{name}/%{version}/bbcms.sh \
   --slave %{_bindir}/bbcountunique.sh bbcountunique.sh /opt/bioit/%{name}/%{version}/bbcountunique.sh \
   --slave %{_bindir}/bbduk.sh bbduk.sh /opt/bioit/%{name}/%{version}/bbduk.sh \
   --slave %{_bindir}/bbest.sh bbest.sh /opt/bioit/%{name}/%{version}/bbest.sh \
   --slave %{_bindir}/bbfakereads.sh bbfakereads.sh /opt/bioit/%{name}/%{version}/bbfakereads.sh \
   --slave %{_bindir}/bbmapskimmer.sh bbmapskimmer.sh /opt/bioit/%{name}/%{version}/bbmapskimmer.sh \
   --slave %{_bindir}/bbmask.sh bbmask.sh /opt/bioit/%{name}/%{version}/bbmask.sh \
   --slave %{_bindir}/bbmerge-auto.sh bbmerge-auto.sh /opt/bioit/%{name}/%{version}/bbmerge-auto.sh \
   --slave %{_bindir}/bbmerge.sh bbmerge.sh /opt/bioit/%{name}/%{version}/bbmerge.sh \
   --slave %{_bindir}/bbnorm.sh bbnorm.sh /opt/bioit/%{name}/%{version}/bbnorm.sh \
   --slave %{_bindir}/bbrealign.sh bbrealign.sh /opt/bioit/%{name}/%{version}/bbrealign.sh \
   --slave %{_bindir}/bbrename.sh bbrename.sh /opt/bioit/%{name}/%{version}/bbrename.sh \
   --slave %{_bindir}/bbsketch.sh bbsketch.sh /opt/bioit/%{name}/%{version}/bbsketch.sh \
   --slave %{_bindir}/bbsplitpairs.sh bbsplitpairs.sh /opt/bioit/%{name}/%{version}/bbsplitpairs.sh \
   --slave %{_bindir}/bbsplit.sh bbsplit.sh /opt/bioit/%{name}/%{version}/bbsplit.sh \
   --slave %{_bindir}/bbsstats.sh bbstats.sh /opt/bioit/%{name}/%{version}/bbstats.sh \
   --slave %{_bindir}/bbversion.sh bbversion.sh /opt/bioit/%{name}/%{version}/bbversion.sh \
   --slave %{_bindir}/bbwrap.sh bbwrap.sh /opt/bioit/%{name}/%{version}/bbwrap.sh \
   --slave %{_bindir}/bloomfilter.sh bloomfilter.sh /opt/bioit/%{name}/%{version}/bloomfilter.sh \
   --slave %{_bindir}/bloomfilterparser.sh bloomfilterparser.sh /opt/bioit/%{name}/%{version}/bloomfilterparser.sh \
   --slave %{_bindir}/calcmem.sh calcmem.sh /opt/bioit/%{name}/%{version}/calcmem.sh \
   --slave %{_bindir}/calctruequality.sh calctruequality.sh /opt/bioit/%{name}/%{version}/calctruequality.sh \
   --slave %{_bindir}/callgenes.sh callgenes.sh /opt/bioit/%{name}/%{version}/callgenes.sh \
   --slave %{_bindir}/callpeaks.sh callpeaks.sh /opt/bioit/%{name}/%{version}/callpeaks.sh \
   --slave %{_bindir}/callvariants2.sh callvariants2.sh /opt/bioit/%{name}/%{version}/callvariants2.sh \
   --slave %{_bindir}/callvariants.sh callvariants.sh /opt/bioit/%{name}/%{version}/callvariants.sh \
   --slave %{_bindir}/clumpify.sh clumpify.sh /opt/bioit/%{name}/%{version}/clumpify.sh \
   --slave %{_bindir}/commonkmers.sh commonkmers.sh /opt/bioit/%{name}/%{version}/commonkmers.sh \
   --slave %{_bindir}/comparegff.sh comparegff.sh /opt/bioit/%{name}/%{version}/comparegff.sh \
   --slave %{_bindir}/comparesketch.sh comparesketch.sh /opt/bioit/%{name}/%{version}/comparesketch.sh \
   --slave %{_bindir}/comparessu.sh comparessu.sh /opt/bioit/%{name}/%{version}/comparessu.sh \
   --slave %{_bindir}/comparevcf.sh comparevcf.sh /opt/bioit/%{name}/%{version}/comparevcf.sh \
   --slave %{_bindir}/consect.sh consect.sh /opt/bioit/%{name}/%{version}/consect.sh \
   --slave %{_bindir}/consensus.sh consensus.sh /opt/bioit/%{name}/%{version}/consensus.sh \
   --slave %{_bindir}/countbarcodes.sh countbarcodes.sh /opt/bioit/%{name}/%{version}/countbarcodes.sh \
   --slave %{_bindir}/countgc.sh countgc.sh /opt/bioit/%{name}/%{version}/countgc.sh \
   --slave %{_bindir}/countsharedlines.sh countsharedlines.sh /opt/bioit/%{name}/%{version}/countsharedlines.sh \
   --slave %{_bindir}/crossblock.sh crossblock.sh /opt/bioit/%{name}/%{version}/crossblock.sh \
   --slave %{_bindir}/crosscontaminate.sh crosscontaminate.sh /opt/bioit/%{name}/%{version}/crosscontaminate.sh \
   --slave %{_bindir}/cutgff.sh cutgff.sh /opt/bioit/%{name}/%{version}/cutgff.sh \
   --slave %{_bindir}/cutprimers.sh cutprimers.sh /opt/bioit/%{name}/%{version}/cutprimers.sh \
   --slave %{_bindir}/decontaminate.sh decontaminate.sh /opt/bioit/%{name}/%{version}/decontaminate.sh \
   --slave %{_bindir}/dedupe2.sh dedupe2.sh /opt/bioit/%{name}/%{version}/dedupe2.sh \
   --slave %{_bindir}/dedupebymapping.sh dedupebymapping.sh /opt/bioit/%{name}/%{version}/dedupebymapping.sh \
   --slave %{_bindir}/dedupe.sh dedupe.sh /opt/bioit/%{name}/%{version}/dedupe.sh \
   --slave %{_bindir}/demuxbyname.sh demuxbyname.sh /opt/bioit/%{name}/%{version}/demuxbyname.sh \
   --slave %{_bindir}/diskbench.sh diskbench.sh /opt/bioit/%{name}/%{version}/diskbench.sh \
   --slave %{_bindir}/estherfilter.sh estherfilter.sh /opt/bioit/%{name}/%{version}/estherfilter.sh \
   --slave %{_bindir}/explodetree.sh explodetree.sh /opt/bioit/%{name}/%{version}/explodetree.sh \
   --slave %{_bindir}/fetchproks.sh fetchproks.sh /opt/bioit/%{name}/%{version}/fetchproks.sh \
   --slave %{_bindir}/filterassemblysummary.sh filterassemblysummary.sh /opt/bioit/%{name}/%{version}/filterassemblysummary.sh \
   --slave %{_bindir}/filterbarcodes.sh filterbarcodes.sh /opt/bioit/%{name}/%{version}/filterbarcodes.sh \
   --slave %{_bindir}/filterbycoverage.sh filterbycoverage.sh /opt/bioit/%{name}/%{version}/filterbycoverage.sh \
   --slave %{_bindir}/filterbyname.sh filterbyname.sh /opt/bioit/%{name}/%{version}/filterbyname.sh \
   --slave %{_bindir}/filterbysequence.sh filterbysequence.sh /opt/bioit/%{name}/%{version}/filterbysequence.sh \
   --slave %{_bindir}/filterbytaxa.sh filterbytaxa.sh /opt/bioit/%{name}/%{version}/filterbytaxa.sh \
   --slave %{_bindir}/filterbytile.sh filterbytile.sh /opt/bioit/%{name}/%{version}/filterbytile.sh \
   --slave %{_bindir}/filterlines.sh filterlines.sh /opt/bioit/%{name}/%{version}/filterlines.sh \
   --slave %{_bindir}/filterqc.sh filterqc.sh /opt/bioit/%{name}/%{version}/filterlines.sh \
   --slave %{_bindir}/filtersam.sh filtersam.sh /opt/bioit/%{name}/%{version}/filtersam.sh \
   --slave %{_bindir}/filtersilva.sh filtersilva.sh /opt/bioit/%{name}/%{version}/filtersilva.sh \
   --slave %{_bindir}/filtersubs.sh filtersubs.sh /opt/bioit/%{name}/%{version}/filtersubs.sh \
   --slave %{_bindir}/filtervcf.sh filtervcf.sh /opt/bioit/%{name}/%{version}/filtervcf.sh \
   --slave %{_bindir}/fixgaps.sh fixgaps.sh /opt/bioit/%{name}/%{version}/fixgaps.sh \
   --slave %{_bindir}/fungalrelease.sh fungalrelease.sh /opt/bioit/%{name}/%{version}/fungalrelease.sh \
   --slave %{_bindir}/fuse.sh fuse.sh /opt/bioit/%{name}/%{version}/fuse.sh \
   --slave %{_bindir}/gbff2gff.sh gbff2gff.sh /opt/bioit/%{name}/%{version}/gbff2gff.sh \
   --slave %{_bindir}/getreads.sh getreads.sh /opt/bioit/%{name}/%{version}/getreads.sh \
   --slave %{_bindir}/gi2ancestors.sh gi2ancestors.sh /opt/bioit/%{name}/%{version}/gi2ancestors.sh \
   --slave %{_bindir}/gi2taxid.sh gi2taxid.sh /opt/bioit/%{name}/%{version}/gi2taxid.sh \
   --slave %{_bindir}/gitable.sh gitable.sh /opt/bioit/%{name}/%{version}/gitable.sh \
   --slave %{_bindir}/grademerge.sh grademerge.sh /opt/bioit/%{name}/%{version}/grademerge.sh \
   --slave %{_bindir}/gradesam.sh gradesam.sh /opt/bioit/%{name}/%{version}/gradesam.sh \
   --slave %{_bindir}/icecreamfinder.sh icecreamfinder.sh /opt/bioit/%{name}/%{version}/icecreamfinder.sh \
   --slave %{_bindir}/icecreamgrader.sh icecreamgrader.sh /opt/bioit/%{name}/%{version}/icecreamgrader.sh \
   --slave %{_bindir}/icecreammaker.sh icecreammaker.sh /opt/bioit/%{name}/%{version}/icecreammaker.sh \
   --slave %{_bindir}/idmatrix.sh idmatrix.sh /opt/bioit/%{name}/%{version}/idmatrix.sh \
   --slave %{_bindir}/idtree.sh idtree.sh /opt/bioit/%{name}/%{version}/idtree.sh \
   --slave %{_bindir}/invertkey.sh invertkey.sh /opt/bioit/%{name}/%{version}/invertkey.sh \
   --slave %{_bindir}/kapastats.sh kapastats.sh /opt/bioit/%{name}/%{version}/kapastats.sh \
   --slave %{_bindir}/kcompress.sh kcompress.sh /opt/bioit/%{name}/%{version}/kcompress.sh \
   --slave %{_bindir}/keepbestcopy.sh keepbestcopy.sh /opt/bioit/%{name}/%{version}/keepbestcopy.sh \
   --slave %{_bindir}/khist.sh khist.sh /opt/bioit/%{name}/%{version}/khist.sh \
   --slave %{_bindir}/kmercountexact.sh kmercountexact.sh /opt/bioit/%{name}/%{version}/kmercountexact.sh \
   --slave %{_bindir}/kmercountmulti.sh kmercountmulti.sh /opt/bioit/%{name}/%{version}/kmercountmulti.sh \
   --slave %{_bindir}/kmercoverage.sh kmercoverage.sh /opt/bioit/%{name}/%{version}/kmercoverage.sh \
   --slave %{_bindir}/kmerfilterset.sh kmerfilterset.sh /opt/bioit/%{name}/%{version}/kmerfilterset.sh \
   --slave %{_bindir}/kmerlimit2.sh kmerlimit2.sh /opt/bioit/%{name}/%{version}/kmerlimit2.sh \
   --slave %{_bindir}/kmerlimit.sh kmerlimit.sh /opt/bioit/%{name}/%{version}/kmerlimit.sh \
   --slave %{_bindir}/kmerposition.sh kmerposition.sh /opt/bioit/%{name}/%{version}/kmerposition.sh \
   --slave %{_bindir}/kmutate.sh kmutate.sh /opt/bioit/%{name}/%{version}/kmutate.sh \
   --slave %{_bindir}/lilypad.sh lilypad.sh /opt/bioit/%{name}/%{version}/lilypad.sh \
   --slave %{_bindir}/loadreads.sh loadreads.sh /opt/bioit/%{name}/%{version}/loadreads.sh \
   --slave %{_bindir}/loglog.sh loglog.sh /opt/bioit/%{name}/%{version}/loglog.sh \
   --slave %{_bindir}/makechimeras.sh makechimeras.sh /opt/bioit/%{name}/%{version}/makechimeras.sh \
   --slave %{_bindir}/makecontaminatedgenomes.sh makecontaminatedgenomes.sh /opt/bioit/%{name}/%{version}/makecontaminatedgenomes.sh \
   --slave %{_bindir}/makepolymers.sh makepolymers.sh /opt/bioit/%{name}/%{version}/makepolymers.sh \
   --slave %{_bindir}/mapPacBio.sh mapPacBio.sh /opt/bioit/%{name}/%{version}/mapPacBio.sh \
   --slave %{_bindir}/matrixtocolumns.sh matrixtocolumns.sh /opt/bioit/%{name}/%{version}/matrixtocolumns.sh \
   --slave %{_bindir}/mergebarcodes.sh mergebarcodes.sh /opt/bioit/%{name}/%{version}/mergebarcodes.sh \
   --slave %{_bindir}/mergeOTUs.sh mergeOTUs.sh /opt/bioit/%{name}/%{version}/mergeOTUs.sh \
   --slave %{_bindir}/mergepgm.sh mergepgm.sh /opt/bioit/%{name}/%{version}/mergepgm.sh \
   --slave %{_bindir}/mergeribo.sh mergeribo.sh /opt/bioit/%{name}/%{version}/mergeribo.sh \
   --slave %{_bindir}/mergesam.sh mergesam.sh /opt/bioit/%{name}/%{version}/mergesam.sh \
   --slave %{_bindir}/mergesketch.sh mergesketch.sh /opt/bioit/%{name}/%{version}/mergesketch.sh \
   --slave %{_bindir}/mergesorted.sh mergesorted.sh /opt/bioit/%{name}/%{version}/mergesorted.sh \
   --slave %{_bindir}/msa.sh msa.sh /opt/bioit/%{name}/%{version}/msa.sh \
   --slave %{_bindir}/mutate.sh mutate.sh /opt/bioit/%{name}/%{version}/mutate.sh \
   --slave %{_bindir}/muxbyname.sh muxbyname.sh /opt/bioit/%{name}/%{version}/muxbyname.sh \
   --slave %{_bindir}/partition.sh partition.sh /opt/bioit/%{name}/%{version}/partition.sh \
   --slave %{_bindir}/phylip2fasta.sh phylip2fasta.sh /opt/bioit/%{name}/%{version}/phylip2fasta.sh \
   --slave %{_bindir}/pileup.sh pileup.sh /opt/bioit/%{name}/%{version}/pileup.sh \
   --slave %{_bindir}/plotflowcell.sh plotflowcell.sh /opt/bioit/%{name}/%{version}/plotflowcell.sh \
   --slave %{_bindir}/plotgc.sh plotgc.sh /opt/bioit/%{name}/%{version}/plotgc.sh \
   --slave %{_bindir}/postfilter.sh postfilter.sh /opt/bioit/%{name}/%{version}/postfilter.sh \
   --slave %{_bindir}/printtime.sh printtime.sh /opt/bioit/%{name}/%{version}/printtime.sh \
   --slave %{_bindir}/processfrag.sh processfrag.sh /opt/bioit/%{name}/%{version}/processfrag.sh \
   --slave %{_bindir}/processhi-c.sh processhi-c.sh /opt/bioit/%{name}/%{version}/processhi-c.sh \
   --slave %{_bindir}/processspeed.sh processspeed.sh /opt/bioit/%{name}/%{version}/processspeed.sh \
   --slave %{_bindir}/randomgenome.sh randomgenome.sh /opt/bioit/%{name}/%{version}/randomgenome.sh \
   --slave %{_bindir}/randomreads.sh randomreads.sh /opt/bioit/%{name}/%{version}/randomreads.sh \
   --slave %{_bindir}/readlength.sh readlength.sh /opt/bioit/%{name}/%{version}/readlength.sh \
   --slave %{_bindir}/readqc.sh readqc.sh /opt/bioit/%{name}/%{version}/readqc.sh \
   --slave %{_bindir}/reducesilva.sh reducesilva.sh /opt/bioit/%{name}/%{version}/reducesilva.sh \
   --slave %{_bindir}/reformatpb.sh reformatpb.sh /opt/bioit/%{name}/%{version}/reformatpb.sh \
   --slave %{_bindir}/reformat.sh reformat.sh /opt/bioit/%{name}/%{version}/reformat.sh \
   --slave %{_bindir}/removebadbarcodes.sh removebadbarcodes.sh /opt/bioit/%{name}/%{version}/removebadbarcodes.sh \
   --slave %{_bindir}/removecatdogmousehuman.sh removecatdogmousehuman.sh /opt/bioit/%{name}/%{version}/removecatdogmousehuman.sh \
   --slave %{_bindir}/removehuman2.sh removehuman2.sh /opt/bioit/%{name}/%{version}/removehuman2.sh \
   --slave %{_bindir}/removehuman.sh removehuman.sh /opt/bioit/%{name}/%{version}/removehuman.sh \
   --slave %{_bindir}/removemicrobes.sh removemicrobes.sh /opt/bioit/%{name}/%{version}/removemicrobes.sh \
   --slave %{_bindir}/removesmartbell.sh removesmartbell.sh /opt/bioit/%{name}/%{version}/removesmartbell.sh \
   --slave %{_bindir}/renameimg.sh renameimg.sh /opt/bioit/%{name}/%{version}/renameimg.sh \
   --slave %{_bindir}/rename.sh rename.sh /opt/bioit/%{name}/%{version}/rename.sh \
   --slave %{_bindir}/repair.sh repair.sh /opt/bioit/%{name}/%{version}/repair.sh \
   --slave %{_bindir}/replaceheaders.sh replaceheaders.sh /opt/bioit/%{name}/%{version}/replaceheaders.sh \
   --slave %{_bindir}/representative.sh representative.sh /opt/bioit/%{name}/%{version}/representative.sh \
   --slave %{_bindir}/rqcfilter2.sh rqcfilter2.sh /opt/bioit/%{name}/%{version}/rqcfilter2.sh \
   --slave %{_bindir}/rqcfilter.sh rqcfilter.sh /opt/bioit/%{name}/%{version}/rqcfilter.sh \
   --slave %{_bindir}/runhmm.sh runhmm.sh /opt/bioit/%{name}/%{version}/runhmm.sh \
   --slave %{_bindir}/samtoroc.sh samtoroc.sh /opt/bioit/%{name}/%{version}/samtoroc.sh \
   --slave %{_bindir}/seal.sh seal.sh /opt/bioit/%{name}/%{version}/seal.sh \
   --slave %{_bindir}/sendsketch.sh sendsketch.sh /opt/bioit/%{name}/%{version}/sendsketch.sh \
   --slave %{_bindir}/shred.sh shred.sh /opt/bioit/%{name}/%{version}/shred.sh \
   --slave %{_bindir}/shrinkaccession.sh shrinkaccession.sh /opt/bioit/%{name}/%{version}/shrinkaccession.sh \
   --slave %{_bindir}/shuffle2.sh shuffle2.sh /opt/bioit/%{name}/%{version}/shuffle2.sh \
   --slave %{_bindir}/shuffle.sh shuffle.sh /opt/bioit/%{name}/%{version}/shuffle.sh \
   --slave %{_bindir}/sketchblacklist2.sh sketchblacklist2.sh /opt/bioit/%{name}/%{version}/sketchblacklist2.sh \
   --slave %{_bindir}/sketchblacklist.sh sketchblacklist.sh /opt/bioit/%{name}/%{version}/sketchblacklist.sh \
   --slave %{_bindir}/sketch.sh sketch.sh /opt/bioit/%{name}/%{version}/sketch.sh \
   --slave %{_bindir}/sortbyname.sh sortbyname.sh /opt/bioit/%{name}/%{version}/sortbyname.sh \
   --slave %{_bindir}/splitbytaxa.sh splitbytaxa.sh /opt/bioit/%{name}/%{version}/splitbytaxa.sh \
   --slave %{_bindir}/splitnextera.sh splitnextera.sh /opt/bioit/%{name}/%{version}/splitnextera.sh \
   --slave %{_bindir}/splitribo.sh splitribo.sh /opt/bioit/%{name}/%{version}/splitribo.sh \
   --slave %{_bindir}/splitsam4way.sh splitsam4way.sh /opt/bioit/%{name}/%{version}/splitsam4way.sh \
   --slave %{_bindir}/splitsam6way.sh splitsam6way.sh /opt/bioit/%{name}/%{version}/splitsam6way.sh \
   --slave %{_bindir}/splitsam.sh splitsam.sh /opt/bioit/%{name}/%{version}/splitsam.sh \
   --slave %{_bindir}/stats.sh stats.sh /opt/bioit/%{name}/%{version}/stats.sh \
   --slave %{_bindir}/statswrapper.sh statswrapper.sh /opt/bioit/%{name}/%{version}/statswrapper.sh \
   --slave %{_bindir}/streamsam.sh streamsam.sh /opt/bioit/%{name}/%{version}/streamsam.sh \
   --slave %{_bindir}/subsketch.sh subsketch.sh /opt/bioit/%{name}/%{version}/subsketch.sh \
   --slave %{_bindir}/summarizecontam.sh summarizecontam.sh /opt/bioit/%{name}/%{version}/summarizecontam.sh \
   --slave %{_bindir}/summarizecoverage.sh summarizecoverage.sh /opt/bioit/%{name}/%{version}/summarizecoverage.sh \
   --slave %{_bindir}/summarizecrossblock.sh summarizecrossblock.sh /opt/bioit/%{name}/%{version}/summarizecrossblock.sh \
   --slave %{_bindir}/summarizemerge.sh summarizemerge.sh /opt/bioit/%{name}/%{version}/summarizemerge.sh \
   --slave %{_bindir}/summarizequast.sh summarizequast.sh /opt/bioit/%{name}/%{version}/summarizequast.sh \
   --slave %{_bindir}/summarizescafstats.sh summarizescafstats.sh /opt/bioit/%{name}/%{version}/summarizescafstats.sh \
   --slave %{_bindir}/summarizeseal.sh summarizeseal.sh /opt/bioit/%{name}/%{version}/summarizeseal.sh \
   --slave %{_bindir}/summarizesketch.sh summarizesketch.sh /opt/bioit/%{name}/%{version}/summarizesketch.sh \
   --slave %{_bindir}/synthmda.sh synthmda.sh /opt/bioit/%{name}/%{version}/synthmda.sh \
   --slave %{_bindir}/tadpipe.sh tadpipe.sh /opt/bioit/%{name}/%{version}/tadpipe.sh \
   --slave %{_bindir}/tadpole.sh tadpole.sh /opt/bioit/%{name}/%{version}/tadpole.sh \
   --slave %{_bindir}/tadwrapper.sh tadwrapper.sh /opt/bioit/%{name}/%{version}/tadwrapper.sh \
   --slave %{_bindir}/taxonomy.sh taxonomy.sh /opt/bioit/%{name}/%{version}/taxonomy.sh \
   --slave %{_bindir}/taxserver.sh taxserver.sh /opt/bioit/%{name}/%{version}/taxserver.sh \
   --slave %{_bindir}/taxsize.sh taxsize.sh /opt/bioit/%{name}/%{version}/taxsize.sh \
   --slave %{_bindir}/taxtree.sh taxtree.sh /opt/bioit/%{name}/%{version}/taxtree.sh \
   --slave %{_bindir}/testfilesystem.sh testfilesystem.sh /opt/bioit/%{name}/%{version}/testfilesystem.sh \
   --slave %{_bindir}/testformat2.sh testformat2.sh /opt/bioit/%{name}/%{version}/testformat2.sh \
   --slave %{_bindir}/testformat.sh testformat.sh /opt/bioit/%{name}/%{version}/testformat.sh \
   --slave %{_bindir}/tetramerfreq.sh tetramerfreq.sh /opt/bioit/%{name}/%{version}/tetramerfreq.sh \
   --slave %{_bindir}/textfile.sh textfile.sh /opt/bioit/%{name}/%{version}/textfile.sh \
   --slave %{_bindir}/translate6frames.sh translate6frames.sh /opt/bioit/%{name}/%{version}/translate6frames.sh \
   --slave %{_bindir}/unicode2ascii.sh unicode2ascii.sh /opt/bioit/%{name}/%{version}/unicode2ascii.sh \
   --slave %{_bindir}/unzip.sh unzip.sh /opt/bioit/%{name}/%{version}/unzip.sh \
   --slave %{_bindir}/vcf2gff.sh vcf2gff.sh /opt/bioit/%{name}/%{version}/vcf2gff.sh \
   --slave %{_bindir}/webcheck.sh webcheck.sh /opt/bioit/%{name}/%{version}/webcheck.sh \
   --slave %{_bindir}/Xcalcmem.sh Xcalcmem.sh /opt/bioit/%{name}/%{version}/Xcalcmem.sh

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bbmap /opt/bioit/%{name}/%{version}/bbmap.sh
fi

%files

%changelog
* Fri Oct 07 2022 Shane Sturrock <shane.sturrock@gmail.com> - 39.01-1
- Bugfixes

* Thu Sep 22 2022 Shane Sturrock <shane.sturrock@gmail.com> - 39.00-1
- Bugfixes

* Thu Aug 11 2022 Shane Sturrock <shane.sturrock@gmail.com> - 38.98-1
- Added bloom filter option lockedincrement, which substantially increases
  accuracy of overloaded counting Bloom filters, with a ~15% speed reduction.
  Disabled by default, except for BBCMS.
- Fixed a possible race condition in RQCFilter file writing.

* Thu Aug 04 2022 Shane Sturrock <shane.sturrock@gmail.com> - 38.97-1
- Added trimtips to BBDuk, mainly for trimming adapters on both ends of PacBio
  reads.
- Changed processing of reads longer than 200bp to force ASCII-33 quality.
- Enable automatic entryfilter in Clumpify to handle libraries with mostly
  identical reads.

* Fri Mar 04 2022 Shane Sturrock <shane.sturrock@gmail.com> - 38.96-1
- Bugfix release

* Wed Jan 19 2022 Shane Sturrock <shane.sturrock@gmail.com> - 38.95-1
- Bugfix release

* Fri Oct 22 2021 Shane Sturrock <shane.sturrock@gmail.com> - 38.94-1
- Bugfix release

* Thu Sep 23 2021 Shane Sturrock <shane.sturrock@gmail.com> - 38.93-1
- Bugfix release

* Tue Aug 17 2021 Shane Sturrock <shane.sturrock@gmail.com> - 38.92-1
- Bugfix release

* Tue Jul 20 2021 Shane Sturrock <shane.sturrock@gmail.com> - 38.91-1
- Fixed SendSketch json array format for very large input, on client side.
- Added maxload flag to BBCMS.

* Fri Feb 19 2021 Shane Sturrock <shane.sturrock@gmail.com> - 38.90-1
- Added support for degenerate amino acid symbols B, J, Z.
- Added workaround for BubblePopper 640 assertion failure.
- RQCFilter deterministic mode added for mapping phases.
- Wrapped instances of byte array instantiation in allocByte1D.

* Fri Jan 29 2021 Shane Sturrock <shane.sturrock@gmail.com> - 38.88-1
- Refactored many instances of numeric array initialization to use KillSwitch.
- Added donefile to RQCFilter2.
- Wrote initial Walker class for kmer set iteration.
- Added in-place condense to IntList/LongList/etc.
- Wrote LongListSet for extending LongList beyond 2b elements.
- Wrote LongListSetIterator.
- Fixed BBDuk speed flag; was limited to range 0-7.
- Changed BBDuk rcomp calls to accomodate amino mode.
- Added SuperLongList functionality and checks.
- Integrated SuperLongList into ReadStats for length histograms; read length
  histograms no longer have an upper length limit.
- ApplyVariants should correctly handle truncated scaffold names now.
- RQCFilter/ReadStats static variable hangover fixed.
- Wrote KExpand and kmutate.sh for creating sets of mutant kmers.
- Split Parse class off from Tools.

* Fri Nov 06 2020 Shane Sturrock <shane.sturrock@gmail.com> - 38.87-1
- SamStreamer now correctly sets the header for sam files with no reads, fixing
  a hang.
- LoadSharedHeader wait delay reduced from 1000 to 100ms.
- Removed leftover BBDuk entropy-trimming print statement.
- make universal flag document including e.g. cq (changequality).
- bzip2 fails on JGI cloud, though lbzip2 works.  Test bzip2 on Cori.
- Since code knows where docs are it should point to it.
- Complete list of common flags in a file, point every shell script to this.

* Fri Aug 28 2020 Shane Sturrock <shane.sturrock@gmail.com> - 38.86-1
- 38.85
  - Fixed fastq interleaving detection for a rare failure with PacBio reads.
  - Added entropy histogram support to BBDuk.
  - Pileup modifications and a bugfix.
  - Wrote ReformatPacBio, reformatpb.sh, and various support classes (ZMW,
    ZMWStreamer, PBHeader).
  - Modified BaseGraph to do alignment.
  - Modified BaseGraph to do piecewise alignment and handle overlaps correctly.
  - Added CCS support to ReformatPacBio, but it currently only works well on
    synthetic data.
  - Added artic3 primers to resources.
  - Wrote FlatAligner2.
  - Added hmm package and classes for parsing hmmsearch results.
  - Added jasper package for intern.
  - Added KmerPosition, KmerPosition3, and kmerposition.sh for positional kmer
    counts.  These were written by Jasper Toscani Field.
  - Added FlatAligner2 with flatter weights than FlatAligner.
  - Added ApplyVariants support for renaming, excluding certain indels, and
    better handling of variations in low-coverage regions.
  - Updated Covid scripts.
  - Added A_SampleSummary template.
  - Added BBDuk entropy histogram.
  - Fixed IceCreamMaker reference loading.
  - Fixed Tadpole1 ownership reinitialization bug.
  - Added total sub/var count to FilterSam.
  - Added CallVariants/VCF support for NearbyVarCount and Flag fields.
  - Added seed to RandomGenome.
  - Added TrimRead handling of aligned reads without attached SamLines.
- 38.86
  - Bump due to git glitch.

* Fri Aug 23 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.63-1
- Gene-calling long kmers are now uncompressed.
- tRNA and 5S now use 10-mers instead of 9-mers; plastid, plasmid, and viral
  sources are included.
- Fixed some remaining crash bugs from adding GC content to Sketches.
- Updated RefSeq protein sketching pipeline.

* Fri Aug 16 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.62-1
- Added ACGT count tracking and printgc to Sketch.
- Sketch JSON format now caps decimals places of some numbers.
- MergeSorted can now use subprocess for decompression.
- Added linear sketch sizing via the density flag.
- Added polyploid support for MutateGenome (ploidy and hetrate flags).
- Added nohomopolymers flag to MutateGenome.
- Updated calcmem.sh with path for pigz.
- Revised fetch pipeline scripts again.
- Added plasmids to prokprot; removed viroids which no longer exist.
- Sambamba should no longer print the banner.
- Wrote FetchProks and fetchproks.sh, for downloading one genome assembly and
  gff per prokaryotic genus.
- Updated model.pgm with all archaea and one bacteria per genus.
- Deleted spurious copy of GffLine.
- Split VcfToGff off of GffLine.
- Moved Gff-related classes to gff package.
- Wrote GbffFile, GbffLocus, and GbffFeature.
- Fixed equals method in StringNum.
- Rewrote CompareGff to take sequence name and type into account.
- Generated pgms for plastid and plasmid, but they made bacterial calling
  worse.
- Enabled 5S long kmer support (9-mers) for CallGenes.  Might be worthwhile
  ignoring the 1-count kmers.

* Fri Aug 09 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.61b-1
- 38.60
  - maxReads is now a required parameter for SamStreamer; this allows
    acceleration of some other tools when reads are limited.
  - Redid Sketch taxfilter.  Now there are two different taxfilters, white
    (include) and black (exclude).  The flags have changed.
  - Organism names are now acceptable for TaxFilter.
  - JNI mode for IceCreamFinder and BBMap is now automatic on NERSC or
    Mac/Linux AMD64 systems.
  - Moved OS/CPU environment detection from Data to Shared.
  - Restarted Sketch servers; they will no longer handle the old taxonomy
    filtering flags.
  - Added reformat complement flag.
  - Fixed spelling of complement in some cases.
  - Added Sketch taxID to Sketch lookup table.
  - Added Sketch server reference mode.
  - Sketch taxonomy and metadata filtering are now handled by DisplayParams,
    and done prior to comparison, exactly once, and in threads.
- 38.61
  - Added Sketch KID, WKID, and hits comparators.
  - Revised TaxonomyGuide.txt.
  - Wrote ThreadWaiter and simplified A_SampleMT.
  - Fixed an accidental use of bgzip for decompression.
  - Fixed an erroneous error message (header with no bases) from splitting
    reads of target length in FastaReadInputStream.
  - Added fixsra and addpairnum flags to RenameReads.
  - Modified and moved ncbi and sketch scripts to pipelines/fetch and
    pipelines/server.

* Fri Jul 26 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.59-1
- Added json output and stats redirection to IceCreamFinder.
- Added preliminary SamStreamer support to IceCreamFinder.
- SamStreamer now supports a limited number of reads.
- Added libbbtools.dylib (Mac version) to jni folder.  Thanks Jie Wang for
  compiling it!
- Updated makefile.osx and jni readme.
- CoveragePileup now detects and aborts when a scaffold is specified multiple
  times with different lengths.
- Added ByteBuilder.print(float x, int decimals).
- Added asrhist and irsrhist to IceCreamFinder.
- Fixed an unnecessary array copy in adapter detection; X is no properly added
  to reads with adapters detected.
- Added trim support to IceCreamFinder.

* Fri Jul 19 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.58-1
- Fixed PreParser failure when encountering a standalone equals sign.
- Fixed a bug in automatically setting Sketch blacklists for known databases.
- Updated server-starting shellscripts to point to the new URLs.
- Renamed Missing Adapter as Absent Adapter.
- Changed ambiguity logic to better classify reads when there are 2 passes.
- Adapter alignment is slightly more lenient when an inverted repeat is
  detected.
- Slightly accelerated adapter detection by changing conditionals to array
  lookups in the inner loop.
- SendSketch can now load TaxTree.
- Increased Sketch number of comparisons returned, to compensate for potential
  los ses during TaxFilter.

* Fri Jul 05 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.57-1
- 38.56
  - Improved and accelerated IceCreamFinder adapter detection.
  - Reduced discarding of reads with adapters only at the tips.
- 38.57
  - Greatly improved IceCreamFinder adapter detection sensitivity by aligning
    to more reads.
  - Increased speed of adapter aligner.
  - Added less-specific adapter-screening phases to reduce calls to the adapter
    aligner.
  - Added ambig output stream and changed the logic for determining ambiguous
    inverted repeats.
  - Adapter-containing inverted repeats no longer go to junctions output.
  - Improved timeless adapter aligner and made it default.
  - Added start location to low bits of timeless aligner score, but it does not
    seem to work.

* Fri Jun 28 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.55-1
- Made IceCreamFinder ~50% faster by debranching loops and optimizing cache
  footprint.
- Added IceCreamFinder junction output.
- Simplified shell scripts by centralizing path-setting commands.
- Moved JNI library loading to Shared.
- Wrote IceCreamAligner JNI version.
- Made IceCreamAligner JNI faster by adding functions for all alignments and
  adding 16-bit versions.
- Fixed bugs in calcmem.sh path setting and module loading on Cori.
- Automated jni library path setting (-Djava.library.path flag is no longer
  required).
- Disabled BBMerge attempt to load JNI libraries.
- Added magic number detection for .gz files.
- Disabled bgzip reading of non-bgzip .gz files, awaiting new bgzip release,
  because current bgzip breaks on concatenated gzip files (supposedly addressed
  after v1.9).

* Fri Jun 14 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.51-1
- Changed handling of same-name JSON keys; by default they are now replaced.
- Improved Sketch D3 output - added more keys, fixed depth handling.
- Subprocess testing now returns false for exit codes 126 and higher (missing
  libraries yield 127).
- Turned bgzip and pigz on by default for all programs.
- Made bgzip the default for RQCFilter.
- Modified TaxServer sketch portion to prevent carryover of parameters from
  subsequent queries.
- Fixed Sketch header reporting observed depth as actual depth.
- Wrote IceCreamFinder, IceCreamAligner, and icecreamfinder.sh.
- Wrote A_Sample_Generator, IceCreamMaker, and icecreammaker.sh.
- Moved A_Sample classes to new templates package.
- Changed some new Random() calls to Shared.threadLocalRandom().
- Added jsonarrays flag to Sketch.
- Wrote IceCreamGrader and icecreamgrader.sh.
- Renamed demuxbyname2.sh to demuxbyname.sh.

* Thu Jun 13 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.50b-1
- Added bgzip control flags and version parsing.
- .vcf.gz files now default to being written and read by bgzip.
- All gzip files now default to being read with bgzip over pigz.
- Non-vcf files will only be written with bgzip if the bgzip flag is added
  (for now).
- Added alternate Sketch addresses via vm flag.
- minProb and minQual moved from SketchObject to DisplayParams, requiring the
  modification of many methods.
- Simplified some Sketch method signatures by allowing DisplayParams to
  substitute for multiple parameters.
- Added Locale to all String formatting without it.
- Refactored DemuxByName2.
- Improved commenting of DemuxByName2 and related classes.
- Added PacBio subread support to PartionReads (partition.sh).
- Disabled ByteFile1 being forced outside of JGI.  ByteFile2 caused some
  problems, but those should be resolved now, I think...
- Added loglog and barcode flags to DemuxByName2.
- Fixed order of SendSketch setting server address to allow alternate (VM)
  server use.
- Fixed DemuxByName2 order of parsing parser args, allowing the barcode flag
  to trigger.
- Unified DemuxByName2 modes under a single mode field.
- Fixed maxrecords not being observed in Sketch JSON format.
- TaxServer sketch handler now does full parsing of URL arguments.
- Added D3 support to Sketch results.

* Fri May 24 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.49-1
- 38.48
  - Added samline field to Read. obj field is no longer used for SamLines.
    Caused substantial refactoring; may have introduced bugs when processing
    sam files (they will not be subtle if present).
  - BufferedMultiCross now offers a threaded mode, but this has not improved
    performance.
  - BufferedMultiCross now supports minReadsToDump and puts residual reads into
    unknown.
  - Fixed DemuxByName2 hamming distance code, and improved it to only remove
    colliding keys.
- 38.49
  - Fully commented DemuxByName2, BufferedMultiCros, MultiCros2, and
    MultiCros3.
  - Fixed a bug in MultiCros3 that created some duplicate reads.  Speed is now
    >950MB/s for twin files.

* Fri May 17 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.47-1
- Added demuxbyname2 hamming distance support.
- Renamed Var.COMPOUND to Var.MULTI and added Var.COMPLEX.
- Modified demuxbyname2.sh to use pigz.
- Increased compiler error level (@Override, shadowing) and fixed resulting
  errors.
- Wrote MultiCros3, which supports concurrent streams; this makes DemuxByName2
  faster.
- Made BufferedMultiCross an abstract superclass of MultiCros2 and MultiCros3.

* Fri May 10 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.46-1
- Added Unzip.java and fixed unzip.sh.  It is pretty resource-intensive,
  though, for a program that does nothing.  This is possible to improve.
- Added KID and WKID to Sketch format 3, and flags to disable them.
- CompareVCF now prints results to screen correctly when there is no output
  file.
- TaxServer now defaults to 200k max reads in local mode.
- In local mode, TaxServer no longer reads files with pigz.
- FilterVCF now correctly observes del and ins flags.
- Added Var.COMPOUND type for multiallelic variations.
- Added VCFLine.trimPrefix() and trimSuffix().
- Fixed bugs in trimToCanonical handling of compound variations.
- VCFLines split by allele now split INFO fields as well.
- Wrote demuxbyname2, to support massively multiplexed Novaseq runs.
- Splitting alleles now also splits the info field of VCFLines.

* Fri May 03 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.45-1
- Last restarted timestamp fixed for TaxServer stats page.
- Clarified randomreads.sh description of generating twin files versus
  interleaved.
- Added Read.countVars, CallVariants.findUniqueVars.
- Added support for indels and border to FilterSam.
- CallVariants can now force calls of specific alleles with an input vcf.
- VarMap is now iterable over values.
- Modified ShrinkAccession to optionally retain GI numbers.
- Fixed VCF genotype call of 1 for haploids failing filters.
- Updated GiToNcbi to read gi numbers from accession files since gi files will
  disappear soon.
- Clarified bbduk.sh comment on maxlength.
- Added unzip.sh script.
- Split Sketch displayfname into rfname and qfname.
- Fixed file column being enabled by default for sendsketch.
- Changed VarMap WAYS to 8, allowing 16 billion variants.
- Short match strings no longer generate consecutive symbols like mm because it
  is hard to parse.
- MSA.score() now accepts short or long match strings.
- CallVariants no longer generates long match strings prior to trimming, for
  perfect matches; 5-10% faster.
- FilterVCF can now split long substitutions into SNPs with the splitsubs flag.
- Fixed CalcTrueQuality ploidy unset warning.
- Add ls to testfilesystem.  May be inaccurate due to cache effects.
- Added amino acid codes B and Z, mapped to ANY (same as X).
- CallVariants now integrated into FilterSam.
- BBCMS now supports sam files, if error-correction is disabled (depth
  filtering is allowed).
- Added some columns to CallVariants screen output for average allele depth.
- Added taxonomic levels series and section.
- Added RenameGiToTaxid badheaders flag for logging.
- Added RenameGiToTaxid maxbadheaders flag for early termination when exceeded,
  and included it in the download scripts (at 5000 since recent nt contains
  2440 headers with no TaxID).
- Removed sharedVarMap from CallVariants2; replace with forcedVars1 or
  forcedVars2 for the two passes.
- FungalRelease agp generation now uses ByteStreamWriter over tsw and
  Read.breakAtGaps uses ByteBuilder over sb to save memory.

* Fri Apr 05 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.44-1
- Fixed a bug in Tools.parseKMG.
- Added qualhist to CallVariants.
- Added code in CallVariants to deal with recalibrated base quality.
- CallVariants no longer needs ref= prefix before fasta reference.
- FilterVCF can now split alleles.
- Modified mutate.sh to allow variable-length indels, and not put them too
  close together (to allow better grading).
- Major: Fixed BBDuk/Seal/Clumpify issue in failure to correctly
  reverse-complement some kmers.

* Fri Mar 29 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.43-1
- Wrote var2.VarKey for hashing.  May not use it.
- Added indel processing to fixVars, and Read.containsVars().
- Fixed bugs in reading insertions from VCF files.
- TaxServer usage no longer displays stats (stats are on the /stats page).
- Added ref flag to CompareVCF.
- Added shist to FilterVCF (for vars passing filter).
- FilterVCF no longer requires a reference (in most cases) if the VCF has a
  correct header.
- CallVariants modified to reduce negative impact of strand bias and read bias
  on score, in cases that otherwise appear fine.
- Demuxbyname can now do 1 file per sequence header, but it does not close the
  streams as soon as a sequence is written.  This would be better as a custom
  program.
- Removed a mysterious automatic newline from Read.toSam(bb).
- Wrote CoverageArray3A, Atomic version.
- Added atomic flag to CallVariants, which increases speed by up to 300
  percent.
- Increased speed of multithreaded coverage calculation even without atomic
  flag.
- Fixed stranded coverage default to false.
- Added CoverageArray.incrementRangeSynchronized.
- CallVariants trackstrand now correctly defaults to false, which disables the
  DP4 field.
- CalcTrueQuality should now ignore indels declared in a VCF.

* Fri Mar 15 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.42-1
- 38.40
  - Replaced some obsolete StringBuilder methods (mainly for read printing)
    with ByteBuilder.
  - Deleted obsolete classes ReadStreamStringWriter and SortByMapping.
  - Replaced many instances of StringBuilder with ByteBuilder.
  - Moved some fields from Gene to Shared.
  - Made Header class.
  - Fixed a float-to-int rounding-down problem making BBMerge not strictly obey
    the maxmismatches flag.
  - Redid RandomReads naming format to be pair-capable in sam format.
  - Converted all known header-parsing functions to use the new format.
  - Wrote SuperLongList.toString
  - Added Reformat prioritizelength flag for subsampling variable-length reads.
  - Fixed trailing whitespace in bhist.
- 38.41
  - Fixed a compile error.
- 38.42
  - Added stats handler to TaxServer, with version and quantity tracking.
  - Added bbversion field to sendsketch header.
  - Fixed SendSketch address parsing.
  - Added p and q suffixes to parseKMG.
  - Added PacBio read length modelling to RandomReads.
  - Fixed a CallVariants assertion with SamLine.RNAME_AS_BYTES.
  - Fixed major bug in vcf line reading, misinterpreting variant types,
    preventing BBDuk from parsing vcf properly.
  - Wrote SamStreamerMF, a multifile SamStreamer.
  - Integrated SamStreamerMF into CallVariants.  Now, with 8 sam.gz files,
    CallVariants is about 5x as fast on a 32-core node.
  - Fixed CallVariants vcf output MCOV reporting -1 when out= is set instead of
    vcf=.
  - Fixed ihist not working in BBDuk.

* Fri Feb 22 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.39-1
- Fixed a bug in phist (required polysymbol to be set).
- Fixed a bug in BBDuk amino mode (failure to support k=12).
- Fixed a bug in bhist (no newlines!).
- Sketch and Tax servers now tracks single versus bulk queries.
- Converted several ReadStats histograms from TextStreamWriter to
  ByteStreamWriter.

* Fri Feb 15 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.38-1
- 38.36
  - Increased Sketch minprob to 0.0008.  Q7 (80% accurate) areas will be used
    but Q6 (75%) will be ignored; before it was 0.0001 (Q6.1).  This slightly
increases accuracy with raw reads.
  - Trimrname now works on sam headers.
  - Trimrname is now automatically set to the same as trd unless explicitly
    overriden with the trimrname flag.
  - Added small RNA adapters to adapters.fa (thanks to Daniel N.)
  - Sketch now reports the number of unique kmers indexed.
  - BBTools can now read embl and gbk formats.
  - Added support for subcohort taxonomic level.
- 38.37
  - Fixed a bug in BBDuk JSON readsOut reporting.
  - BBSketch format 3 now prints taxID.
  - Fixed broken qin flag (was being overriden by autodetection).
  - Improved quality autodetection for out-of-range quality scores.
  - FastqReadInputStream now correctly inherits interleaving from FileFormat
    rather than running internal tests.
  - Added JsonParser.parseJsonObjectStatic.
  - Added Blacklist.toBlacklist.
  - Added SendSketch.toAddress, .setFromAddress, and .sendSketch (static).
  - Simplified SendSketch parsing.
  - TestFormat now automatically tries to detect organism with SendSketch.
  - ReadStats bhist is now faster by formatting with ByteBuilder.
  - Added TestFormat bhistlen flag to disable gigantic bhists.
- 38.38
  - Fixed a parsing error in SendSketch.
  - Wrote docs/RestartingServers.txt

* Fri Feb 01 2019 Shane Sturrock <shane.sturrock@gmail.com> - 38.35-1
- Added sketchonly flag to CompareSketch, allowing it to just sketch and write
  files but not actually run comparisons.
- Protein sketch server is now active.
- Added TaxTree.descendsFrom(child, parent).
- TaxTree now classifies species-attached no-rank archaeal nodes as strains in
  addition to bacteria.
- pigz --version is now recorded to determine whether -11 and -I flags are
  supported.
- Added sketch sixframes flag, for dealing with indels.  This works
  surprisingly well but bloats the genome size.  Probably the size should be
  divided by 6.
- Added prokprot sketch to RQCFilter.
- Sketch now ignores AA kmers spanning stop codons in sixframes mode.
- Fixed a flaw in rkmer generation following Ns, in many classes.
- Added Sketch toValue2 function to process dual kmers in an unbiased manner.
  This yields more accurate ANI.
- Added comparison logic for tracking k1 and k2 matches independently.
- toValue2 now handles aminos as well.
- Changed default kmer lengths from 31,0 to 32,23, and 10,7 to 11,7.
- Simplified some parts of Sketch, like removing aniFromWkid flag.
- Changed an assertion in TaxTree to a warning, because the latest version of
  NCBI taxdump contains errors.
- Validation of K and hash version between sketches is now more robust.
- Fixed all instances of kmer bitmasks to work correctly with k=32; prior limit
  was k=31.
- Added 1-bit antialiasing to Sketch hashcodes.
- Bumped hash version to 2.
- Increased amino default kmer length to 12,8 to increase specificity.
- Fixed an assertion failure in comparesketch perfile mode.
- Increased size of prokprot blacklist.
- Added Sketch refhits flag, to indicate the number of references sharing kmers
  with keys hitting a reference.
- Remade prokprot blacklists at a higher taxonomic level to deal with high
  conservation.
- Fixed an assertion with regards to sketchonly mode in comparesketch.
- avgrefhits is now weakly factored into score.
- Modified some rqcfilter2 sketch flags such as minprob.
- NOTE: Entropy is disabled in Sketch amino acid mode; might be worth checking
  the entropy of common amino kmers.

* Fri Dec 21 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.34-1
- 38.33
  - Shred now validates input files.
  - Reformat now has options for padding sequences.
  - ****KmerFilterSet now accepts an initial kmer set.
  - Wrote IntList3.
  - Wrote HashArrayHybridFast.
  - Changed HashArray bulk add contract.
  - Back-ported HashArrayHybridFast changes to KmerNode2D.
  - Seal now uses HashArrayHybrid; indexing Silva became >100x faster.
  - Sketch now uses HashArrayHybrid; indexing speed increased somewhat.
  - Added amino support to BBDuk.
  - Added amino support to KmerCountExact.
  - Added amino support to EntropyTracker.
  - Modified entropy defaults for amino acid mode with Sketch(?) and BBDuk(?)
  - Fixed tracking of PercentOfPairs for insert size statistics.
  - CompareSketch now automatically sets the protein, fungi, or mito path on
    NERSC.
  - Mutate.sh now works on amino acid sequences.
  - Validated CompareSketch on raw reads in protein space; it works amazingly well.
- 38.34
  - Wrote MetagenomeDataWriter to produce some stats for Brian Foster.
  - Modified PreParser and Shared to deal with determining the original command
    line

* Fri Nov 23 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.32-1
- Tadpole now refuses to run with no input files.
- BBMerge now supports filtermemory flag.
- Wrote KmerFilterSetMaker and kmerfilterset.sh to generate small covering sets
  of kmers for use with BBDuk.
- Added silent flags to suppress screen messages from BBDuk, Reformat, and
  KmerTab leSet-related classes.

* Fri Nov 16 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.31-1
- 38.30
  - More calibration of gene models.
  - Fixed some misassumptions in percent encoding.
  - Modified GatherKapaStats to output raw data.
  - Generated a minimal representation of RefSeq Microbial...  achieved 80%
    size reduction.
  - Changed the way pileup calculates coverage from soft-clipped bases; they
    are now ignored.
  - Changed the way samtools/sambamba exclusion flags are processed to be more
    flexible and faster.
  - Pileup now uses samtools to parse the header and sambamba to parse the
    reads, since sambamba is slow at reading headers.
  - Added key=value pair output to pileup.
  - Wrote ScoreTracker to track scores of accepted and rejected ORFs when
    calling genes.
- 38.31
  - Added long kmer support to RNA calling in CallGenes.
  - Added BBMerge flags maxmismatches and forcemerge.
  - Added Tadpole flag filtermem.

* Fri Nov 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.29-1
- 38.27
  - Bugfixes and improvements to gene calling.
  - Began adding RNA models to gene calling.
  - Refactored gene-caller to allow more flexibility with models; pgm format
    changed.
  - Adjusted default gene model.
- 38.28
  - Multithreaded AnalyzeGenes.
  - Wrote FloatList.
  - Fixed a bug in Tools.reverseInPlace for partial arrays.
  - Added trimcircular flag to Tadpole to trim ends of loop-loop contigs, which
    are presumably circular.
  - Finished tRNA and rRNA models and calling functions.
- 38.28
  - Fixed a bug in 3-column Sketch colors.
- 38.29
  - Calibration of gene models.
  - Fixed a bug with chloroOutFile/fbtOutFile name in RQCFilter2.
  - Sketch now allows integrated gene-calling for nucleotide to protein
    translation.
  - Added minsize and maxsize to RepresentativeSet.

* Fri Oct 12 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.26-1
- 38.24
  - Skipped this version.
- 38.25
  - Added maxcov flag to Tadpole.
  - Seal now supports filenames without the ref= flag to allow wildcard
    expansion.
  - Removed calcmem.sh perl dependency on Genepool, since Genepool is gone.
  - Fixed a logging bug in RQCFilter.
  - Added optical alias to RQCFilter.
  - Modified mergesorted.sh.
  - SortByName and MergeSorted buffer-resizing logic made safer.
  - Fixed leftRatio calculation in Tadpole for printing in contig headers.
  - Fixed an unwanted print statement in Tadpole dot generation.
  - Fixed a crash in Clumpify when handling Ns.
  - BBMap bloomserial now defaults to true.
  - Deleted normandcorrectwrapper.sh.
  - Updated removehuman, removehuman2, etc. to use Bloom filters and clarified
    that the scripts are for NERSC.
  - Wrote PercentEncoding for translating URLs, and made it more efficient by
    removing String functions.
- 38.26
  - Improved Blacklist name translation.
  - Data internmap is now faster and takes less memory.
  - Made prok package for prok gene-calling.
  - Moved LOGICAL_PROCESSORS to Shared to avoid an initialization order
    problem.
  - Fixed a bug in FastaReadInputStream with buffer resizing logic.
  - Disabled some assertions in BBIndex that do not appear to be valid with a
    long maxindel and many short contigs.
  - Added nl() and tab() to ByteBuilder.
  - Reduced memory prealloc request for kmer tables on high memory (>120G)
    nodes.
  - Fixed CallVariants reporting of deletion count.
  - Clarified CallVariants SamStreamer flag, and capped it at Shared.threads().
  - Clarified callvariants2.sh purpose and function.
  - Wrote AnalyzeGenes, CallGenes, and CompareGff.
  - Added amino acid output to CallGenes.

* Fri Aug 31 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.23-1
- Wrote hiseq.CycleTracker.
- Fixed a parse error in AnalyzeFlowCell.
- Added preliminary G-bubble-detection and elimination to AnalyzeFlowCell, but
  it is not clear if it is working correctly.
- Wrote hiseq.IlluminaHeaderParser.
- Revised A_Sample, A_SampleMT, and A_SampleByteFile with additional submethods
  to reduce the length of long methods.
- Removed JNI path flag from BBMerge, BBMap, and RQCFilter shell scripts.
- Fixed a bug in reading adaptersOut.fa from RQCFilter2.
- Changed the way path is appended to output files in RQCFilter2.
- Added poly-C flags to BBDuk.
- Wrote PolymerTracker.
- Added polymer count tracking to BBDuk and RQCFilter.
- Added clipfilter to Reformat.

* Fri Aug 17 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.22-1
- 38.21
  - Wrote JsonLiteral and modified Stats to not put quotes around formatted
    floats.
  - Added support for accession, gi, and header lookups to RenameGiToNcbi.
  - --help or --version now exit with status 0 rather than 1.
  - Updated some documentation.
  - Added BBDuk trimpolyg flag.
  - FlowCell MicroTiles now track more data and have more methods.
  - Wrote PlotFlowCell and plotflowcell.sh, to look at the distribution of
    polyG in NovaSeq runs.
  - Fixed a broken if-else in AccessionToTaxId that was causing TaxServer to
    start with prealloc false.
  - Fixed a bug in verifying other mapped stats in RQCFilter2.
- 38.22
  - Added getters for sketch.Comparison and Ssketch.CompareBuffer, and made
    fields private.
  - Fixed bug causing Sketch unique count to display incorrectly - bitsetbits
    had been changed from 2 to 1.  It should be 2; made static final.
  - Fixed an array size bug in Tadpole caused by increasing the range of
    termination codes.
  - Fixed a problem of Kmers being appended to ByteBuilders
    reverse-complemented.  This impacted Shaver2.
  - Fixed a static variable (MASK_CORE) hangover from Tadpole1 into Tadpole2
    with Ta dWrapper.
  - Added more BBDuk polyG options.
  - Added polyG options and tracking to RQCFilter.
  - Fixed an incident where a new KmerComparator was created unnecessarily.
  - Clumpify now correctly counts the number of reads when a temp file is
    streamed without being clumped.

* Fri Aug 10 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.20-1
- Added logsum and powsum to stats.sh gc output format 5.
- Fixed a bug in tracking reads in RQCFilter.
- Fixed a basic to extended taxonomy translation routine in TaxTree.
- Added JSON (format 8) to stats.sh.
- Fixed(?) BBMap tracking of trimm/untrimmed bases for mapped and unmapped
  reads.
- Fixed bugs in RQCFilter tracking of trim/untrimmed mapped bases.

* Fri Aug 03 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.19-1
- 38.17
  - Added Sketch minLevelExtended flag.  ***TODO: Document.
  - Fixed bbcms loglog using quality scores from the wrong read.
  - Wrote MergeSketch and mergesketch.sh.
  - Fixed a major bug in TaxTree.getNodeAtLevel and restarted all servers.
  - Wrote KmerLimit and kmerlimit.sh.
  - Wrote Shuffle2 and shuffle2.sh.
  - Changed blacklist_nt_species_1000.sketch to blacklist_nt_species_500.sketch
- 38.18
  - Modified RQCFilter and BBMap to correctly track and report unmapped reads
    and bases when using the Bloom filter.
  - Wrote RQCFilterStats for tracking relevant RQCFilter stats.  This is
    printed tofilterStats2.txt.
  - Added some columns to BBMap scafstats/refstats where a read is assigned to
    at most a single reference.
  - All classes that used ThreadLocalRandom now call Shared.threadLocalRandom()
    to comply with Java 6.
  - Wrote KmerLimit and kmerlimit.sh to restrict a randomly-ordered file to a
    specific number of unique kmers.
  - Wrote KmerLimit2 and kmerlimit2.sh to restrict an arbitrarily-ordered file
    to a specific number of unique kmers via subsampling.
  - Updated /pipelines/ scripts for fetching and sketching.
- 38.19
  - Updated RQCFilterData tar.
  - Updated wrapper shellscripts to handle Cori error messages.
  - Fixed a bug in tracking duplicate reads in RQCFilter.

* Fri Jul 27 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.16-1
- 38.12
  - Stats now omits the first size bracket if it is less than minscaf.
  - Fixed problems with extended stats in format 4-6.
  - Fixed a bug in reporting amount of spikin removed in RQCFilter.
  - Multithreaded kmer frequency histogram generation using kmer and ukmer
    packages.
  - mutate.sh now outputs vcf files.
  - Fixed processing of sam files with M, =, and X in cigar string.
  - Fixed a bloom filter BBMap bug in counting reads.
  - Updated some pipelines shell scripts.
  - Started writing a new KCountArray class, but abandoned it as the current
    one looks as efficient as possible.
- 38.13
  - Fixed a casting exception in Shared.sort.
  - Fixed missing column from mutate.sh vcf output.
  - Addslash for RandomReads now works with the illuminanames flag.
  - Fixed mutate.sh VCF files.
  - Wrote Contig and Edge classes.
  - Wrote ContigLengthComparator.
  - Transitioned Tadpole from building Reads to building Contigs.
  - Wrote ProcessContigThread.
  - Tadpole now writes additional information about contig ends to headers.
  - Tadpole now strictly uses F_BRANCH and B_BRANCH instead of just BRANCH
    (TODO: D_BRANCH).
  - Tadpole output should now have canonical orientation, order, and names
    (apart from circular contigs).
  - Tadpole1 now has a preliminary contig graph processing phase (in progress).
  - Tadpole now supports preliminary dot output (not yet correct).
  - Added appendln to some ByteBuilder methods.
  - Added print(Contig) to bsw.
- 38.14-38.15
  - Integrated dev Python changes; merging Git branches.
- 38.16
  - Ported Tadpole1 ProcessContigThread to Tadpole2.
  - Added perfile flag to CompareSketch, which allows multithreaded loading.
  - Added prealloc flag to CompareSketch.
  - Revised TaxServer to use Sketch index, and typically run 1 thread per
    sketch.
  - Added outsketch flag to CompareSketch.
  - Modified RandomGenome to be faster and more flexible, and added a shell
    script.

* Fri Jul 13 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.12-1
- Stats now omits the first size bracket if it is less than minscaf.
- Fixed problems with extended stats in format 4-6.
- Fixed a bug in reporting amount of spikin removed in RQCFilter.
- Multithreaded kmer frequency histogram generation using kmer and ukmer
  packages.
- mutate.sh now outputs vcf files.
- Fixed processing of sam files with M, =, and X in cigar string.
- Fixed a bloom filter BBMap bug in counting reads.
- Updated some pipelines shell scripts.

* Fri Jul 06 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.11-1
- 38.09
  - bbcms default bits changed from 1 to 2.
  - Improved bbcms tossjunk function.
  - Added documentation to bbcms and Tadpole.
  - Added fixextensions flag, and enabled it for CallVariants, BBDuk, Reformat,
    RQCFilter, BBNorm, BBMerge, BBMap, Tadpole, and bbcms.
  - RQCFilter now extends reads prior to merging if there is enough memory.
    This means the insert size histogram will take longer, but allow
    non-overlapping inserts.
  - BBMap now tracks statistics correctly when Bloom filter is enabled.
  - Fixed Children flag in TaxServer.
  - Shave and rinse no longer checks owner for initial high kmers.
  - Shave and rinse now ignores initial high kmers above the isJunction trigger
    for extension in some cases, for a large speedup in isolates (uses
    shaveFast flag).
  - Changed RandomReads default insert size distribution to more closely match
    JGI fragment library targets.
  - Multithreaded KmerCountArray/KmerCountArrayU ownership array allocation via
    OwnershipThread for a large speed increase in assembly.
  - Added 2passresize flag to Tadpole but it didn't seem to speed things up.
  - Added Constellation-like output option for CompareSketch.
  - Major changes to Kmer table sizing - a premade resize schedule is now used.
    Only for Kmer so far not UKmer.
- 38.10
  - Merged dev python changes.
- 38.11
  - Ported schedule to UKmer.
  - Fixed a bytesPerKmer bug in KmerCountExact for k>31.

* Fri Jun 22 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.08-1
- FilterByTaxa and RQCFilter no longer crash if a header cannot be parsed and
  the accession tables are not loaded.

* Fri Jun 15 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.07-1
- Changed KmerTable increment functions to require an incr value.
- Added sortbuffer flag to Tadpole, but speed was barely improved on high-depth
  Clumpified data.
- Migrated coremask and fillfast to tadpole2, but they make it slower for some
  reason.
- Migrated shave and rinse improvements to Tadpole2; these can make those steps
  dramatically faster in metagenomes.
- Added BloomFilter serialization.
- Increased default k and minhits of Bloom filter in RQCFilter2 and added
  serialized filters.
- Reduced RandomReads default quality.
- Made gaussian insert size distribution default for RandomReads.
- Wrote FastaShredInputStream for faster Bloom filter loading with lower memory
  consumption.
- Fixed number of threads allocated to Bloom filter loading from index.

* Fri Jun 08 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.06-1
- Changed KmerArray to collide all possible kmer extensions into the same cell.
- Wrote FillFast to grab all 4 possible kmer extensions with a single modulo
  operation.
- Simplified some of BBDuk pair-tracking and discarding logic.
- Added trimfailures bbduk flag.
- Fixed a division by zero bug in SortByName.mergeRecursive.
- Fixed an array-out-of-bounds in CallPeaks.
- Made dual-kmer ANI estimation from Sketch more accurate.
- Added loglog support to BBMerge and Seal.
- Added loglogout support to BBMerge, BBDuk, and Seal.
- RQCFilter2 status.log now tracks kmers.
- Removed RQCFilter and pointed rqcfilter.sh to rqcfilter2.sh.

* Fri Jun 01 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.05-1
- Fixed interleaving detection in SortByName.
- Changed interleaving detection in FileFormat to audodetect more aggressively.
- Fixed a bug with RQCFilter2 interleaving settings carrying over from BBMerge
  to FilterByTaxa.

* Fri May 25 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.04-1
- 38.03
  - Fixed broken interleaving in bbcms output.
  - Added seed flag to bbcms and bloomfilter.
  - Added BBMerge vstrict and ustrict flags to bbcms.
  - Added mergeOK and testmerge flags to BBMerge.
  - Added BloomFilter support to BBMerge.
  - BBMerge now automatically writes both mergable and unmergable pairs to out
    if ecco=t and mix is unset.
  - testmerge flag now works with ecco.
  - Fixed indentation for Tadpole/bbcms results.
- 38.04
  - bbcms and bloom filter now allow random seeds.
  - Changed version printing to not repeat arguments.
  - Eliminated redundant copies of mergeOK functions.
  - Fixed bbcms testmerge flag.
  - Fixed trim/qtrim flag in BBSplit help.
  - Added relative error threshold for mergeOK.  TODO: Does not seem to help in
    my test; try on single cell data.
  - Added variable smooth width to bbcms.
  - Changed bbcms default bits to 4 after testing.
  - Fixed bbcms extra flag.

* Fri May 18 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.02-1
- 38.01
  - Added support for lowercase letters in accessions.
  - gi2ncbi now supports streaming and some other options like shrinknames in
    server mode.
  - Sketch can now return json format from a curl call.
  - Sketch server no longer crashes from invalid symbols in sequence in local
    mode.
  - SketchMaker now has a local cache of SketchHeaps per thread in per-taxa
    mode, allowing a 6x speedup by reducing synchronization and rework.
  - RefSeq now uses a 250-species blacklist limit with sizemult=2 instead of
    300.
  - Wrote MergeSorted and mergesorted.sh to resume SortByName runs that crashed
    or were killed during merging.
  - Removed DumpCount from SortByName and CrisContainer.  It was too confusing.
    To shuffle large datasets, they can be merged round-robin.
  - Fixed an error message when autodetecting quality encoding.
  - Refseq sketch server is now double the normal resolution (sizemult=2).
  - SendSketch defaults to sizemult=2 for RefSeq.
  - Sketch server startup script now sets sizemult=2 for refseq.
  - Added logscale peak calling.
  - Added peaks file GC annotation.
  - Fixed an array out of bounds in EntropyTracker.
  - CallVariants now ignores duplicates by default (0x400 bit).
  - StatsWrapper will now append to the gc output if there are multiple
    assemblies.
  - Wrote AnalyzeAccession and analyzeaccession.sh to reduce the memory
    footprint of accessions in the tax server.
  - Added entropy filter flag to RQCFilter2.
  - BloomFilter can now act as a highpass filter.
- 38.02
  - BloomFilter can now do error correction, using the Tadpole algorithm.
  - Added merge and unmerge to Tadpole and BloomFilter for dramatic error
    correction improvements.
  - Improved BloomFilter error correction defaults and added smoothing.
  - Improved BloomFilter's memory management and added a memfraction flag.
  - Fixed tuc not working.
  - Tadpole.BloomFilter ECC_ROLLBACK will now roll back merges also (but not
    ecco currently).
  - Wrote Rollback object to simplify rollbacks during error correction.
  - Spun BloomFilterCorrectorWrapper of from BloomFilterWrapper.
  - Spun bbcms.sh off of bloomfilter.sh.
  - Fixed a bug in msa.sh handling of reverse-complements.
  - Improved msa.sh to fully expand undefined bases, accept fasta files, and
    name the output such that it is clear whether an alignment was forward or
    reverse.
  - msa.sh now allows a cutoff for min identity.
  - Improved bbcms smoothing.
  - bbcms now allows a minimum fraction of kmers above a certain count to be
    specified.
  - bbcms now prints more statistics about the loaded bloom filter.
  
* Fri May 04 2018 Shane Sturrock <shane.sturrock@gmail.com> - 38.00-1
- Moved ByteBuilder to Structures.
- Added some formatting and comments to SuperLongList.
- JsonObject printing now has an inArray state that prevents newlines from
  arrays of JsonObjects.
- Improved JsonParser handling of booleans.
- Added a JsonParser validate command.
- Wrote TaxClient for internally doing tax lookups from the TaxServer.
- Added post mode to TaxClient and TaxServer, for URLs over 2000 characters.
- Moved StringNum to Structures.
- Accession loader now sorts files in ascending order of size and can load some
  before others.
- Fixed a flaw in the hash function for accession numbers that may have allowed
  collisions.
- TaxTree.parseNodeFromHeader will now try harder for headers with certain
  formatting.
- Fixed potential overflows by changing Integer.MAX_VALUE to
  Shared.MAX_ARRAY_LEN.
- SketchTool now has a custom, low-garbage loader instead of relying on
  ByteFile.
- RQCFilter2 now uses half as many threads for pigz as logical cores.
- Wrote BloomFilter and BloomFilterWrapper.
- Added BloomFilter support into BBMap and RQCFilter.
- Wrote a better available memory estimation function for BloomFilter.
- Accelerated BloomFilter lookup when minConsecutiveMatches>1.
- Fixed logging of BBSplit vs BBMap in RQCFilter2.
- Bloom filter creation from BBMap index now uses multiple threads per chunk.
- Fixed a null pointer in TextStringWriter.
- Fixed a static variable (ef) persisting in RQCFilter, which slowed human
  removal.
- Moved ByteBuilder to Structures.
- Added some formatting and comments to SuperLongList.
- JsonObject printing now has an inArray state that prevents newlines from
  arrays of JsonObjects.
- Improved JsonParser handling of booleans.
- Added a JsonParser validate command.
- Wrote TaxClient for internally doing tax lookups from the TaxServer.
- Added post mode to TaxClient and TaxServer, for URLs over 2000 characters.
- Moved StringNum to Structures.
- Accession loader now sorts files in ascending order of size and can load some
  before others.
- Fixed a flaw in the hash function for accession numbers that may have allowed
  collisions.
- TaxTree.parseNodeFromHeader will now try harder for headers with certain
  formatting.
- Fixed potential overflows by changing Integer.MAX_VALUE to
  Shared.MAX_ARRAY_LEN.
- SketchTool now has a custom, low-garbage loader instead of relying on
  ByteFile.
- RQCFilter2 now uses half as many threads for pigz as logical cores.
- Wrote BloomFilter and BloomFilterWrapper.
- Added BloomFilter support into BBMap and RQCFilter.
- Wrote a better available memory estimation function for BloomFilter.
- Accelerated BloomFilter lookup when minConsecutiveMatches>1.
- Fixed logging of BBSplit vs BBMap in RQCFilter2.
- Bloom filter creation from BBMap index now uses multiple threads per chunk.
- Fixed a null pointer in TextStringWriter.
- Fixed a static variable (ef) persisting in RQCFilter, which slowed human
  removal.

* Fri Apr 20 2018 Shane Sturrock <shane.sturrock@gmail.com> - 37.99-1
- 37.98
  - Fixed a bug in RQCFilter2 mousecatdoghuman mode with read-only files.
  - Added ksplit to BBDuk.
- 37.99
  - Improved error message when processing sam files with no MD tag in
    Reformat.
  - Possibly fixed a crash-hang during OutOfMemory exception handling in
    ConcurrentGenericReadInputStream.
  - Merged DNA and RNA artifact files for RQCFilter2; modified the primary
    artifact files, and removed redundancies.
  - Adapters are no longer present in Illumina.artifacts, only in adapters.fa.
  - Nextera linkers are no longer present in Illumina.artifacts.
  - PolyA is now a flag.
  - Created a second RQCFilterData - RQCFilterData_Local, identical but with
    unmasked sequence names.
  - Added ploidy flag to CallPeaks documentation.
  - Added polyA.fa.gz to resources.
  - Modified resources/sequencing_artifacts.fa.gz to remove adapter sequences
    and Nextera linkers.
  - Changed Read constructors to ensure amino acid flag is passed correctly.
  - Fixed an array length overflow in ByteBuilder.

* Fri Apr 13 2018 Shane Sturrock <shane.sturrock@gmail.com> - 37.97-1
- 37.96
  - Wrote FindJiCJunctions and processhi-c.sh for identifying and trimming
    junctions.
  - Added formatting functions in Tools to handle printing reads and bases
    processed.
  - Fixed a crash bug in CallVariants realign mode.
  - Fixed missing sample names in CallVariants multisample mode.
  - Fastawrap now supports kmg extensions.
  - Fixed assemblers trying to get stats from stdout.fa.
  - Fuse now allows length limits of fused output.
  - Wrote preliminary junction detection for CallVariants.
  - Made new RiboKmers files from Silva 132, and made a script for replicating
    the creation process (in /pipelines/).
  - Wrote var2.SoftClipper.
- 37.97
  - Added FilterByTile to RQCFilter.
  - Fixed a Clumpify crash-hang with low memory.
  - Made a Clumpify KmerSort superclass to reduce code redundancy between
    KmerSort versions.
  - Changed an exception handler in FastaReadInputStream to handle null-pointer
    exceptions as well.
  - Wrote RQCFilter2, with dependencies in a single path set by the
    rqcfilterdata flag.

* Fri Apr 06 2018 Shane Sturrock <shane.sturrock@gmail.com> - 37.95-1
- 37.94
  - Found and replaced some instances of z2=Xmx with z2=Xms in shells.
  - Reimplemented ByteFile.pushBack(line) to sidestep a NERSC slowdown in
    multithreaded java reading.
  - Fixed VcfLine.type().
  - Wrote GffLine and vcf2gff.sh.
  - Added CallVariants gff output.
  - Fixed pairLength() and pairCount() swap.
  - Fixed the way sambamba was being called.
  - Re-tested bcftools 1.7 and BBMap 37.94. CallVariants is 14x more efficient
    and 180x faster.
  - It is now difficult to replicate the memory/timing bug in 37.94 with
    CompareSketch bf1, but partially replicates with bf2.
  - TaxTree now checks for the auto keyword just before tree load.
  - Moved TaxNode size tracking from TaxServer to TaxTree.
  - Wrote SummarizeContamReport and summarizecontam.sh.
  - Fixed an off-by-one error in Var to GFF translation.
  - Added match generation from cigar, bases, and reference with no MDTags.
  - Fixed bug in MDWalker for substitutions immediately after deletions.
- 37.95
  - Reformat is now able to generate match strings from a reference instead of
    an MD Tag.
  - Default SamStreamer threads increased to 6, to deal with match string
    generation from sam 1.3.
  - ref added as a flag for various programs to enable MD-free sam line
    processing.
  - Fixed an assertion preventing # replacement for BBMap input.
  - Fixed handling of assertion errors during fastq quality encoding
    autodetection during initialization, for paired files in which file 2 has
    corrupted quality scores.
  - Program now prints a warning instead of terminating when quality format is
    specified but it seems wrong, in at least one case.
  - Check where BBNorm is writing temp files on Lustre.
  - Failed an attempt to accelerate FASTQ.quadToRead.

* Fri Mar 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 37.93-1
- 37.91
  - Multithreaded FilterVCF.  Poor speedup with vcfline.toVar, for reasons that
    are hard to diagnose.
  - Fixed a bug in ScafMap.loadVcfHeader.
  - Wrote Tools.parseDelimited.
  - Var.fromVCF now optionally imports extended information.
  - Added maxReads, minCov, and maxCov to VarFilter.
  - Reordered VCF info fields for faster parsing.
  - Added code to convince compiler some possible null pointer acceses were
    safe.
  - Added ConcurrentReadInputStream.returnList(ListNum) with internal null
    check.
  - Added an assertion to most paring statements expecting a non-null b.
  - Fixed several other potential null accesses.
  - Made AccessionToTaxid/RenameGiToNcbi somewhat faster; running multiple
    concurrent unpigz processes makes it slow.
  - Fixed taxpath setting failure in RenameGiToNcbi and other programs.
  - Added G.species name format support for TaxServer and taxonomy in general.
  - PreParser now supports printexecuting flag for command-line suppression of
    repeating the parameters.
  - Wrote SuperLongList.
  - Column needed for percent of library in sketch output, something like depth
    * genome size.
  - TestFormat2 now works better with negative numbers for quality and broken
    quality scores.
  - TestFormat2 supports additional fields like length mode and stddev.
- 37.92
  - Bump for Jenkins.
- 37.93
  - RQCFilter now defaults to auto for taxTreeFile.
  - Fixed BBSplit crashing when parsing flags without an = symbol.
  - Fixed some missing accession numbers in TaxServer.
  - TaxServer now timestamps queries and displays the number of NotFound
    queries.

* Tue Feb 13 2018 Shane Sturrock <shane.sturrock@gmail.com> - 37.90-1
- 37.89
  - Wrote ByteBuilder.appendFast(double, int).
  - Changed Var to perform calculations with doubles instead of floats.
  - Fixed nondeterminisim in RevisedAlleleFraction calculation.  This was not
    due to the use of floats vs doubles so the doubles can be changed back.
  - VCF/Var files are now written much faster, at around 55 MB/s up from 10
    MB/s.
  - ByteStreamWriter now supports multithreaded input.
  - FileFormat now detects VCF and Var files.
  - Added some information to Var header.
  - Wrote VcfWriter class to write VCF/Var files multithreaded, at up to 630
    MB/s.
  - Wrote Tools.isDigit, isLetter, toUpperCase, etc.  Character.isDigit is
    slow.
  - ByteBuilder now implements CharSequence, allowing it to be used with
    TextStreamWriter.
  - Changed several instances of StringBuilder and String.Format to
    ByteBuilder.
- 37.90
  - Multithreaded TetramerFrequencies.
  - Fixed some printing errors.
  - Multithreaded var2.MergeSamples.

* Thu Feb 01 2018 Shane Sturrock <shane.sturrock@gmail.com> - 37.88-1
- 37.87
  - Fixed a ByteBuilder overflow bug in append(long).
  - Changed TetramerFrequencies to use ByteBuilder.
  - Fixed missing else in CalcTrueQuality parser.
  - Added a new switch case to shellscripts to handle Shifter environment
    variables on Cori/Denovo.
  - Wrote multithreaded version of TestFormat.
  - Added merge and trim to TestFormat.
  - Better error message for ByteStreamWriter to read-only file.
  - TestFormat no longer crashes when trying to write to a read-only directory.
- 37.88
  - SummarizeSketch now supports colors.
  - Wrote CallVariants.findUniqueSubs to help locate bad NovaSeq reads.
  - Added variant-based read filtering to BBDuk.
  - Read.countSubs now supports shortmatch.
  - Fixed Read.countMatchSymbols().
  - Fixed clearfilters flag not clearing SamFilter, only VarFilter.
  - Var now parses depth, minusdepth, r1p, r2p, r1m, and r2m from VCF.
  - Added AD field to primary fields of VCF output for ease of parsing.
  - Wrote VcfLoader, a multithreaded VCF or var-format loader.

* Tue Jan 23 2018 Shane Sturrock <shane.sturrock@gmail.com> - 37.86-1
- 37.83
  - Merged a branch.
- 37.84
  - Bump.
- 37.85
  - Removed an obsolete module name from shellscripts.
  - Fixed BBMap bug in which files with uppercase letters were erroneously not
    found.
  - Modified TetramerFrequencies to comply with stricter compilation rules.
- 37.86
  - Modified TetramerFrequencies to make k a variable.
  - Changed TetramerFrequencies printing to use ByteBuilder.
  - Wrote TestFormat and testformat2.sh.
  - Undefined amino acids are now assigned X instead of .
  - Fixed a race condition in ByteFile2 via a defensive copy.

* Tue Jan 16 2018 Shane Sturrock <shane.sturrock@gmail.com> - 37.82-1
- Fixed BBMap producing X8 (insert size) tag for improper pairs (on different
  contigs).
- Added an early test for BBMap invalid input files.
- Added a triple switch to shellscripts for genepool/cori/denovo.

* Wed Jan 10 2018 Shane Sturrock <shane.sturrock@gmail.com> - 37.81-1
- Fixed a Json display error for duplicate names.
- Added Json parsing and printing support for escape characters and exponent
  numbers.
- Added Json parsing and printing support for arrays.
- Fixed a bug in ReadWrite failing to strip path correctly.

* Wed Jan 10 2018 Shane Sturrock <shane.sturrock@gmail.com> - 37.80-1
- 37.79
  - RenameGiToNcbi now accepts multiple input files.
  - TaxServer now handles favicon.ico requests.
  - Modified SortByName to better handle large numbers of temp files with long
    sequences, by reducing buffers and adding a mem mult.
  - Redid JsonObject to remove name field.
  - Wrote JsonParser.
  - Added stopcov option to Pileup.
  - Fixed a bug with reporting invalid bases in Read.
  - Regenerated RefSeq and nt sketches from the latest versions.
- 37.80
  - Fixed hidden compile errors.

* Tue Jan 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 37.78-1
- 37.77
  - Wrote ExplodeTree and explodetree.sh, to create a directory structure
    mirroring the tax tree.
  - Rearranged parse order in A_SampleByteFile and A_SampleD.
  - Added some convenience methods to TaxTree and TaxNode.
  - Wrote LongLongHashMap.
  - Added sequence path lookup to TaxServer.
  - LongHashMap and LongLongHashMap no longer include invalid entries in
    toArray().
  - Wrote IntLongHashMap.
  - Wrote TaxSize and taxsize.sh to generate the size of tax nodes.
  - Added Silva header parsing to TaxServer.
  - Added size lookup to TaxServer and created a RefSeq size file.
  - ByteStreamWriter.print methods now return this, to allow chaining.
  - Rewrote Read.validate() to be faster, simpler, and more modular.
  - Read MIN_ and MAX_CALLED_QUALITY are now private, and generally replaced by
    a remapping array.
  - Read validation no longer turns . - X to N by default.
  - Fixed toSemicolon method in TaxTree.
  - Increased TaxServer default memory to 52G in response to frequent GC during
    high query volume.
  - ByteFile1 mode is no longer forced on Denovo or Cori.
  - Added Parser.validateStdio() to ensure interleaving and file formats are
    specified when piping.  Currently only enabled for BBDuk, BBMap, and
    Reformat.
  - Added header and more columns to RepresentativeSet.
- 37.78
  - Updated citation guidlines.
  - Added validatebranchless flag and code path.
  - Improved validatebranchless to use binary instead of boolean or.
  - Removed invalid sequence cre_lox_lib_yadapt1 from reference collections.
  - Changed JsonObject handling of null values to be compliant.
  - Added JsonObject handling for floating-point types.
  - Added Json output for Sketch results.

* Wed Dec 13 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.76-1
- Added Shared.threadLocalRandom() to produce a ThreadLocalRandom when
  supported, and otherwise a Random.
- Converted some programs to use Shared.threadLocalRandom(), but not BBNorm
  since it uses .nextLong(long).
- DiskBench is now much faster in generating random text.
- TestFilesystem now supports multiple sequential files and is probably
  generating correct data.
- ReadWrite can now getRawOutputStream for /dev/null/* and will remove the *
  portion. This is much faster than writing to /dev/shm/*
- Removed an invalid assertion from RepresentativeSet.

* Tue Dec 12 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.75-1
- 37.73
  - Re-added libbbtoolsjni.so, which had somehow been removed.
  - Wrote DiskBench.java and diskbench.sh for comparing multithreaded I/O on
    local and networked disks.
  - Added RQCFilter flags for Clumpify groups and tmpdir.
- 37.74
  - Sketch servers now log the first 3 lines of the body of malformed queries
    to help diagnose the problem.
  - mouseCatDogHumanPath added to RQCFilter.
  - Changed parse order of silva flag in TaxServer.
  - Added RQCFilter dryrun flag.
  - Split RQCFilter aggressive flag into aggressivehuman and aggressivemicrobe.
  - Sketch servers no longer return error messages when query sketches are size
    0.
  - Fixed a parse bug allowing minkeycount to be 0 for sketch processing.
  - Sketch k2 can now only be set via k.
  - Sketch k2 can no longer be set to k.
  - Enabled verbose output from SketchTool (for debugging).
- 37.75
  - Fixed AssemblyStats default outstream and printing Executing... message.

* Thu Dec 07 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.72-1
- 37.69
  - Renamed kapatags.L40.fasta to kapatags.L40.fa and pJET1.2.fasta to
    pJET1.2.fa.
  - Added kapa support to RQCFilter.
  - Added pjet, lambda, mtst, and kapa keywords to BBDuk.
  - Added pjet, lambda, mtst, kapa, adapters, artifacts, and phix keywords to
    Seal to mirror BBDuk.
  - Moved breakReads from Reformat to Tools.
  - Wrote PreParser to allow output stream redirection.
  - Converted most classes to using PreParser.
  - Removed MakeCoverageHistogram.
  - Deprecated NormAndCorrectWrapper.
  - Generally got rid of printOptions(); help is in shellscripts, not code.
    This is handled in PreParser now.
- 37.70
  - Tightened project error and warning levels for compilation; modified a
    large amount of code to comply.
  - Deleted a redundant copy of KillSwitch.
  - Deleted redudant copies of safe array allocators.
- 37.71
  - Eliminated hyphen-stripping, java flag parsing, and null flag replacement
    from PreParser classes.
  - outstreams are now always closed in main, except in rare cases like
    TaxServer.
  - Added outstream to a few classes like BBMerge.
- 37.72
  - Moved some TaxServer parsing to ServerTools.
  - TaxServer no longer allows external file access by default.
  - TaxServer logs ip addresses of malformed queries.
  - Rewrote ServerTools.sendAndRecieve to be more robust.
  - Changed URLConnection to HttpURLConnection to allow error stream access.
  - Fixed a bug not displaying help in RemoveHuman.
  - calcmem.sh now supports SLURM_MEM_PER_NODE.  However this is only set when
    the --mem= flag is specified for job submission.
  - Sketch metadata is now set in SketchMaker for per-taxa and per-sequence
    modes.
  - Sketch results can now be filtered by optional metadata fields.

* Fri Dec 01 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.68-1
- Added Clumpify allowNs flag.
- Clumpify can now process containments and affixes.
- clumpify.sh no longer prints out the java version.
- Clumpify now supports a dupesubrate flag.

* Wed Nov 22 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.67-1
- Fixed a extended/normal level bug when widening TaxFilter.
- Updated CoveragePilup (pileup.sh) to give a more detailed summary, and import
  scaffold names from the reference sequences (default true) or reads (default
  false).
- Fixed crash when SamTools version string contains letters.
- RQCFilter now gathers chloro, ribo, mito references for mapping at the
  species level by default, rather than order.  This dramatically speeds up
  mapping, by 20x in some cases.
- Pileup now calculates kmer coverage.
- BBMap can now output coverage statistics with the cov flag even if there are
  no coverage files specified.
- Reformat can now calculate kmer statistics via the k flag.
- Reformat now ties loglog k to counting k.
- Setting loglogk now atomatically enables loglog.
- Fixed order of the conditional last column (name0) in Sketch output.
- Sketch format 3 now prints qsize and rsize instead of size ratio.
- RepresentativeSet now expects potentially 5 columns, with qsize and rsize.
- Clarified an assertion error in Seal.
- Added taxonomic filtering to RepresentativeSet.
- RepresentativeSet now prints the size of genomes retained and discarded.
- Strain can now be assigned to children of subspecies.
- TaxServer now prints children for life node.
- JsonObject now ignores attempts to add null values, preventing TaxServer from
  crashing.
- Comparison.taxID() and imgID() now return -1 rather than 0 if the number is
  undefined.
- Tweaked RepresentativeSet sorting to favor larger genomes; yields a slightly
  smaller output.
- Added pJET and lambda to BBMap resources.
- remote_files now additionally lists cat, dog, mouse, and microbial
  references.
- Sketch format 3 now prints out query size in bases, to avoid including
  massive sets of E.coli all listed under the same taxID.
- Added DedupeProtein, via the amino flag in dedupe.sh.
- Fixed a bug in Dedupe in which sequences could subsume each other if both
  contained the other.  This mainly happened when they were the same length but
  differed by substitutions.

* Tue Nov 07 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.66-1
- 37.65
  - TaxServer now caps sketch load threads at 2 for local files.
  - Added numChildren, minParentLevelExtended, and maxChildLevelExtended fields
    to TaxNode.
  - Added printChildren and printRange to taxonomy server URL parsing.
- 37.66
  - Changed tax server error response codes from 200 to 400.
  - Rewrote tax server URL parsing to be more flexible; /tax/ is no longer
    needed (though /sketch/ is).
  - Broke down server timing reports by local, remote, and usage.
  - Added TaxTree.getChildren() using a hashtable.
  - Depth and merge flags now work in sketch server local mode.
  - TaxServer has now enabled multithreaded local fastq sketch loading and
    capped the threads at 4 instead of 2 by default.
  - TaxServer handlers are now multithreaded, fixing poor response time when
    loading data in local mode.
  - RQCFilter now adds the original filename and organism name (if known) to
    sketch 
  - query headers.
  - RQCFilter now reports which microbes were used in filtering.

* Tue Oct 31 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.64-1
- 37.59
  - Increased memory for RefSeq sketches by 1g.
  - Set default Sketch entropy filter to 0.66.
  - Set default Sketch minprob to 0.0001, which is sufficient for 31bp at 74%
    (Q5.9).
  - Added EntropyTracker fast, slow, and superslow modes.
  - Added command-line flags for EntropyTracker speed, verify, and Sketch
    entropyK.
  - out=/dev/null no longer prompts you to delete it in most cases.
  - RQCFilter sketchminprob flag added, and default changed to 0.2 (95%; Q12.9).
  - Fixed a bug in EntropyTracker ns calculation and added it to verify().
  - RQCFilter now suppresses error messages when SendSketch fails due to
    connectivity issues.
  - Fully commented EntropyTracker.
  - Suppressed a race-condition-induced error message from closing the input
    stream early in Reformat and BBDuk.
- 37.60
  - Brought back UnicodeToAscii and changed it slightly.  Still does not work
    as intended, but may work in most cases.
- 37.61
  - Made some slight changes to EntropyTracker.
  - Added ribomap flag to RQCFilter.
  - Added default adapter sequences to RandomReads.
  - Suppressed printing some unnecessary verbose stuff from CoveragePileup.
  - Added kmersIn tracking to kmer counters.
  - KmerCountExact now prints average depth.
  - Added Tools.observedToActualCoverage().  This allows conversion of observed
    kmer counts to average kmer depth.
  - BBMap now has printstats and printsettings flags to suppress verbose
    output.
  - Revised observedToActualCoverage with a more precise estimate with a
    reverse curve-fit.
  - Added observedToActualCoverage to BBNorm.
  - Updated BBSketchGuide.txt with entropy, depth, and merging.
- 37.62
  - Average kmer quality is now tracked in Sketch and stored in the header.
  - Fixed a place in SketchTool where genomeSequences was not being reset to 0
    (should have no effect).
  - Added synonyms for onesketch and so forth so that the prefix mode= is no
    longer required.
  - CompareSketch can now use # notation for paired reads.
  - Added unique2 and unique3 flags.
  - Comparesketch now automatically generates an index if required by some
    columns.
  - Wrote TaxFilter.reviseByBestEffort(file) to allow closest available
    ancestors as output.
  - Added FilterByTaxa besteffort flag.
  - Improved FilterByTaxa output formatting.
  - TaxTree constructor became private.
  - TaxTree gained a static sharedTree which is used by default.
  - RQCFilter ribomap, chloromap, and mitomap automatically widen filter
    thresholds when nothing is found.
  - RQCFilter disables chloromap when the organism is not a plant
    (Viridiplantae), unless no taxa is given.
- 37.63
  - Fixed a bug when using Sketch constructor to pass average kmer quality and
    restarted servers.
  - Added anifromwkid flag to alternate between calculating ani from kid.
  - Added minbases to filter results, ignoring small reference sequences.
  - Added minsizeratio to filter results.  Intended mainly for all-to-all
    comparisons.
  - Added Strain and Substrain to TaxTree.
  - Added RepresentativeSet and representative.sh for condensing sets of
    genomes by all-to-all ANI.
- 37.64
  - Fixed a bug in determining which levels to print in PrintTaxonomy.

* Tue Oct 17 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.58-1
- 37.57
  - Changed default printOptions content.
  - Wrote MakePolymers.
  - Added period flag to MutateGenome.
  - Tested: Homopolymer blacklisting up to k=9 does not obviously improve
    sketch depth accuracy.
  - calcmem.sh now supports RQCMEM override flag (in megabytes).
  - BBSketch now supports intersection and printing sketch intersections.
  - Wrote Sketch.invertKey.  Note that this requires the reference.
  - Fixed an issue of not including ref= with # flag in SketchSearcher loading.
  - Fixed a bug stemming from a null return in SketchIndex when there are no
    matches.
  - Fixed an infinite loop in Sketch comparebydepth and volume.
  - Sketch score moved to a field to make sorting faster.
  - Deleted BBMask_noSam.java
- 37.58
  - Added exception handlers for AssertionErrors in cris.
  - Added nucleotide support to sketch files.
  - Added Var.noPassDotGenotype.
  - Wrote EntropyTracker.
  - Modified BBDuk to use EntropyTracker.
  - Modified BBMask to use EntropyTracker.
  - Note that entropy calculation was slightly off prior to EntropyTracker.
  - BBSketch now supports entropy filtering.
  - BBMap now supports sambamba for bam input.
* Tue Oct 03 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.56-1
- 37.51
  - Sketch ref= flag can now accept # wildcard.
  - BBDuk Poly-A trimming now occurs before entropy-masking.
  - Documented BBDuk internal order of operations in BBDukGuide.
  - Wrote MakeContaminatedGenomes and makecontaminatedgenomes.sh.
  - Removed a couple references to nonexistent changelogs in shellscripts.
  - Fixed a bug in ConcurrentReadInputStream.getReads (failure to call start).
  - ImgID sketch results header now is padded by spaces.
  - MDWalker can now handle cigar N symbol.
- 37.52
  - Fixed CompareSketch replacing original header filenames with sketch
    filenames.
  - Fixed a bug in FilterByTile by forcing IntList initial size to at least 1.
  - Added eoom (ExitOnOutOfMemoryException) shellscript support.
  - Added shellscript parsing for degenerate terms like xmx= and ea.
  - Added DisplayParams taxFilter field, and SketchResults autoremoval of
    nonpassing results.
  - Added TaxTree.parseLevel and called it in many parsing routines.
  - Made shellscript formating slightly more standardized.
  - Added some error checking to SendSketch; it now uses a nonzero exit code
    when the connection fails.
  - Updates shell scripts with references to guides.
  - Sketch now supports taxonomic filtering.
  - Delete an obsolete redundant guide.
- 37.53
  - Sketches now scale heap size with sizemult, and default heap size is
    doubled.
  - Fixed Refseq server; it was using a whitelist.
  - KillSwitch kill and print methods are now synchronized.
  - Moved parse location of Sketch db names to Searcher.
  - Searcher.refFiles is now a LinkedHashSet.
  - Added Tools.isDigitOrSign and toString(Throwable).
  - TaxServer now returns error messages from doubleheader parsing.
  - TaxFilter now always adds specified nodes regardless of tax level, and
    stops promoting as soon as the target level is reached.
  - Fixed some taxonomy server issues with tax filtering.
  - Added IntHashSetList for creating concise sets.
  - Added blacklists to Silva and RefSeq server invocations; they were missing.
  - All shellscripts now load oracle-jdk/1.8_144_64bit on Genepool.
  - Sketches now have a count array.
  - Sketch reading and writing now supports the count array.
  - Sketch spid parsing fixed.
  - No more spurious warnings about missing blacklists when they are not being
    used.
  - Accelerated Sketch writing by around 20% by debranching.
  - Changed TaxServer back to prior Java version because 8u144 is not installed
    on gpwebs.
  - Changed default startSilvaServer.sh to old style since the silva keyword is
    conflated.
  - Added Sketch minQual and minProb processing.
  - RefSeq is now the default sketch server, since bigger references are more
    accurate.
  - Added support for NCBI merged.dmp file in TaxTree (now mandatory).  This
    necessitates a coordinated push since the fo
  - rmat changed.
  - TaxServer no longer crashes when there are missing TaxNodes.
  - taxpath now works better with printtaxonomy.sh.
  - Sketch unique and nohit counts are now calculated correctly when
    printcontam is disabled.
  - BBDuk now correctly removes reads that fail maxlen even when no trimming is
    performed.
  - TaxServer now correctly tracks external query counts through a proxy (at
    NERSC).
- 37.55
  - TaxServer now reports average and most recent query time.
  - Making a Sketch from a Heap moved from SketchTool to SketchHeap.
  - Sketch construction now adds counts when available.
  - SketchMaker now parses display params.
  - Fixed an array out of bounds in LongHeapMap.
  - PrintDepth is now working!
  - Swapped minProb and minQual in SketchObject; parsing was bugged.
  - Added #-symbol support for dual fastq files in Sketch.
  - Added contains(key) to LongHeapSet and LongHeapMap.
  - SendSketch now loads fastq files multithreaded.  This is up to 6x as fast
    though slightly less efficient.
  - Reformat now can upsample via samplereadstarget/samplebasestarget.
- 37.56
  - SendSketch now does read validation in-thread and achieves up to 9x the
    speed of the singlethreaded version and bette
  - r efficiency.
  - CompareSketch had bufferlen cap removed when processing fastq.
  - SketchMaker has a new fast path for onesketch of a single fastq file, and
    default bufferlen changed from 1 to 2 to better deal with short sequences.
    For fastq, speed was quadrupled.
  - SketchMaker no longer prints an error message if there were no output
    sketches; instead, there is a warning.
  - Sketch now allows internal merging of paired reads.
  - RQCFilter defaults to merging reads and using minprob=0.75.
  - Added Sketch arbitrary metadata tags.
  - Added Sketch depth2 (repeat-compensated depth).
  - Regenerated nt and RefSeq reference sketches with coverage information and
    restarted the servers.
  - Added Sketch volume column.
  - Added IntHashSetList.toPackedArray.
  - SketchIndex now returns SketchResults with taxHits instead of a raw
    ArrayList.
  - contam2 now appears to work.
  - SketchMaker now obeys read limit.
  - Sketch results are now sortable by depth and volume.
  - RQCFilter now uses some additional sketch flags like volume.

* Wed Aug 30 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.50-1
- Documented autosizefactor in sketch shellscripts.
- Updated BBSketchGuide.txt with information about sketch sizing.
- Wrote fetchSilva.sh.
- Improved commenting of many /pipelines/ scripts.
- Modified RenameIMG to handle dual IMG files.
- Fixed img name parsing when no taxID is present.
- Fixed a failure to increment in TaxTree.parseDelimitedNumber.
- Sketch Amino mode now autosets k2, and a message is suppressed.
- Fixed a bug with Sketch amino mode parsing (it is parsed in 3 places).
- Really deleted ecc.sh from public BBTools distribution.
- Started MakeContaminatedGenomes.

* Mon Aug 21 2017 Shane Sturrock <shane.sturrock@gmail.com> - 37.48-1
- Updated BBSketch guide.
- Changed default IMG path to the k=31,24 version.
- Renamed minID to minWKID.
- MutateGenome can now output a smaller genome fraction of the original genome.
- Fixed a missing newline in Sketch server help info.
- BBSketch now supports non-multiples-of-4 for k2.
- Revised assemblyPipeline.sh.
- Added assembleMito to /pipelines.
- Increased hashing speed by 4-8% by switching from 2D to 1D matrix.
- Increased Sketch max kmer length to 32.
- Enabled pn0 (printseqname) flag for query.
- Fixed CompareSketch ignoring read limit when loading input files; this was
  caused by parse order.
- Reworded code description of maq to indicate it happens after trimming.
- Added mbq to BBDuk.
- Added Sketch ANI bisection, enabled by exactani flag.  But it made the
  results l
- ess accurate at low ANI than linear interpolation.
- Fixed a bug in which old 2D matrix was sometimes used instead of 1D matrix.
- Discovered current K=31,24 server sketches were generated with a bug;
  regenerating.
- Updated alapy compression support; speed flags are now enabled.
- Updated TaxonomyGuide.txt.
- Added testPlatformQuality.sh.
- Updated callInsertions.sh.
- Updated assemblyPipeline.sh.
- Made a MapPacBio assertion error more explicit, for debugging.
- TaxServer no longer logs usage queries.
- Clumpify spanx was controlling both spanx and spany due to a parse error;
  fixed.
- Added full range of delimiters to demuxbyname and clarified shellscript help.
- Added demuxbyname column mode (e.g. column=2 to demux by the 2nd column).
- Demuxbyname default compression level changed to 1 to cope with slow
  compression speed.
- Improved CompareSketch parsing of flags shared by Parser and DisplayParams.
- Added 3-column Sketch results.
- Restarted servers with new format support.
- Fixed a null pointer exception in Sketch format 3.
- Sketch now supports minANI flag.
- Added Sketch spid field and allowed spid and imgID to be set from SketchMaker
  command line.

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
