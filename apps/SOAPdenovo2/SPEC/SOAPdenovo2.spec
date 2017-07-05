%define priority 241
%define dir_exists() (if [ ! -d /opt/biology/%{name}/%{version} ]; then \
  echo "/opt/biology/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		SOAPdenovo2
Version:	241
Release:	1%{?dist}
Summary:	SOAPdenovo is a novel short-read assembly method
Group:		Applications/Engineering
License:	GPL
URL:		http://soap.genomics.org.cn/soapdenovo.htm
BuildRoot:	%{_tmppath}/%{name}-2.04-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
SOAPdenovo is a novel short-read assembly method that can build a de novo 
draft assembly for the human-sized genomes. The program is specially designed 
to assemble Illumina GA short reads. It creates new opportunities for building 
reference sequences and carrying out accurate analyses of unexplored genomes 
in a cost effective way.  

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/SOAPdenovo-127mer SOAPdenovo2 /opt/biology/%{name}/%{version}/SOAPdenovo-127mer %{priority} \
   --slave %{_bindir}/SOAPdenovo-63mer SOAPdenovo-63mer /opt/biology/%{name}/%{version}/SOAPdenovo-63mer \
   --slave %{_bindir}/SOAPdenovo-fusion SOAPdenovo-fusion /opt/biology/%{name}/%{version}/SOAPdenovo-fusion

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove SOAPdenovo2 /opt/biology/%{name}/%{version}/SOAPdenovo-127mer
fi

%files

%changelog
* Wed Jun 28 2017 Shane Sturrock <shane.sturrock@gmail.com> - r240
- Added a scaffolding preparation module.
