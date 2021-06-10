%define priority 3172
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		SolexaQA++
Version:	3.1.7.2
Release:	1%{?dist}
Summary:	Calculates quality statistics and creates visual representations of data quality from FASTQ files.
Group:		Applications/Engineering
License:	GPLv3
URL:		http://solexaqa.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
SolexaQA is a Perl-based software package that calculates quality statistics 
and creates visual representations of data quality from FASTQ files generated 
by Illumina second-generation sequencing technology (“Solexa”).

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/SolexaQA++ SolexaQA++ /opt/bioit/%{name}/%{version}/SolexaQA++ %{priority}

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove SolexaQA++ /opt/bioit/%{name}/%{version}/SolexaQA++
fi

%files

%changelog
* Fri Jun 11 2021 Shane Sturrock <shane.sturrock@gmail.com> - 3.1.7.2-1
- Minor bugfixes

* Tue Jun 27 2017 Shane Sturrock <shane.sturrock@gmail.com> - 3.1.7.1-1
- Bugfix for high-output NextSeq runs
- minor bugfixes.
