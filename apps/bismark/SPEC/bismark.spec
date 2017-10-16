%define priority 190
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bismark
Version:	0.19.0
Release:	1%{?dist}
Summary:	A bisulfite read mapper and methylation caller
Group:		Applications/Engineering
License:	GNU GPL v3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description

Bismark is a program to map bisulfite treated sequencing reads to a genome of
interest and perform methylation calls in a single step. The output can be
easily imported into a genome viewer, such as SeqMonk, and enables a researcher
to analyse the methylation levels of their samples straight away.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/bismark bismark /opt/bioit/%{name}/%{version}/bismark %{priority} \
   --slave %{_bindir}/bam2nuc bam2nuc /opt/bioit/%{name}/%{version}/bam2nuc \
   --slave %{_bindir}/bismark2bedGraph bismark2bedGraph /opt/bioit/%{name}/%{version}/bismark2bedGraph \
   --slave %{_bindir}/bismark2report bismark2report /opt/bioit/%{name}/%{version}/bismark2report \
   --slave %{_bindir}/bismark2summary bismark2summary /opt/bioit/%{name}/%{version}/bismark2summary \
   --slave %{_bindir}/bismark_genome_preparation bismark_genome_preparation /opt/bioit/%{name}/%{version}/bismark_genome_preparation \
   --slave %{_bindir}/bismark_methylation_extractor bismark_methylation_extractor /opt/bioit/%{name}/%{version}/bismark_methylation_extractor \
   --slave %{_bindir}/coverage2cytosine coverage2cytosine /opt/bioit/%{name}/%{version}/coverage2cytosine \
   --slave %{_bindir}/deduplicate_bismark deduplicate_bismark /opt/bioit/%{name}/%{version}/deduplicate_bismark \
   --slave %{_bindir}/filter_non_conversion filter_non_conversion /opt/bioit/%{name}/%{version}/filter_non_conversion \
   --slave %{_bindir}/NOMe_filtering NOMe_filtering /opt/bioit/%{name}/%{version}/NOMe_filtering

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bismark /opt/bioit/%{name}/%{version}/bismark
fi

%files

%changelog
* Tue Oct 17 2017 Shane Sturrock <shane.sturrock@gmail.com> - 0.19.0-1
- Bismark
  - Changed the methylation call behaviour so that insertions in a read (which
    are filled in with X for the methylation call) are also considered as
    Unknown context for the methylation call. Here is issue #135.
- filter_non_conversion
  - Added new options --percentage_cutoff [int] and --minimum_count [int] to
    allow filtering reads for non-bisulfite conversion using an overall
    methylation percentage and count cutoff. Here is issue #122.
- deduplicate_bismark
  - Added option --multiple to the deduplicator to treat several input SAM/BAM
    files as the same sample. Here is issue #107.
  - Added option --output_dir to deduplicate_bismark so that it can be used in
    the Google cloud. Here is issue #123
- coverage2cytosine
  - Output files are now handled better and more consistently. Default
    processing now produces the following output files (with --gzip):
        CpG_report.txt(.gz) or
        CX_report.txt(.gz)
  - The option --NOMe-Seq now produces four output files (with --gzip):
        NOMe.CpG_report.txt(.gz)
        NOMe.CpG.cov(.gz)
        NOMe.GpC_report.txt(.gz)
        NOMe.GpC.cov(.gz)
  - The option --split_by_chromosome should work in either default, --gc or
    --NOMe-seq mode.
  - NOMe-Seq processing if now ignoring processing that were not covered by any
    reads.
  - Improved handling of the --output_dir, i.e. the folder will be created if
    it doesn't exist already and making the path absolute.
  - Added new option --discordance <int> to allow filtering for discordance pf
    top and bottom strand when in --merge_CpG mode. CpG positions for which
    either the top or bottom strand was not measured at all will not be assessed
    for discordance and hence appear in the regular 'merged_CpG_evidence.cov' 
    file.  More details in issue #91.
  - Fixed context extraction for Gs at positions 1 and 2 of a
    chromosome/contig. Also, last cytosine positions of not covered chromosomes
    are now ignored in the same way as for covered chromosomes issue #127

- copy_files_for_release
  - Is now working from any location.
* Wed Aug 16 2017 Shane Sturrock <shane.sturrock@gmail.com> - 0.18.2-1
- Bismark
  - Changed the timing of when ambiguous within same thread alignments are
    reset. Previously some alignments were incorrectly considered ambiguous
    (see here). This affected Bowtie 2 alignments only.
- bismark2bedGraph
  - The option --ample_mem is now mutually exclusive with specifying memory for
    the UNIX sort command via the option --buffer_size.
