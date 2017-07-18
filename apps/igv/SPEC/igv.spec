%define priority 2397
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		igv
Version:	2.3.97
Release:	1%{?dist}
Summary:	Integrative Genomics Viewer
Group:		Applications/Engineering
License:	LGPL
URL:		http://www.broadinstitute.org/igv/home
Source0:	igv.desktop
Source1:	igv-icons.tar.gz
Patch0:		about.properties.patch
Requires:	java-1.8.0 dejavu-sans-fonts dejavu-sans-mono-fonts dejavu-serif-fonts
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Integrative Genomics Viewer (IGV) is a high-performance visualization tool 
for interactive exploration of large, integrated genomic datasets. It supports 
a wide variety of data types, including array-based and next-generation 
sequence data, and genomic annotations.

%pre
%dir_exists

%install
rm -rf %{buildroot}
# .desktop
mkdir -p %{buildroot}%{_datadir}/applications/
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/applications/
# Icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/
tar xf %{SOURCE1} -C %{buildroot}%{_datadir}/icons/hicolor/

%clean
rm -rf %{buildroot}

%post
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --quiet /usr/share/icons/hicolor
fi
alternatives \
   --install %{_bindir}/igv igv /opt/bioit/%{name}/%{version}/igv %{priority}

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove igv /opt/bioit/%{name}/%{version}/igv
fi

%files
%defattr(-,root,root,-)
/usr/share/icons/hicolor/*
/usr/share/applications/igv.desktop

%changelog
* Wed Jul 19 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.97-1
- Fix for track name bug
- Fix sequence bug
- Update chrom.sizes
