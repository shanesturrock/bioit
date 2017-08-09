%define priority 104807
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		ea-utils
Version:	1.04.807
Release:	1%{?dist}
Summary:	Command-line tools for processing biological sequencing data.
Group:		Applications/Engineering
License:	MIT
URL:		https://expressionanalysis.github.io/ea-utils/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description

Command-line tools for processing biological sequencing data. Barcode
demultiplexing, adapter trimming, etc. Primarily written to support an Illumina
based pipeline - but should work with any FASTQs.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/alc ea-utils /opt/bioit/%{name}/%{version}/alc %{priority} \
   --slave %{_bindir}/determine-phred determine-phred /opt/bioit/%{name}/%{version}/determine-phred \
   --slave %{_bindir}/fastq-clipper fastq-clipper /opt/bioit/%{name}/%{version}/fastq-clipper \
   --slave %{_bindir}/fastq-join fastq-join /opt/bioit/%{name}/%{version}/fastq-join \
   --slave %{_bindir}/fastq-mcf fastq-mcf /opt/bioit/%{name}/%{version}/fastq-mcf \
   --slave %{_bindir}/fastq-multx fastq-multx /opt/bioit/%{name}/%{version}/fastq-multx \
   --slave %{_bindir}/fastq-stats fastq-stats /opt/bioit/%{name}/%{version}/fastq-stats \
   --slave %{_bindir}/fastx-graph fastx-graph /opt/bioit/%{name}/%{version}/fastx-graph \
   --slave %{_bindir}/randomFQ randomFQ /opt/bioit/%{name}/%{version}/randomFQ \
   --slave %{_bindir}/sam-stats sam-stats /opt/bioit/%{name}/%{version}/sam-stats \
   --slave %{_bindir}/varcall varcall /opt/bioit/%{name}/%{version}/varcall

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove ea-utils /opt/bioit/%{name}/%{version}/alc
fi


%files

%changelog
* Thu Aug 10 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.04.807-1
- Initial import
