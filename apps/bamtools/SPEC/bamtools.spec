%define priority 241
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bamtools
Version:	2.4.1
Release:	1%{?dist}
Summary:	Tools for handing BAM files
Group:		Applications/Engineering
License:	MIT
URL:		https://github.com/pezmaster31/bamtools
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
BamTools provides both a programmer's API and an end-user's toolkit for handling
BAM files.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/bamtools bamtools /opt/bioit/%{name}/%{version}/bin/bamtools %{priority}

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove bamtools /opt/bioit/%{name}/%{version}/bin/bamtools
fi


%files

%changelog
* Tue Jun 27 2017 Shane Sturrock <shane.sturrock@gmail.com> 2.4.1-1
- Added: list-tag support to 'bamtools split'
- Fixed: various architecture/compiler errors (see commits for specifics)
- Fixed: documentation-related errors
