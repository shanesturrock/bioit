%define priority 0115
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		FastQC
Version:	0.11.5
Release:	1%{?dist}
Summary:	A quality control application for high throughput sequence data
Group:		Applications/Engineering
License:	GPLv3
URL:		http://www.bioinformatics.babraham.ac.uk/projects/%{name}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
* Wed Jun 28 2017 Shane Sturrock <shane.sturrock@gmail.com> - 0.11.5-1
- Fixed the smallRNA adapter sequence so that abundance isn't under-represented
  in the adapter content plot
- Fixed a bug in the warn / error code for the per-base sequence content plot
- Fixed a typo in the documentation for the duplication plot
