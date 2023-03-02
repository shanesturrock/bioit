%define priority 121
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		FastQC
Version:	0.12.1
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
* Thu Mar 02 2023 Shane Sturrock <shane.sturrock@gmail.com> - 0.12.1-1
- 0.12.1
  - Fix a bug in file type detection on OSX
- 0.12.0
  - Add total base count to basic stats
  - Add dup_length option to set the level of truncation for duplicate finding
  - Make default truncation length always 50bp
  - Removed the deduplicated duplication line from the duplicate plot
  - Improve memory handling and add a --memory option to the command line
  - Move BAM parsing to htsjdk
  - Make colours colourblind friendly
  - Generate SVG versions of graphs, and add a --svg option to use these in the
    report
  - Add line numbers to parsing errors
  - Change the default adapter sequences to search

* Fri Jan 17 2020 Shane Sturrock <shane.sturrock@gmail.com> - 0.11.9-1
- We removed the native look and feel from the linux application since it's
  horribly broken
- Fixed a hang if a run terminated from an out-of-memory error
- Bundle a suitable JRE with the OSX app build
- Fixed a corner case where adapters could occasionally be double-counted
- Updated the fast5 parser to account for the newer format multi-read oxford
  nanopore fast5 files
- Fixed problems if analysing a completely blank file

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
