%define priority 1210
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		velvet
Version:	1.2.10
Release:	1%{?dist}
Summary:	Sequence assembler for very short reads
Group:		Applications/Engineering
License:	GPLv3
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	samtools
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
Velvet is a de novo genomic assembler specially designed for short read
sequencing technologies, such as Solexa or 454, developed by Daniel Zerbino and
Ewan Birney at the European Bioinformatics Institute (EMBL-EBI), near
Cambridge, in the United Kingdom.

Velvet currently takes in short read sequences, removes errors then produces
high quality unique contigs. It then uses paired-end read and long read
information, when available, to retrieve the repeated areas between contigs.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/velveth velveth /opt/bioit/%{name}/%{version}/velveth %{priority} \
   --slave %{_bindir}/velvetg velvetg /opt/bioit/%{name}/%{version}/velvetg

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove velveth /opt/bioit/%{name}/%{version}/velveth
fi

%files

%changelog
* Wed Aug 16 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.2.10-1
- Bug in multi k-mer run
- Addition of contributed 'read_prepare' script
- Better detection of out-of-bounds error
