%define priority 182
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bismark
Version:	0.18.2
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
* Wed Aug 16 2017 Shane Sturrock <shane.sturrock@gmail.com> - 0.18.2-1
- Bismark
  - Changed the timing of when ambiguous within same thread alignments are
    reset. Previously some alignments were incorrectly considered ambiguous
    (see here). This affected Bowtie 2 alignments only.
- bismark2bedGraph
  - The option --ample_mem is now mutually exclusive with specifying memory for
    the UNIX sort command via the option --buffer_size.
