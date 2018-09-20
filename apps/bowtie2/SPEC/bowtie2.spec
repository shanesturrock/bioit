%define debug_package %{nil}
%define priority 2343
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bowtie2
Version:	2.3.4.3
Release:	1%{?dist}
Summary:	An ultrafast and memory-efficient tool for aligning sequencing reads to long reference sequences
Group:		Applications/Engineering
License:	GPLv3
URL:		http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
Bowtie 2 is an ultrafast and memory-efficient tool for
aligning sequencing reads to long reference sequences. It is
particularly good at aligning reads of about 50 up to 100s or 1,000s
of characters, and particularly good at aligning to relatively long
(e.g. mammalian) genomes. Bowtie 2 indexes the genome with an FM Index
to keep its memory footprint small: for the human genome, its memory
footprint is typically around 3.2 GB. Bowtie 2 supports gapped, local,
and paired-end alignment modes.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/bowtie2 bowtie2 /opt/bioit/%{name}/%{version}/bin/bowtie2 %{priority} \
   --slave %{_bindir}/bowtie2-build bowtie2-build /opt/bioit/%{name}/%{version}/bin/bowtie2-build \
   --slave %{_bindir}/bowtie2-build-l bowtie2-build-l /opt/bioit/%{name}/%{version}/bin/bowtie2-build-l \
   --slave %{_bindir}/bowtie2-build-s bowtie2-build-s /opt/bioit/%{name}/%{version}/bin/bowtie2-build-s \
   --slave %{_bindir}/bowtie2-align-l bowtie2-align-l /opt/bioit/%{name}/%{version}/bin/bowtie2-align-l \
   --slave %{_bindir}/bowtie2-align-s bowtie2-align-s /opt/bioit/%{name}/%{version}/bin/bowtie2-align-s \
   --slave %{_bindir}/bowtie2-inspect-l bowtie2-inspect-l /opt/bioit/%{name}/%{version}/bin/bowtie2-inspect-l \
   --slave %{_bindir}/bowtie2-inspect-s bowtie2-inspect-s /opt/bioit/%{name}/%{version}/bin/bowtie2-inspect-s \
   --slave %{_bindir}/bowtie2-inspect bowtie2-inspect /opt/bioit/%{name}/%{version}/bin/bowtie2-inspect

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bowtie2 /opt/bioit/%{name}/%{version}/bin/bowtie2
fi

%files

%changelog
* Fri Sep 21 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.4.3-1
- Fixed an issue causing `bowtie2-build` and `bowtie2-inspect` to output
  incomplete help text.
- Fixed an issue causing `bowtie2-inspect` to crash.
- Fixed an issue preventing `bowtie2` from processing paired and/or unpaired
  FASTQ reads together with interleaved FASTQ reads.

* Fri Aug 10 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.4.2-1
- Fixed issue causing bowtie2 to fail in --fast-local mode.
- Fixed issue causing --soft-clipped-unmapped-tlen to be a positional argument.
- New option --trim-to N causes bowtie2 to trim reads longer than N bases to
  exactly N bases. Can trim from either 3' or 5' end, e.g. --trim-to 5:30 trims
  reads to 30 bases, truncating at the 5' end.
- Updated "Building from source" manual section with additional instructions on
  installing TBB.
- Several other updates to manual, including new mentions of Bioconda and
  Biocontainers.
- Fixed an issue preventing bowtie2 from processing more than one pattern
  source when running single threaded.
- Fixed an issue causing bowtie2 and bowtie2-inspect to crash if the index
  contains a gap-only segment.
- Added experimental BAM input mode -b. Works only with unpaired input reads
  and BAM files that are sorted by read name (samtools sort -n). BAM input mode
  also supports the following options: 
    --preserve-sam-tags: Preserve any optional fields present in BAM record 
    --align-paired-reads: Paired-end mode for BAM files
- Add experimental CMake support

* Tue Feb 13 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.4.1-1
- Fixed an issue with `--reorder` that caused bowtie2 to crash while reordering
  SAM output

* Tue Jan 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.4-1
- Fixed major issue causing corrupt SAM output when using many threads
  (-p/--threads) on certain systems.
- Fixed an issue whereby bowtie2 processes could overwrite each others' named
  pipes on HPC systems.
- Fixed an issue causing bowtie2-build and bowtie2-inspect to return
  prematurely on Windows.
- Fixed issues raised by compiler "sanitizers" that could potentially have
  caused memory corruption or undefined behavior.
- Added the "continuous FASTA" input format (-F) for aligning all the k-mers in
  the sequences of a FASTA file. Useful for determining mapability of regions
  of the genome, and similar tasks.

* Tue Oct 17 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.3.1-1
- Fixed an issue causing input files to be skipped when running multi-threaded
  alignment
- Fixed an issue causing the first character of a read name to be dropped while
  parsing reads spl

* Tue Sep 12 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.3-1
- bowtie2-build now supports gzip-compressed FASTA inputs
- New --xeq parameter for bowtie2 disambiguates the 'M' CIGAR flag. When
  specified, matches are indicated with the = operation and mismatches with X
- Fixed a possible infinite loop during parallel index building due to the
  compiler optimizing away a loop condition
- Added --soft-clipped-unmapped-tlen parameter for bowtie2 that ignores
  soft-clipped bases when calculating template length (TLEN)
- Added support for multi-line sequences in FASTA read inputs
- Expanded explanation of MD:Z field in manual
- Fixed a crashing bug when output is redirected to a pipe
- Fixed ambiguity in the SEED alignment policy that sometimes caused -N
  parameter to be ignored

* Wed Jun 28 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.2-1
- Added support for interleaved paired-end FASTQ inputs (--interleaved)
- Now reports MREVERSE SAM flag for unaligned end when only one end of a pair
  aligns
- Fixed issue where first character of some read names was omitted from SAM
  output when using tabbed input formats
- Added --sam-no-qname-trunc option, which causes entire read name, including
  spaces, to be written to SAM output. This violates SAM specification, but can
  be useful in applications that immediately postprocess the SAM.
- Fixed compilation error caused by pointer comparison issue in
  aligner_result.cpp
- Removed termcap and readline dependencies introduced in v2.3.1
- Fixed compilation issues caused by gzbuffer function when compiling with zlib
  v1.2.3.5 and earlier. Users compiling against these libraries will use the
  zlib default buffer size of 8Kb when decompressing read files.
- Fixed issue that would cause Bowtie 2 hang when aligning FASTA inputs with
  more than one thread
