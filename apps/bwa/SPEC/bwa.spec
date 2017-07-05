%define priority 0715
%define dir_exists() (if [ ! -d /opt/biology/%{name}/%{version} ]; then \
  echo "/opt/biology/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:           bwa
Version:        0.7.15
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
   --install %{_bindir}/bwa bwa /opt/biology/%{name}/%{version}/bin/bwa %{priority} \
   --slave %{_bindir}/qualfa2fq.pl qualfa2fq.pl /opt/biology/%{name}/%{version}/bin/qualfa2fq.pl \
   --slave %{_bindir}/xa2multi.pl xa2multi.pl /opt/biology/%{name}/%{version}/bin/xa2multi.pl \
   --slave %{_mandir}/man1/bwa.1 bwa.1 /opt/biology/%{name}/%{version}/man/man1/bwa.1 

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bwa /opt/biology/%{name}/%{version}/bin/bwa
fi

%files

%changelog
* Wed Jun 28 2017 Shane Sturrock <shane.sturrock@gmail.com> - 0.7.15-1
- Fixed a long existing bug which potentially leads underestimated insert size
  upper bound. This bug should have little effect in practice.
- In the ALT mapping mode, this release adds the "AH:*" header tag to SQ lines
  corresponding to alternate haplotypes.
