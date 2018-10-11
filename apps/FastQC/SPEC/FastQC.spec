%define priority 118
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		FastQC
Version:	0.11.8
Release:	1%{?dist}
Summary:	A quality control application for high throughput sequence data
Group:		Applications/Engineering
License:	GPLv3
URL:		http://www.bioinformatics.babraham.ac.uk/projects/%{name}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
FastQC aims to provide a simple way to do some quality control checks on raw
sequence data coming from high throughput sequencing pipelines. It provides a
modular set of analyses which you can use to give a quick impression of whether
your data has any problems of which you should be aware before doing any
further analysis.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/fastqc FastQC /opt/bioit/%{name}/%{version}/fastqc %{priority}

%postun
if [ $1 -eq 0 ] 
then
  alternatives \
   --remove FastQC /opt/bioit/%{name}/%{version}/fastqc
fi

%files

%changelog
* Fri Oct 12 2018 Shane Sturrock <shane.sturrock@gmail.com> - 0.11.8-1
- Fixed a performance bug in highly duplicated sequences
- Changed the behaviour of the sequence length module when run with --nogroup
- Other minor bug fixes

* Thu Jan 11 2018 Shane Sturrock <shane.sturrock@gmail.com> - 0.11.7-1
- Fixed a crash if the first sequence in a file was shorter than 12bp

* Tue Jan 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 0.11.6-1
- Disabled the Kmer plot by default
- Fixed a bug when long custom adapters were being used
- Changed the tile number cutoff to accommodate the novaseq
- Fixed various format changes in nanopore data from ONT
- Added new Clontech sequences to the contaminant list
- Added a --min-length option to remove short sequences
- Added an option to specify the output name of data streamed into the program

* Wed Jun 28 2017 Shane Sturrock <shane.sturrock@gmail.com> - 0.11.5-1
- Fixed the smallRNA adapter sequence so that abundance isn't under-represented
  in the adapter content plot
- Fixed a bug in the warn / error code for the per-base sequence content plot
- Fixed a typo in the documentation for the duplication plot
