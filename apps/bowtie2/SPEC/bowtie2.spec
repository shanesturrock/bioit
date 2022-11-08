%define debug_package %{nil}
%define priority 2500
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bowtie2
Version:	2.5.0
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
* Wed Nov 09 2022 Shane Sturrock <shane.sturrock@gmail.com> - 2.5.0-1
- Overall improvements in the use of prefetch instructions. (contribution by
  Igor Sfiligoi)
- Made input/output fully asynchronous by using a dedicated thread.
  (contribution by Igor Sfiligoi)
- Added support for AVX2 256-bit instructions with can be enabled by setting
  the SSE_AXV2 environment variable at compile time. (contribution by Igor
  Sfiligoi)
- Fixed an issue causing bowtie2 to crash when processing ZSTD files with high
  compression ratios.
- Changed the way that unique alignments are counted in summary message to
  better match up with filters on SAM output

* Wed Jan 19 2022 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.5-1
- bowtie2
  - Fixed issues with bowtie2 BAM parser that would cause bowtie2 to crash when
    processing input that was encoded with tools other than samtools e.g.
    Picard.
  - Fixed an issue causing bowtie2 to drop certain optional fields when when
    aligning BAM reads with the --preserve-tags option.
  - Fixed an issue causing bowtie2 to produce mangled SAM output when
    specifying --sam-append-comment together with the --passthrough option.
  - Appended GO:query to SAM @HD entry to indicate that reads are grouped by
    query name, bump SAM version to 1.5 to indicate support for this change.
- bowtie2-build
  - Implemented thread pool to address performance regressions introduced
    during the switch to C++11 threads.
  - Fixed an issue causing masked-sequence metadata to be omitted from index.
    This issue would subsequently result in sequence data, @SQ, being left out
    from alignment SAM header.
  - Included .tmp extension to index files currenlty being built. The extension
    is removed only upon successful build. This change seeks to address the
    assumption that bowtie2-build ran successfully without building the reverse
    indexes.
  - Fixed an issue causing bowtie2-build to sometimes incorrectly calculate
    input size. This issue would result in the wrong index type being chosen
    and only happened with GZip compressed files.
- bowtie2-inspect
  - Added a new -o/--output option to save the output of bowtie2-inspect to a
    file instead of being dumped to standard output.

* Fri Jul 02 2021 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.4-1
- 2.4.3
  - Replaced TBB concurrency with C++ threads
  - Added native support for processing Zstd-compressed read files to >bowtie2
  - Added native support for processing Zstd-compressed reference-genome files
    to bowtie2-build
  - Fixed an issue causing bowtie2 to report incorrect alignments on big-endian
    machines
  - Fixed an issue causing bowtie2 to incorrectly process BAM files on
    big-endian machines
  - Fixed an issue causing bowtie2 to set an incorrect MAPQ when AS and XS are
    the maximum for read length
  - Add support for building on Apple M1 processors
- 2.4.4
  - Fixed an issue that would sometimes cause deadlocks in bowtie2 when running
    multithreaded

* Fri Oct 09 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.2-1
- Fixed an issue that would cause the bowtie2 wrapper script to throw an error
  when using wrapper-specific arguments.
- Added new --sam-append-comment flag that appends comment from FASTA/Q read to
  corresponding SAM record.
- Fixed an issue that would cause qupto, -u, to overflow when there are >= 232
  query sequences (PR #312).
- Fixed an issue that would cause bowtie2-build script to incorrectly process
  reference files.

* Fri Mar 06 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.1-1
- 2.4.1
  - Fixed an issue that would cause the bowtie2 wrapper script to incorrectly
    process certain arguments
- 2.4.0
  - Fixed an issue in -b <bam> input mode where one might prematurely close the
    read file pointer causing “Bad file descriptor” in other threads
  - Fixed an issue that could cause bowtie2 to crash in --no-1mm-upfront mode
  - Modified bowtie2-build to better handle of flags and positional parameters
  - Migrated all python scripts to python3
  - Added support for wildcards in input files to bowtie2, e.g. bowtie2 -x
    index -q *.fq as opposed to bowtie2 -x index -q 1.fq,2.fq,3.fq...
  - Fixed an issue causing bowtie2 to incorrectly process read names with slash
    mates plus extra characters (see #265)
  - Clarified support for overriding presets with more specific options e.g
    bowtie2 -x index --local --very-fast-local --L22 -q reads.fq will set the
    seed length to 22, overriding the 25 set by --very-fast-local
  - Modified SAM output for -k/-a so that supplementary alignments get assigned
    a MAPQ of 255
  - Fixed an issue that would sometimes cause bowtie2-build to not generate
    reverse index files
  - Added preliminary support for ppc64le architectures with the help of SIMDE
    project (see #271)
  - Fixed an issue causing bowtie2 to incorrectly calculate the MAPQ when --mp
    was specified in combination with --ignore-quals

* Fri May 03 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.5.1-1
- Added official support for BAM input files
- Added official support for CMake build system
- Added changes to Makefile for creating Reproducible builds (via
  [210](https://github.com/BenLangmead/bowtie2/pull/210))
- Fix an issue whereby building on aarch64 would require patching sed commands
  (via [#243](https://github.com/BenLangmead/bowtie2/pull/243))
- Fix an issue whereby `bowtie2` would incorrectly throw an error while
  processing `--interleaved` input

* Fri Mar 22 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.5-1
- Added support for obtaining input reads directly from the Sequence Read
  Archive, via NCBI's [NGS language bindings](https://github.com/ncbi/ngs).
  This is activated via the [`--sra-acc`](manual.shtml#bowtie2-options-sra-acc)
  option.  This implementation is based on Daehwan Kim's in
  [HISAT2](https://ccb.jhu.edu/software/hisat2).  Supports both unpaired and
  paired-end inputs.
- Bowtie 2 now compiles on ARM architectures (via
  [#216](https://github.com/BenLangmead/bowtie2/pull/216))
- `--interleaved` can now be combined with FASTA inputs (worked only with FASTQ
  before)
- Fixed issue whereby large indexes were not successfully found in the
  `$BOWTIE2_INDEXES` directory
- Fixed input from FIFOs (e.g. via process substitution) to distinguish
  gzip-compressed versus uncompressed input
- Fixed issue whereby arguments containing `bz2` `lz4` were misinterpreted as
  files
- Fixed several compiler warnings
- Fixed issue whereby both ends of a paired-end read could have negative TLEN
  if they exactly coincided
- Fixed issue whereby `bowtie2-build` would hang on end-of-file (via
  [#228](https://github.com/BenLangmead/bowtie2/pull/228))
- Fixed issue whereby wrapper script would sometimes create zombie processes
  (via [#51](https://github.com/BenLangmead/bowtie2/pull/51))
- Fixed issue whereby `bowtie2-build` and `bowtie2-inspect` wrappers would fail
  on some versions of Python/PyPy
- Replaced old, unhelpful `README.md` in the project with a version that
  includes badges, links and some highlights from the manual
- Note: BAM input support and CMake build support both remain experimental, but
  we expect to finalize them in the next release

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
