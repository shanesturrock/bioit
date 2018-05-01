%define priority 43
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		nxtrim
Version:	0.4.3
Release:	1%{?dist}
Summary:	Tool for trimming Illumina Nextera MP Libraries
Group:		Applications/Engineering
License:	BSD
URL:		https://github.com/sequencing/NxTrim
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
Adapter trimming and virtual library creation for Illumina Nextera Mate Pair
libraries.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/nxtrim nxtrim /opt/bioit/%{name}/%{version}/nxtrim %{priority}

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove nxtrim /opt/bioit/%{name}/%{version}/nxtrim
fi


%files

%changelog
* Wed May 02 2018 Shane Sturrock <shane.sturrock@gmail.com> 0.4.3-1
- fixed a bad bug where a partial-but-perfect adapter match exact at the end of
  a read could be missed
- improved logging and error checking
