%define priority 2120
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		ncbi-blast
Version:	2.12.0+
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
* Fri Jul 02 2021 Shane Sturrock <shane.sturrock@gmail.com> - 2.12.0+-1
- New features
  - Threading by query batch (for BLASTN, BLASTP, BLASTX, RPSBLAST, and
    RPSTBLASTN) may more efficiently BLAST large numbers of queries, especially
    if the database is small or the search is limited by taxid. Use "-mt_mode
    1" to enable this option.
  - Makeblastdb requires less virtual memory for smaller databases.
  - Makeprofiledb creates multiple volumes for a CDD database, which allows
    RPSBLAST to handle a larger number of records. The number of SMP files
    included in a volume can be controlled with the new -new_smp_vol option.
  - update_blastdb.pl now supports the "-showall pretty" option for databases
    hosted at the NCBI.
  - update_blastdb.pl now reports the database timestamp in ISO8601 format.
- Bug fixes
  - Fixed phiblast core dump when -subject option is used.
  - Fixed memory leak in setup procedures.

* Fri Nov 06 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.11.0+-1
_ New features
  - Usage reporting - Help improve BLAST by sharing limited information about
    your search. Details on the information collected, how it is used, and how
    to opt-out at https://www.ncbi.nlm.nih.gov/books/NBK563686/
  - Threading by query batch for rpsblast/rpstblast can BLAST large numbers of
    queries faster. For large numbers of queries, use the -mt option to more
    efficiently multi-thread the search.
- Bug fixes
  - Fix slowdown in TBLASTN searches run without composition-based statistics
    on long database sequences.
  - Remove necessity of a network connection for blast_formatter. This also
    speeds up blast_formatter if the database can be found locally.
  - A core dump for RPSBLAST and RPSTBLASTN has been fixed.
  - Makeblastdb for windows has been fixed to not require as much virtual
    memory and to not produce overly large LMDB files.

* Fri Aug 14 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.1+-1
- Bug fixes
  - Fix for TBLASTN Multi-Threading bug.

* Fri Jan 17 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.0+-1
- New features
  - Enhancements to composition-based statistics to ensure the consistency of
    matches if fewer than the default number of matches is selected. Read about
    the details in the “Outline of the BLAST process” section of the BLAST+ user
    manual appendix.
  - Adaptive composition-based statistics may process more sequences in the CBS
    stage of BLAST if many matches have a similar score, increasing the
    likelihood of finding novel results. To enable: set the environment variable
    ADAPTIVE_CBS to 1. This is an experimental feature and your feedback is
    welcome.
  - Default BLAST database version changes:
    - makeblastdb generates BLAST databases in version 5 format.
  - New script to clean up BLAST database volumes (cleanup-blastdb-volumes.py).
  - Add support for genetic code 33 for blastx and rpstblastn.
- Improvements
  - Better error messages for -taxids argument.
  - Consistent error reporting in get_species_taxids.sh to standard error.
- Bug fixes
  - Restore sum statistics (-sum_stat parameter) for BLASTN.
  - Fix Blast-archive generation/ingestion when subject_besthits flag is used.
  - Fix problem with empty lines in files provided to the taxidlist argument.
  - Fix blastdb_aliastool input file size overflow problem.
  - Fix blastdb_aliastool problem in Windows with binary GI list files.
  - Fix search failures using -remote option in BLAST+ 2.9.0.
  - Fix reading from standard input in Windows.
  - Fix missing space in descriptions defline.
  - Fix HTML BLAST report to include version in accession anchors.
  - Fix segmentation fault in tabular BLAST output format when sequences have
    no defline.
  - Fix to prevent generation of local Seq-IDs in Seq-align output format when
    accessions are available.
  - Fix blast_formatter output when searches are limited by taxonomy.

* Fri Apr 05 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.9.0+-1
- New features
  - Support for PDB biopolymer chain identifiers up to four-characters long in
    BLASTDB version 5 (not supported in BLASTDB version 4).
  - Configurable output separator for tabular and CSV output formats (see
    manual entry).
- Improvements
  - Better error messages in get_species_taxids.sh.
  - Fix memory leaks in BLAST libraries and unit tests.
- Bug fixes
  - Fix taxID filtering combined with mask-based alias BLAST databases.
  - Fix ordering of sequence IDs in BLAST report.

* Fri Jan 11 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.8.1+-1
- Improvements
  - A new option (-subject_besthit) culls HSPs on a per subject sequence basis
    by removing HSPs that are completely enveloped by another HSP. This is an
    experimental option and is subject to change.
  - Allow use of the -max_target_seqs option for formats 0-4. The number of
    alignments and descriptions will be set to the max_target_seqs.
  - Issue a warning if -max_target_seqs is set to less than five.
- Bug fixes
  - Disabled an overly aggressive optimization that caused problems mentioned
    by Shah et al. in https://www.ncbi.nlm.nih.gov/pubmed/30247621
  - Fixed an invalid memory error that occurred when composition-based
    statistics and SEG were used.
  - Fixed some memory problems with the culling option.
  - Nucleotide scores for even rewards are no longer rounded down to an even
    number when displayed.
  - Blastdbcmd now reports intervals in the output FASTA if a partial sequence
    is requested with the range option.

* Tue Oct 31 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.7.1+-1
- Improvements
  - Provided an upper limit on the number of threads for BLAST+ search
    applications.
  - Improved performance of taxonomic name lookups.
  - Fixed Mac installers so they are interoperable with other NCBI applications.
  - Reduced the amount of locking in BLASTDB reading library (CSeqDB).
- Bug fixes
  - Fixed race condition when using gilist parameter.
  - Fixed culling_limit bug with HSPs from different strands
  - Fixed dustmasker bug with long region of Ns
  - Fixed bl2seq problem with HTML output

* Tue Oct 17 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.7.0+-1
- Improvements
  - Provided an upper limit on the number of threads for BLAST+ search
    applications.
  - Improved performance of taxonomic name lookups.
  - Fixed Mac installers so they are interoperable with other NCBI
    applications.
  - Reduced the amount of locking in BLASTDB reading library (CSeqDB).
- Bug fixes
  - Fixed race condition when using gilist parameter.
  - Fixed culling_limit bug with HSPs from different strands
  - Fixed dustmasker bug with long region of Ns

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
