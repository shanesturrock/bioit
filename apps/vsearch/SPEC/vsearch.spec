%define priority 2150
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		vsearch
Version:	2.15.0
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
* Fri Jul 31 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.15.0-1
- Update manual and documentation.
- Turn on notrunclabels option for sintax command by default.
- Change maxhits 0 to mean unlimited hits, like the default.
- Allow non-ascii characters in headers, with a warning.
- Sort centroids and uc too when clusterout_sort specified.
- Add cluster id to centroids output when clusterout_id specified.
- Improve error messages when parsing FASTQ files.
- Add missing fastq_qminout option and fix label_suffix option for
  fastq_mergepairs.
- Add derep_id command that dereplicates based on both label and sequence. 
- Remove compilation warnings.

* Fri Jan 31 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.14.2-1
- Fixed some issues with the cut, fastx_revcomp, fastq_convert,
  fastq_mergepairs, and makeudb_usearch commands. 
- Updated manual.

* Fri Sep 20 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.14.1-1
- Fixed bug with sequences written to file specified with fastaout_rev for
  commands fastx_filter and fastq_filter.

* Fri Sep 13 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.14.0-1
- 2.14.0
  - Added relabel_self option. Added fasta_width, sizein, sizeout and
    relabelling options as valid for certain commands.
- 2.13.7
  - Fixes a bug when generating consensus sequences.

* Fri Jul 05 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.13.6-1
- 2.13.5
  - Added cut command to fragment sequences at restriction sites.
  - Silenced output from the fastq_stats command if quiet option was given.
  - Updated manual.
- 2.13.6
  - Added info about the cut command to the output of the help command.

* Fri May 17 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.13.4-1
- Added information about support for gzip- and bzip2-compressed input files to
  the output of the version command. 
- Adapted source code for compilation on FreeBSD and NetBSD systems.

* Fri May 03 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.13.3-1
- 2.13.3
  - Fix bug in FASTQ parsing introduced in version 2.13.2.
- 2.13.2
  - Fix to print error message to log file not stderr
- 2.13.1
  - Minor changes to the allowed options for each command. All commands now
    allow the log, quiet and threads options. If more than 1 thread is
    specified for commands that are not multi-threaded, a warning will be 
    issued.
  - Minor changes to the manual.

* Fri Apr 12 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.13.0-1
- Added the fastx_getseq, fastx_getseqs and fastx_getsubseq commands to extract
  sequences from a FASTA or FASTQ file based on their labels.
- Improved handling of ambiguous nucleotide symbols.
- Corrected behaviour of uchime_ref command with and options self and selfid.
  Strict detection of illegal options for each command.

* Fri Mar 22 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.12.0-1
- Take sequence abundance into account when computing consensus sequences or
  profiles after clustering.
- Warn when rereplicating sequences without abundance info.
- Guess offset 33 in more cases with fastq_chars.
- Stricter checking of option arguments and option combinations.

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

