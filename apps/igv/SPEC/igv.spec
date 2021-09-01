%define priority 21100
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		igv
Version:	2.11.0
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
* Thu Sep 02 2021 Shane Sturrock <shane.sturrock@gmail.com> - 2.11.0-1
- Changed to use sha512 for signing Windows installers

* Thu Aug 05 2021 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.3-1
- Fixed a problem with displaying the popup information in alignment tracks -
  no details where shown for paired-end alignments when "View as pairs" was
  enabled. (Git issue #1003) 

* Thu Jul 15 2021 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.2-1
- 2.10.1
  - Use full height of track to render features in "COLLAPSED" mode.
- 2.10.2
  - Protect more calculated end positions from integer overflow.

* Thu Jul 08 2021 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.0-1
- New features
  - Support for displaying RNA and DNA base modification tags in BAM files,
    described in samtools/hts-specs Git issue #362. These tags are now
    implemented by several Oxford Nanopore tools that detect base modifications,
    including Megalodon and Guppy. (Git issue #945)
  - Allow filtering of feature/annotation tracks based on attributes, via
    Tracks > Filter Tracks. (Git issue #941)
  - New batch command: sortByAttribute
- Bug fixes
  - Couldn't open .igv files from pre-signed Amazon S3 links. (Git issue #922)
    ASK JIM -FIX ONLY FOR .IGV FILES?
  - Tracks were not autoscaling when loading from a port or batch script. (Git
    issue #925)
  - Changing to autoscale or group autoscale on numeric tracks would not take
    effect until the user did something to cause a redraw, for example, pan or
    zoom the view.
  - Fixed issue with gene track translations. When the translation table was
    changed to "vertebrate mitochondrial" and then back to "standard", the
    translations in the RefSeq track were incorrect. (Git issue #923)

* Fri May 07 2021 Shane Sturrock <shane.sturrock@gmail.com> - 2.9.4-1
- 2.9.4
  - Minor bug fixes and code cleanup
- 2.9.3
  - Read stats optimization (alignment experiment type heuristics)

* Fri Feb 19 2021 Shane Sturrock <shane.sturrock@gmail.com> - 2.9.2-1
- Minor bug fixes

* Fri Nov 27 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.8.13-1
- Minor bug fixes

* Fri Nov 20 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.8.12-1
- remove diagnostic print

* Fri Oct 30 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.8.11-1
- Revert "Bug fix -- altColor ignored in feature tracks"

* Fri Aug 14 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.8.9-1
- more precise alignment width calculation (round vs floor)

* Fri Mar 27 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.8.2-1
- Rework reload session & tracks.
- Simplify autoscaling - respect track line.
- fix minor issues with "Reload Tracks" and "Reload Sessions"

* Fri Jan 24 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.8.0-1
- oAuth init error messages

* Fri Nov 08 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.7.2-1
- Fix line plot error (see #715)

* Fri Oct 18 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.7.1-1
- remove unused code
- catch error when removing provisioning URL (don't try to load "")
- correct readme and remove unused (and incorrect) hidpi scripts.
- update server data

* Fri Aug 09 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.6.2-1
- fix "exists" test

* Fri Aug 02 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.6.1-1
- draw bedpe arcs between absolute center of features, don't round down to an
  int

* Fri Jul 26 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.6.0-1
- Increase max cigar length for popup info from 60 to 1000. See issue #667

* Fri May 31 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.5.3-1
- base64 encode proxy password field

* Fri May 03 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.5.2-1
- Replace creation of URLHelper by reflection with factory object. See issue
  #646
- remove unused imports (2.5.1)

* Fri Mar 22 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.5.0-1
- Switched to Java 11

* Fri Feb 22 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.19-1
- update genome registry url
- npe fix in AlignmentTrack

* Fri Feb 08 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.18-1
- update bam csi test files

* Fri Feb 01 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.17-1
- index path logic

* Fri Nov 23 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.16-1
- Fix error creating sessions with merged tracks. Fixes #602

* Fri Nov 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.15-1
- Bugfix release

* Fri Aug 17 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.14-1
- Fix bisulfite coloring bug

* Fri Jul 20 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.4.13-1
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
