%define priority 260
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		ncbi-blast
Version:	2.6.0+
Release:	1%{?dist}
Summary:	BLAST+ is a suite of command-line tools to run BLAST
Group:		Applications/Engineering
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
BLAST+ is a suite of command-line tools to run BLAST. For details, please see
the BLAST+ user manual, the BLAST Help manual, the BLAST releases notes, and
the article in BMC Bioinformatics. BLAST+ is the most current version of BLAST
and is the only supported version.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/blastp %{name} /opt/bioit/%{name}/%{version}/bin/blastp %{priority} \
   --slave %{_bindir}/blastdb_aliastool blastdb_aliastool /opt/bioit/%{name}/%{version}/bin/blastdb_aliastool \
   --slave %{_bindir}/blastdbcheck blastdbcheck /opt/bioit/%{name}/%{version}/bin/blastdbcheck \
   --slave %{_bindir}/blastdbcmd blastdbcmd /opt/bioit/%{name}/%{version}/bin/blastdbcmd \
   --slave %{_bindir}/blast_formatter blast_formatter /opt/bioit/%{name}/%{version}/bin/blast_formatter \
   --slave %{_bindir}/blastn blastn /opt/bioit/%{name}/%{version}/bin/blastn \
   --slave %{_bindir}/blastx blastx /opt/bioit/%{name}/%{version}/bin/blastx \
   --slave %{_bindir}/convert2blastmask convert2blastmask /opt/bioit/%{name}/%{version}/bin/convert2blastmask \
   --slave %{_bindir}/deltablast deltablast /opt/bioit/%{name}/%{version}/bin/deltablast \
   --slave %{_bindir}/dustmasker dustmasker /opt/bioit/%{name}/%{version}/bin/dustmasker \
   --slave %{_bindir}/legacy_blast.pl legacy_blast.pl /opt/bioit/%{name}/%{version}/bin/legacy_blast.pl \
   --slave %{_bindir}/makeblastdb makeblastdb /opt/bioit/%{name}/%{version}/bin/makeblastdb \
   --slave %{_bindir}/makembindex makembindex /opt/bioit/%{name}/%{version}/bin/makembindex \
   --slave %{_bindir}/makeprofiledb makeprofiledb /opt/bioit/%{name}/%{version}/bin/makeprofiledb \
   --slave %{_bindir}/psiblast psiblast /opt/bioit/%{name}/%{version}/bin/psiblast \
   --slave %{_bindir}/rpsblast rpsblast /opt/bioit/%{name}/%{version}/bin/rpsblast  \
   --slave %{_bindir}/rpstblastn rpstblastn /opt/bioit/%{name}/%{version}/bin/rpstblastn \
   --slave %{_bindir}/segmasker segmasker /opt/bioit/%{name}/%{version}/bin/segmasker \
   --slave %{_bindir}/tblastn tblastn /opt/bioit/%{name}/%{version}/bin/tblastn \
   --slave %{_bindir}/tblastx tblastx /opt/bioit/%{name}/%{version}/bin/tblastx \
   --slave %{_bindir}/update_blastdb.pl update_blastdb.pl /opt/bioit/%{name}/%{version}/bin/update_blastdb.pl \
   --slave %{_bindir}/windowmasker windowmasker /opt/bioit/%{name}/%{version}/bin/windowmasker

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove %{name} /opt/bioit/%{name}/%{version}/bin/blastp
fi

%files

%changelog
* Tue Jun 27 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.6.0+-1
- New features
  - Handle bare accessions on blastdb_aliastool.
  - Change defaults for output formats 6, 7, and 10 to incorporate version in
    accessions.
- Improvements
  - Add support for NCBI_DONT_USE_LOCAL_CONFIG and NCBI_DONT_USE_NCBIRC 
    environment variables.
  - Better runtime performance in blastdbcmd when the entry_batch parameter is 
    used.
  - SAM output improvements.
  - Changed gapped alignment starting point to minimize the chance to produce 
    sub-optimal alignments.
  - For custom matrices absent from the util/tables source file, use BLOSUM62 
    for reporting number of positives.
  - Added long_seqids flag to blastdbcmd to use long (legacy) NCBI Seq-id 
    format.
- Bug fixes
  - Fixed issue with missing alignments in blastx.
  - Fixed problem processing accession.version in makeblastdb.
  - Fixed blastdbcmd problem with local IDs.
  - Removed memory leak for multi-threaded runs.
  - Fixed blastdbcmd crash when listing all entries and a sequence has no title.
