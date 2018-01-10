%define priority 384
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		rtg-tools
Version:	3.8.4
Release:	1%{?dist}
Summary:	Utilities for accurate VCF comparison and manipulation
Group:		Applications/Engineering
License:	Simplified BSD
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
RTG Tools includes several useful utilities for dealing with VCF files and
sequence data, but probably the most interesting is the vcfeval command which
performs sophisticated comparison of VCF files.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/rtg-tools %{name} /opt/bioit/%{name}/%{version}/rtg %{priority}

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove %{name} /opt/bioit/%{name}/%{version}/rtg-tools
fi

%files

%changelog
* Thu Jan 11 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.8.4-1
- RTG Core 3.8.4 (2017-09-08)
- This release primarily includes bugfixes and minor improvements:
  - vcfeval: Explicitly warn when the ROC score field does not exist in
    the VCF header, to help in cases where the user has mixed up INFO vs
    FORMAT field names.
  - vcfeval: Fix an exception that could occur when processing VCFs with
    GT ploidy >= 3.
  - format: When formatting FASTA (both DNA and protein), suppress
    warnings about "unexpected symbols" produced by genuine IUPAC
    ambiguity codes.
  - misc: Detect invalid VCF records containing duplicate INFO or FORMAT
    fields.
  - misc: Improved detection of invalid REF/ALT fields in input VCF files,
    allowing clearer exception messages.
  - misc: Fix incorrect detection of network stats capability during local
    run monitoring.
  - misc: Bash command completion now also works if rtg is symlinked as
    rtg-tools or rtg-core, to improve convenience when both are
    installed. (See the bash completion script if you have alternative
    RTG executable names for which you want to enable the completion)
- RTG Core 3.8.3 (2017-08-02)
- This release primarily includes bugfixes and minor improvements:
  - rocplot: (GUI) Improvements to graph zooming, to allow stepping back
    to previous zoom levels as well as fully un-zooming.
  - rocplot: Improve the automatic curve naming heuristic to ignore
    directory name suffixes like "-eval", ".vcfeval" etc, and similar
    prefixes.
  - rocplot: Enable text antialiasing in GUI and PNG output.
  - vcfeval: More graceful handling of input VCFs containing REF values
    that are not valid according to VCF specifications.
  - vcfmerge/vcfeval: Normalize the casing of nucleotides in REF/ALT,
    which permits merging records where the REF/ALT differ in casing.
  - vcffilter: Graceful error handling of a new category of invalid
    javascript expression.
  - vcfsubset: Don't complain when using --keep-filter/--remove-filter
    flags with "PASS" and the VCF header doesn't contain a declaration for
    that filter.
  - misc: Prevent a unit test failure when running on newer versions of
    Ubuntu.
