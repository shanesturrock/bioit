%global pkgbase R
%define priority 341
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:           R-core
Version:        3.4.1
Release:        1%{?dist}
Summary:        R statistical computing and graphics environment

Group:          Applications/Engineering
License:	GPL
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:	libR.so()(64bit) libRblas.so()(64bit) libRlapack.so()(64bit)

# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description

R is a free software environment for statistical computing and graphics. It
compiles and runs on a wide variety of UNIX platforms, Windows and MacOS. 

%pre
%dir_exists

%post
alternatives \
  --install %{_bindir}/R R /opt/bioit/%{name}/%{version}/bin/R %{priority} \
  --slave %{_bindir}/Rscript Rscript /opt/bioit/%{name}/%{version}/bin/Rscript

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove R /opt/bioit/%{name}/%{version}/bin/R
fi

%files

%changelog
* Wed Jul 12 2017 Shane Sturrock <shane.sturrock@gmail.com> - 3.4.1-1
- BUG FIXES
  - getParseData() gave incorrect column information when code contained
    multi-byte characters. (PR#17254)
  - Asking for help using expressions like ?stats::cor() did not work.
    (PR#17250)
  - readRDS(url(....)) now works.
  - R CMD Sweave again returns status = 0 on successful completion.
  - Vignettes listed in ‘.Rbuildignore’ were not being ignored properly.
    (PR#17246)
  - file.mtime() no longer returns NA on Windows when the file or directory is
    being used by another process. This affected installed.packages(), which 
    is now protected against this.
  - R CMD INSTALL Windows .zip file obeys --lock and --pkglock flags.
  - (Windows only) The choose.files() function could return incorrect results
    when called with multi = FALSE. (PR#17270)
  - aggregate(<data.frame>, drop = FALSE) now also works in case of near-equal
    numbers in by. (PR#16918)
  - fourfoldplot() could encounter integer overflow when calculating the odds
    ratio. (PR#17286)
  - parse() no longer gives spurious warnings when extracting srcrefs from a
    file not encoded in the current locale.
  - This was seen from R CMD check with ‘inst/doc/*.R’ files, and check has
    some additional protection for such files.
  - print.noquote(x) now always returns its argument x (invisibly).
  - Non-UTF-8 multibyte character sets were not handled properly in source
    references. (PR#16732)
