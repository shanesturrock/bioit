%define priority 217
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		stringtie
Version:	2.1.7
Release:	1%{?dist}
Summary:	StringTie is a fast and highly efficient assembler of RNA-Seq alignments into potential transcripts.
Group:		Applications/Engineering
License:	Artistic 2.0
URL:		https://ccb.jhu.edu/software/stringtie/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives
Obsoletes:	stringtie

%description

StringTie is a fast and highly efficient assembler of RNA-Seq alignments into
potential transcripts. It uses a novel network flow algorithm as well as an
optional de novo assembly step to assemble and quantitate full-length
transcripts representing multiple splice variants for each gene locus. Its
input can include not only the alignments of raw reads used by other transcript
assemblers, but also alignments longer sequences that have been assembled from
those reads.In order to identify differentially expressed genes between
experiments, StringTie's output can be processed by specialized software like
Ballgown, Cuffdiff or other programs (DESeq2, edgeR, etc.).

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/stringtie stringtie /opt/bioit/%{name}/%{version}/stringtie %{priority} 

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove stringtie /opt/bioit/%{name}/%{version}/stringtie
fi

%files

%changelog
* Thu Jul 08 2021 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.7-1
- 2.1.6
  - new --mix option added to use both short and long read alignments; when
    this option is used, the 2nd .bam file in the command line is expected to
    be a long reads alignment file (the 1st being the short-reads alignment
    file); -L option should not be used in this case.
- 2.1.7
  - fix an occasional bug (crash) when --mix option was used

* Fri Mar 12 2021 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.5-1
- Bug fixes

* Fri Aug 21 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.4-1
- 2.1.4
 - Bugfix release
- 2.1.3
  - added the --viral option for long reads from viral data where splice sites
    do not follow consensus
  - adjustments to the assembly of long read alignment data
  - fixed an occasional issue with the --merge option
  - made the -e compatible with long reads (-L option)

* Fri May 08 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.2-1
- added --ptf option for loading point-feature data (TSA, CPAS)
- improve accuracy of assemblies from long read alignments

* Fri Jan 31 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.1-1
- fixed small bug in trimming procedure
- resolved rlink.cpp merge conflict

* Fri Jan 24 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.0.6-1
- bugfix release for StringTie v2

* Fri Dec 13 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.0.5-1
- Bugfix release

* Fri Nov 01 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.0.4-1
- Bugfix release

* Fri Sep 20 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.0.3-1
- Bugfix release

* Fri Aug 02 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.0-1
- added support for long read alignments (enabled with -L option)
- added a new "super-reads" module (found in the SuperReads_RNA directory of
  the source distribution) which can be used to perform de-novo assembly and
  alignment of RNA-Seq reads preparing them for assembly with StringTie
- overall improved handling of read alignments and their transcription strand
  assignment

* Fri May 10 2019 Shane Sturrock <shane.sturrock@gmail.com> - 1.3.6-1
- fixing a GFF/GTF sorting issue causing occasional errors when the --merge
  option was used
- addressing a float precision problem causing negative coverage/TPM/FPKM
  values in some cases
- various GFF/GTF parsing adjustments improving support for some reference
  annotation sources

* Fri Nov 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.3.5-1
- spliced alignments produced by minimap2 (in SAM format) are now supported;
  there is no need to pre-process them in order to add the XS tag, the cs tag
  is recognized as an alternative. Note: sorting of the SAM/BAM file is still
  required!
- the default value for the -M option (maximum multi-mapping fraction) is now
  set to 1.0, such that transcripts assembled from only multi-mapped reads are
  no longer excluded (e.g. in case of multiple gene copies).
- read alignments not having a transcription strand assigned (generally
  unspliced mappings) can be now automatically assigned the strand of the
  overlaping reference (guide) transcript, if any such overlap exists.

* Fri Mar 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.3.4d-1
- No changes listed

* Thu Feb 22 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.3.4c-1
- No changes listed

* Tue Feb 13 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.3.4b-1
- No changes listed

* Tue Oct 31 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.3.3b-1
- fixed the computation of the TPM value that was reported incorrectly somtimes
  in the presence of guides (-G option)
- few other minor fixes
