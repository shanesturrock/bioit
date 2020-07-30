%define priority 1300
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bowtie
Version:	1.3.0
Release:	1%{?dist}
Summary:	An ultrafast, memory-efficient short read aligner
Group:		Applications/Engineering
License:	Artistic 2.0
URL:		http://bowtie-bio.sourceforge.net/index.shtml
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description

Bowtie, an ultrafast, memory-efficient short read aligner for short
DNA sequences (reads) from next-gen sequencers. Please cite: Langmead
B, et al. Ultrafast and memory-efficient alignment of short DNA
sequences to the human genome. Genome Biol 10:R25.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/bowtie bowtie /opt/bioit/%{name}/%{version}/bin/bowtie %{priority} \
   --slave %{_bindir}/bowtie-build bowtie-build /opt/bioit/%{name}/%{version}/bin/bowtie-build \
   --slave %{_bindir}/bowtie-build-l bowtie-build-l /opt/bioit/%{name}/%{version}/bin/bowtie-build-l \
   --slave %{_bindir}/bowtie-build-s bowtie-build-s /opt/bioit/%{name}/%{version}/bin/bowtie-build-s \
   --slave %{_bindir}/bowtie-align-l bowtie-align-l /opt/bioit/%{name}/%{version}/bin/bowtie-align-l \
   --slave %{_bindir}/bowtie-align-s bowtie-align-s /opt/bioit/%{name}/%{version}/bin/bowtie-align-s \
   --slave %{_bindir}/bowtie-inspect-l bowtie-inspect-l /opt/bioit/%{name}/%{version}/bin/bowtie-inspect-l \
   --slave %{_bindir}/bowtie-inspect-s bowtie-inspect-s /opt/bioit/%{name}/%{version}/bin/bowtie-inspect-s \
   --slave %{_bindir}/bowtie-inspect bowtie-inspect /opt/bioit/%{name}/%{version}/bin/bowtie-inspect

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bowtie /opt/bioit/%{name}/%{version}/bin/bowtie
fi

%files

%changelog
* Fri Jul 31 2020 Shane Sturrock <shane.sturrock@gmail.com> - 1.3.0-1
- v1.2.3
  - Added support for reading and inspecting Bowtie 2 indexes. Bowtie 2 indexes
    can now be used with either Bowtie or Bowtie 2.
  - Added support for building an index from a gzipped-compressed FASTA.
  - Fixed issue preventing bowtie from reporting repeated alignments when -M is
    specified.
  - Fixed issue with -F mode omitting final base of each read.
  - Fixed clipping of first letter of first read in batches after first.
  - Fixed an issue preventing bowtie wrapper script from finding indexes.
- v1.3.0
  - Fixed an issue causing bowtie to report incorrect results when using a
    Bowtie 2 index.
  - New, more efficient implementation of --reorder for keeping SAM output
    lines in same order as input reads
  - Added -x parameter for specifying index. bowtie still supports specifying
    an index via positional parameter, but this behavior will be deprecated.
  - Migrated python scripts to python3.
  - Fully removed colorspace functionality.
  - Added support for compiling on ARM architectures.
  - Fixed an issue preventing bowtie from outputting newlines in --max and --un
    output files.
  - Fixed an issue causing alignment results to vary based on read names.
  - Fixed an issue preventing --no-unal from suppressing unmapped reads.
  - Removed dependence on some third-party libraries, simplifying the code and
    improving portability.
  - Fix an issue preventing bowtie from running with many threads on big-endian
    machines.

* Wed Dec 13 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.2.2-1
- Fixed major issue causing corrupt SAM output when using many threads
  (-p/--threads) on certain systems
- Fixed major issue with incorrect alignment offsets being reported in
  --large-index mode
- Fixed major issue with reads files being skipped when multiple inputs were
  specified together with -p/--threads
- The official LICENSE of Bowtie was changed to Artistic License 2.0. This
  fixes an issue with the previous LICENSE, which mistakenly combined elements
  of different open-source licenses.
- Fixed issue where bowtie would still run for a long time even when -u was set
  to a small number.
- Fixed spurious "Reads file contained a pattern with more than 1024 quality
  values" error for some colorspace inputs.
- Fixed issue with --strata sometimes failing to suppress alignments at lower
  strata.
- Fixed issue with ends of paired-end reads sometimes appearing in non-adjacent
  lines of the SAM output with -p/--threads >1
- Fixed issue whereby the read name of end #2 was not always truncated at the
  first whitespace character
- Code simplifications

* Wed Jun 28 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.2.1.1-1
- Fixed an issue causing Bowtie to segfault when processing reads from stdin
- 1.2.1 - 06/12/2017
  - Please note that Bowtie will be switching to the Artistic 2.0 license in
    the next release. Pre-build binaries now include statically linked TBB and
    zlib libraries no longer requiring
  - Fixed an issue which caused Bowtie to hang during parallell index building
    when running an optimized binary
  - Deprecated --refout option. It will be fully removed in the next release
  - Added parallel index building with the bowtie2-build --threads option
    (credit to Aidan Reilly)
  - Added native support for gzipped read files. The wrapper script is no
    longer responsible for this, which simplifies the wrapper and improves
    speed and thread scaling.
  - Added support for interleaved paired-end FASTQ inputs (--interleaved)
  - Fixed issue where first character of some read names was omitted from SAM
    output when using tabbed input formats
  - Fixed issue that caused Bowtie to hang when aligning FASTA inputs with more
    than one thread
  - Bowtie wrapper now works even when invoked via a symlink in a different
    directory from the executables
  - Fixed issue preventing reading --12 input on stdin
  - Added --no-unal option for suppressing unmapped reads in SAM output
- 1.2.0 - 12/12/2016
  - This is a major release with some larger and many smaller changes. These
    notes emphasize the large changes. See commit history for details.
  - Code related to read parsing was completely rewritten to improve
    scalability to many threads. In short, the critical section is simpler and
    parses input reads in batches rather than one at a time. The improvement
    applies to all read formats.
  - --reads-per-batch command line parameter added to specify the number of
    reads to read from the input file at once
  - TBB is now the default threading library. We consistently found TBB to give
    superior thread scaling. It is widely available and widely installed. That
    said, we are also preserving a "legacy" version of Bowtie that, like
    previous releases, does not use TBB. To compile Bowtie source in legacy
    mode use NO_TBB=1. To use legacy binaries, download the appropriate binary
    archive with "legacy" in the name.
  - Bowtie now uses a queue-based lock rather than a spin or heavyweight lock.
    We find this gives superior thread scaling; we saw an order-of-magnitude
    throughput improvements at 120 threads in one experiment, for example.
  - Unnecessary thread synchronization removed
  - Fixed colorspace parsing when primer base is present
  - Fixed bugs related to --skip command line option
