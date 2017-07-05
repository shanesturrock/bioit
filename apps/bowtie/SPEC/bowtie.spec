%define priority 1211
%define dir_exists() (if [ ! -d /opt/biology/%{name}/%{version} ]; then \
  echo "/opt/biology/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bowtie
Version:	1.2.1.1
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
   --install %{_bindir}/bowtie bowtie /opt/biology/%{name}/%{version}/bin/bowtie %{priority} \
   --slave %{_bindir}/bowtie-build bowtie-build /opt/biology/%{name}/%{version}/bin/bowtie-build \
   --slave %{_bindir}/bowtie-build-l bowtie-build-l /opt/biology/%{name}/%{version}/bin/bowtie-build-l \
   --slave %{_bindir}/bowtie-build-s bowtie-build-s /opt/biology/%{name}/%{version}/bin/bowtie-build-s \
   --slave %{_bindir}/bowtie-align-l bowtie-align-l /opt/biology/%{name}/%{version}/bin/bowtie-align-l \
   --slave %{_bindir}/bowtie-align-s bowtie-align-s /opt/biology/%{name}/%{version}/bin/bowtie-align-s \
   --slave %{_bindir}/bowtie-inspect-l bowtie-inspect-l /opt/biology/%{name}/%{version}/bin/bowtie-inspect-l \
   --slave %{_bindir}/bowtie-inspect-s bowtie-inspect-s /opt/biology/%{name}/%{version}/bin/bowtie-inspect-s \
   --slave %{_bindir}/bowtie-inspect bowtie-inspect /opt/biology/%{name}/%{version}/bin/bowtie-inspect

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bowtie /opt/biology/%{name}/%{version}/bin/bowtie
fi

%files

%changelog
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
