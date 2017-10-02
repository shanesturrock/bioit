%global pkgbase R
%define priority 342
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:           R-core
Version:        3.4.2
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
* Tue Oct 03 2017 Shane Sturrock <shane.sturrock@gmail.com> - 3.4.2-1
- NEW FEATURES
  - Setting the LC_ALL category in Sys.setlocale() invalidates any cached
    locale-specific day/month names and the AM/PM indicator for strptime() (as
    setting LC_TIME has since R 3.1.0).
  - The version of LAPACK included in the sources has been updated to 3.7.1, a
    bug-fix release.
  - The default for tools::write_PACKAGES(rds_compress=) has been changed to
    "xz" to match the compression used by CRAN.
  - c() and unlist() are now more efficient in constructing the names(.) of
    their return value, thanks to a proposal by Suharto Anggono. (PR#17284)
- UTILITIES
  - R CMD check checks for and R CMD build corrects CRLF line endings in shell
    scripts configure and cleanup (even on Windows).
- INSTALLATION on a UNIX-ALIKE
  - A workaround has been added for the change in location of time-zone files
    on macOS 10.13 ‘High Sierra’, so the default time zone is deduced correctly
    from the system setting when R is configured with --with-internal-tzcode 
    (the default on macOS).
  - The order of selection of OpenMP flags has been changed: Oracle Developer
    Studio 12.5 accepts -fopenmp and -xopenmp but only the latter enables
    OpenMP so it is now tried first.
- BUG FIXES
  - raw(0) & raw(0) now returns raw again; ditto for |.
  - within(List, rm(x1, x2)) works correctly again, including when List[["x2"]]
    is NULL.
  - regexec(pattern, text, *) now applies as.character(.) to its first two
    arguments, as documented.
  - write.table() and related functions, writeLines(), and perhaps other
    functions writing text to connections did not signal errors when the writes
    failed, e.g. due to a disk being full. Errors will now be signalled if 
    detected during the write, warnings if detected when the connection is 
    closed. (PR#17243)
  - rt() assumed the ncp parameter was a scalar. (PR#17306)
  - menu(choices) with more than 10 choices which easily fit into one
    getOption("width")-line no longer erroneously repeats choices. (PR#17312)
  - length()<- on a pairlist succeeds.
    (https://stat.ethz.ch/pipermail/r-devel/2017-July/074680.html)
  - Language objects such as quote(("\n")) or R functions are correctly printed
    again, where R 3.4.1 accidentally duplicated the backslashes.
  - Construction of names() for very large objects in c() and unlist() now
    works, thanks to Suharto Anggono's patch proposals in PR#17292.
  - Resource leaks (and similar) reported by Steve Grubb fixed. (PR#17314,
    PR#17316, PR#17317, PR#17318, PR#17319, PR#17320)
  - model.matrix(~1, mf) now gets the row names from mf also when they differ
    from 1:nrow(mf), fixing PR#14992 thanks to the suggestion by Sebastian
    Meyer.
  - sigma(fm) now takes the correct denominator degrees of freedom for a fitted
    model with NA coefficients. (PR#17313)
  - hist(x, "FD") no longer “dies” with a somewhat cryptic error message when x
    has extreme outliers or IQR() zero: nclass.FD(x) tries harder to find a
    robust bin width h in the latter case, and hist.default(*, breaks) now 
    checks and corrects a too large breaks number. (PR#17274)
  - callNextMethod() works for ... methods.
  - qr.coef(qd, y) now has correct names also when qd is a complex QR or stems
    from qr(*, LAPACK=TRUE).
  - Setting options(device = *) to an invalid function no longer segfaults when
    plotting is initiated. (PR#15883)
  - encodeString(<very large string>) no longer segfaults. (PR#15885)
  - It is again possible to use configure --enable-maintainer-mode without
    having installed notangle (it was required in R 3.4.[01]).
  - S4 method dispatch on ... calls the method by name instead of .Method (for
    consistency with default dispatch), and only attempts to pass non-missing
    arguments from the generic.
  - readRDS(textConnection(.)) works again. (PR#17325)
  - (1:n)[-n] no longer segfaults for n <- 2.2e9 (on a platform with enough
    RAM).
  - x <- 1:2; tapply(x, list(x, x), function(x) "")[1,2] now correctly returns
    NA. (PR#17333)
  - Running of finalizers after explicit GC request moved from the R interface
    do_gc to the C interface R_gc. This helps with reclaiming inaccessible
    connections.
  - help.search(topic) and ??topic matching topics in vignettes with multiple
    file name extensions (e.g., ‘*.md.rsp’ but not ‘*.Rmd’) failed with an
    error when using options(help_type = "html").
  - The X11 device no longer uses the Xlib backing store (PR#16497).
  - array(character(), 1) now gives (a 1D array with) NA as has been documented
    for a long time as in the other cases of zero-length array initialization
    and also compatibly with matrix(character(), *). As mentioned there, this 
    also fixes PR#17333.
  - splineDesign(.., derivs = 4) no longer segfaults.
  - fisher.test(*, hybrid=TRUE) now (again) will use the hybrid method when
    Cochran's conditions are met, fixing PR#16654.

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
