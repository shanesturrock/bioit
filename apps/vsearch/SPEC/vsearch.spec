%define priority 2111
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		vsearch
Version:	2.11.1
Release:	1%{?dist}
Summary:	An alternative to the USEARCH
Group:		Applications/Engineering
License:	GPLv3 
URL:		https://github.com/torognes/vsearch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
VSEARCH stands for vectorized search, as the tool takes advantage of
parallelism in the form of SIMD vectorization as well as multiple threads to
perform accurate alignments at high speed. VSEARCH uses an optimal global
aligner (full dynamic programming Needleman-Wunsch), in contrast to USEARCH
which by default uses a heuristic seed and extend aligner. This results in more
accurate alignments and overall improved sensitivity (recall) with VSEARCH,
especially for alignments with gaps.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/vsearch vsearch /opt/bioit/%{name}/%{version}/bin/vsearch %{priority} \
   --slave %{_mandir}/man1/vsearch.1 vsearch.1 /opt/bioit/%{name}/%{version}/share/man/man1/vsearch.1

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove vsearch /opt/bioit/%{name}/%{version}/bin/vsearch
fi

%files

%changelog
* Fri Mar 01 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.11.1-1
- Minor change to the handling of the weak_id and id options when using
  cluster_unoise.

* Fri Feb 15 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.11.0-1
- Added ability to trim and filter paired-end reads using the reverse option
  with the fastx_filter and fastq_filter commands. 
- Added xee option to remove ee attributes from FASTA headers. Minor invisible
  improvement to the progress indicator.

* Fri Jan 11 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.4-1
- Fixed serious bug in x86_64 SIMD alignment code introduced in version 2.10.3.
- Added link to BioConda in README.
- Fixed bug in fastq_stats with sequence length 1.
- Fixed use of equals symbol in UC files for identical sequences with
  cluster_fast.

* Fri Dec 21 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.3-1
- Support for 64-bit ARMv8 systems.
- Fix gcc 8 warning.

* Fri Dec 14 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.2-1
- Improved sff_convert command. It will now read several variants of the SFF
  format. It is also able to read from a pipe. Warnings are given if there are
  minor problems. Errors messages have been improved. Minor speed and memory
  usage improvements.
- Fix bug in syntax with reversed order of domain and kingdom.

* Fri Dec 07 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.0-1
- Added the sff_convert command to convert SFF files to FASTQ

* Fri Oct 12 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.9.0-1
- 2.8.5
  - Fix bug with fastq_eestats2.
- 2.8.6
  - Fixed bug in derep_fulllength causing headers not to be truncated after the first space. This bug was unfortunately introduced in version 2.8.2.
- 2.9.0
  - Added the fastq_join command.

* Fri Sep 07 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.8.4-1
- Fix for segfault bug with derep_fulllength and uc.
- Further reduce memory requirements for dereplication when not using the uc
  option. 
- Fix output during subsampling when quiet or log options are in effect.

* Fri Aug 24 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.8.2-1
- Fix for wrong placement of semicolons in header lines in some cases when
  using the sizeout or xsize options.
- Reduced memory requirements for full-length dereplication in cases with many
  duplicate sequences.
- Improved wording of fastq_mergepairs report.
- Updated manual regarding use of sizein and sizeout with dereplication.
- Changed a compiler option.

* Fri Jun 29 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.8.1-1
- Fixes for compilation warnings with GCC 8.

* Fri Apr 27 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.8.0-1
- Added fastq_maxdiffpct option.

* Thu Feb 22 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.7.1-1
- 2.7.0
  - Added cluster_unoise, uchime2_denovo and uchime3_denovo commands.
- 2.7.1
  - Fixes several bugs on Windows.

* Tue Jan 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.6.2-1
- Fix for partially inactive xsize option.

* Tue Dec 12 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.6.1-1
- Improved parallelisation of paired end reads merging

* Tue Nov 14 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.6.0-1
- Rewritten paired-end reads merger with improved accuracy. 
- Decreased default value for fastq_minovlen option from 16 to 10. 
- The default value for the fastq_maxdiffs option is increased from 5 to 10. 
- There are now other more important restrictions that will avoid merging reads
  that cannot be reliably aligned.

* Tue Oct 31 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.5.2-1
- Fix bug with '-' not treated as stdin when used as argument to fastq_eestats2
  option.

