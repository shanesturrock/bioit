%define debug_package %{nil}
%define priority 232
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bowtie2
Version:	2.3.2
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
