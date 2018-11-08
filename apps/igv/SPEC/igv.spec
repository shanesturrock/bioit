%define priority 2415
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		igv
Version:	2.4.15
Release:	1%{?dist}
Summary:	Integrative Genomics Viewer
Group:		Applications/Engineering
License:	LGPL
URL:		http://www.broadinstitute.org/igv/home
Source0:	bioinformatics.menu
Source1:	bioinformatics.directory
Source2:	igv.desktop
Source3:	igv-icons.tar.gz
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
# Menu
mkdir -p %{buildroot}/%{_sysconfdir}/xdg/menus/applications-merged/
install -m 644 %{SOURCE0} %{buildroot}/%{_sysconfdir}/xdg/menus/applications-merged/
mkdir -p %{buildroot}%{_datadir}/desktop-directories/
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/desktop-directories/
# .desktop
mkdir -p %{buildroot}%{_datadir}/applications/
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/applications/
# Icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/
tar xf %{SOURCE3} -C %{buildroot}%{_datadir}/icons/hicolor/

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
/usr/share/desktop-directories/bioinformatics.directory
/etc/xdg/menus/applications-merged/bioinformatics.menu

%changelog
* Fri Nov 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.15-1
- Bugfix release

* Fri Aug 17 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.14-1
- Fix bisulfite coloring bug

* Wed Jul 20 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.13-1
- fix recursive startup bug

* Wed Jul 11 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.11-1
- Menu and popup text for cluster track

* Fri Mar 23 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.10-1
- Allow setting max data range to zero (vs 1E-45). Fixes #517

* Fri Mar 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.9-1
- Fix "is proper pair" test

* Tue Feb 13 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.8-1
- Reset clip rect properly. See issue #511

* Thu Feb 01 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.7-1
- Set clip for arc tracks. Fixes #511

* Thu Jan 11 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.6-1
- Fix NPE exception with Sashimi plot

* Mon Dec 18 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.5-1
- Keep only alignments in view (don't cache).
- Keep alignments for alignment track even if hidden.

* Tue Nov 14 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.4-1
- null check for sequence tile

* Tue Oct 31 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.3-1
- Fix NPE error when restoring session

* Tue Oct 17 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.2-1
- Fixed a problem with loading genomes on Windows. The genome identifier
  appeared in the dropdown menu, but none of the genome data was actually
  loaded.
- Fixed a problem with coloring/sorting/grouping alignments by tag. The popup
  window to enter the tag never appeared.
- Updated the BED file parser to allow a period (.) in the score column.

* Tue Oct 03 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.1-1
- Add 2.4 switches
- Fixes #451
- Present all server genomes for download, including genomes already downloaded.
- Restore default "color by" alignment setting
- Synchonize queries to htsjdk SAMReader -- its not thread safe
- Fixes #452 Sashimi Plot
- Remove "retrieve network" button
- Fixes #463

* Wed Jul 26 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.98-1
- Manifest change for Java 8 1.4.1 bug (affects java webstart)

* Wed Jul 19 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.3.97-1
- Fix for track name bug
- Fix sequence bug
- Update chrom.sizes
