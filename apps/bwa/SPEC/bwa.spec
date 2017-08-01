%define priority 0716
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:           bwa
Version:        0.7.16a
Release:        1%{?dist}
Summary:        Burrows-Wheeler Alignment tool
Group:          Applications/Engineering
License:        GPLv3
URL:            http://bio-bwa.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description

BWA is a program for aligning sequencing reads against a large
reference genome (e.g. human genome). It has two major components, one
for read shorter than 150bp and the other for longer reads.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/bwa bwa /opt/bioit/%{name}/%{version}/bin/bwa %{priority} \
   --slave %{_bindir}/qualfa2fq.pl qualfa2fq.pl /opt/bioit/%{name}/%{version}/bin/qualfa2fq.pl \
   --slave %{_bindir}/xa2multi.pl xa2multi.pl /opt/bioit/%{name}/%{version}/bin/xa2multi.pl \
   --slave %{_mandir}/man1/bwa.1 bwa.1 /opt/bioit/%{name}/%{version}/man/man1/bwa.1 

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bwa /opt/bioit/%{name}/%{version}/bin/bwa
fi

%files

%changelog
* Tue Aug 01 2017 Shane Sturrock <shane.sturrock@gmail.com> - 0.7.16a-1
- This release added a couple of minor features and incorporated multiple pull
  requests, including:
  - Added option -5, which is useful to some Hi-C pipelines.
  - Fixed an error with samtools sorting (#129). Updated download link for
    GRCh38 (#123). Fixed README MarkDown formatting (#70). Addressed multiple
    issues via a collected pull request #139 by @jmarshall. Avoid malformatted
    SAM header when -R is used with TAB (#84). Output mate CIGAR (#138).

* Wed Jun 28 2017 Shane Sturrock <shane.sturrock@gmail.com> - 0.7.15-1
- Fixed a long existing bug which potentially leads underestimated insert size
  upper bound. This bug should have little effect in practice.
- In the ALT mapping mode, this release adds the "AH:*" header tag to SQ lines
  corresponding to alternate haplotypes.
