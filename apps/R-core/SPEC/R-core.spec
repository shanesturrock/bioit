%global pkgbase R
%define priority 420
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:           R-core
Version:        4.2.0
Release:        1%{?dist}
Summary:        R statistical computing and graphics environment

Group:          Applications/Engineering
License:	GPL
Source0:	R-x86_64.conf
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

%install
rm -rf %{buildroot}
# Install ld.so.conf.d file
mkdir -p %{buildroot}/%{_sysconfdir}/ld.so.conf.d/
install -m 644 %{SOURCE0} %{buildroot}/%{_sysconfdir}/ld.so.conf.d/

%post
alternatives \
  --install %{_bindir}/R R /opt/bioit/%{name}/%{version}/bin/R %{priority} \
  --slave %{_bindir}/Rscript Rscript /opt/bioit/%{name}/%{version}/bin/Rscript \
  --slave %{_mandir}/man1/R.1 R.1 /opt/bioit/%{name}/%{version}/share/man/man1/R.1 \
  --slave %{_mandir}/man1/Rscript.1 Rscript.1 /opt/bioit/%{name}/%{version}/share/man/man1/Rscript.1
rm /usr/lib64/R
ln -s /opt/bioit/%{name}/%{version}/lib64/R /usr/lib64/R
ldconfig

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove R /opt/bioit/%{name}/%{version}/bin/R 
  rm /usr/lib64/R
  ldconfig
fi

%files
%defattr(-,root,root,-)
%{_sysconfdir}/ld.so.conf.d/R-x86_64.conf
#/etc/ld.so.conf.d/R-x86_64.conf

%changelog
* Tue May 03 2022 Shane Sturrock <shane.sturrock@gmail.com> - 4.2.0-1
- SIGNIFICANT USER-VISIBLE CHANGES
  - The formula method of aggregate() now matches the generic in naming its
    first argument x (resolving PR#18299 by Thomas Soeiro).
  - This means that calling aggregate() with a formula as a named first
    argument requires name formula in earlier versions of R and name x now, so
    portable code should not name the argument (code in many packages did).
  - Calling && or || with either argument of length greater than one now gives
    a warning (which it is intended will become an error).
  - Calling if() or while() with a condition of length greater than one gives
    an error rather than a warning. Consequently, environment variable
    _R_CHECK_LENGTH_1_CONDITION_ no longer has any effect.
- NEW FEATURES
  - matrix(x, n, m) now warns in more cases where length(x) differs from n * m,
    as suggested by Abby Spurdle and Wolfgang Huber in Feb 2021 on the R-devel
    mailing list.
  - This warning can be turned into an error by setting environment variable
    _R_CHECK_MATRIX_DATA_ to ‘⁠TRUE⁠’: R CMD check --as-cran does so unless it
    is already set.
  - Function file_test() in package utils gains tests for symlinks, readability
    and writability.
  - capabilities("libxml") is now false.
  - The description of capabilities("http/ftp") now reflects that it refers to
    the default method, no longer the internal one.
  - simplify2array() gains an except argument for controlling the exceptions
    used by sapply().
  - Environment variables R_LIBS_USER and R_LIBS_SITE are both now set to the R
    system default if unset or empty, and can be set to NULL to indicate an
    empty list of user or site library directories.
  - The warning for axis()(-like) calls in cases of relatively small ranges
    (typically in log-scale situations) is slightly improved and suppressed
    from explicit calls to .axisPars() as has always been the intention.
  - The contrasts setter function `contrasts<-` gains an explicit default
    how.many = NULL rather than just using missing(how.many).
  - grid.pretty() gains a new optional argument n = 5.
  - There is a new function .pretty() with option bounds as a technical-utility
    version of pretty(). It and pretty() gain a new argument f.min with a
    better than back-compatible default.
  - Function grDevices::axisTicks() and related functions such as
    graphics::axis() work better, notably for the log scale; partly because of
    the pretty() improvements, but also because care is taken e.g., when ylim is
    finite but diff(ylim) is infinite.
  - nclass.FD() gains a digits option.
  - The R Mathlib internal C function bd0() (called indirectly from a dozen
    probability density and distribution functions such as dpois(), dbinom(),
    dgamma(), pgamma() etc) has been complemented by a more sophisticated and
    (mostly) more accurate C function ebd0(), currently called only by internal
    dpois_raw() improving accuracy for R level dpois() and potentially others
    calling it such as dnbinom(), dgamma() or pgamma(). (Thanks to Morten
    Welinder's PR#15628.)
  - write.ftable() gains sep = " " argument as suggested by Thomas Soeiro.
  - The names of the locale categories supported by R's Sys.getlocale() and
    Sys.setlocale() are now provided by variable .LC.categories in the base
    namespace.
  - The Date and POSIXt methods for hist() and the histogram method for plot()
    now also use the new default col = "lightgray" in consistency with the
    corresponding change to hist()'s default for R 4.0.0.
  - hist.default() gains new fuzz argument, and the histogram plot method no
    longer uses fractional axis ticks when displaying counts ("Frequency").
  - mapply() and hence Map() now also obey the “max-or-0-if-any” recycling
    rule, such that, e.g., Map(`+`, 1:3, 1[0]) is valid now.
  - as.character(<obj>) for "hexmode" or "octmode" objects now fulfils the
    important basic rule as.character(x)[j] === as.character(x[j]).
  - The set utility functions, notably intersect() have been tweaked to be more
    consistent and symmetric in their two set arguments, also preserving a
    common mode.
  - substr(ch, start,end) <- new now e.g., preserves names(ch); ditto for
    substring(), thanks to a patch from Brodie Gaslam.
  - plot(<lm>) gains a extend.ylim.f argument, in partial response to PR#15285;
    further PR#17784 is fixed thanks to several contributors and a patch by
    Elin Waring. The Cook's dist contours get customizable via cook.col and
    cook.lty with a different default color and their legend is nicer by default
    and customizable via cook.legendChanges.
  - Attempting to subset an object that is not subsettable now signals an error
    of class notSubsettableError. The non-subsettable object is contained in
    the object field of the error condition.
  - Subscript-out-of-bounds errors are now signaled as errors of class
    subscriptOutOfBoundsError.
  - Stack-overflow errors are now signaled as errors inheriting from class
    stackOverflowError. See ?stackOverflowError for more details.
  - New partly experimental Sys.setLanguage() utility, solving the main problem
    of PR#18055.
  - gettext() and gettextf() get a new option trim = TRUE which when set to
    false allows translations for strings such as "Execution halted\n" typical
    for C code.
  - An experimental implementation of hash tables is now available. See
    ?hashtab for more details.
  - identical() gains a extptr.as.ref argument for requesting that external
    pointer objects be compared as reference objects.
  - reorder() gets an argument decreasing which it passes to sort() for level
    creation; based on the wish and patch by Thomas Soeiro in PR#18243.
  - as.vector() gains a data.frame method which returns a simple named list,
    also clearing a long standing ‘FIXME’ to enable as.vector(<data.frame>,
    mode="list"). This breaks code relying on as.vector(<data.frame>) to return
    the unchanged data frame.
  - legend() is now vectorized for arguments cex, x.intersp, and text.width.
    The latter can now also be specified as a vector (one element for each
    column of the legend) or as NA for computing a proper column wise maximum
    value of strwidth(legend). The argument y.intersp can be specified as a
    vector with one entry for each row of the legend.
  - legend() also gains new arguments title.cex and title.font. Thanks to
    Swetlana Herbrandt.
  - Deparsing no longer remaps attribute names dim, dimnames, levels, names and
    tsp to historical S-compatible names (which structure() maps back).
  - sample() and sample.int() have additional sanity checks on their size and n
    arguments.
  - all.equal.numeric() gains a sanity check on its tolerance argument –
    calling all.equal(a, b, c) for three numeric vectors is a surprisingly
    common error.
  - mean(na.rm =), rank(na.last =), barplot(legend.text =), boxplot(),
    contour(drawlabels =), polygon(border =) and methods::is(class2 =) have
    more robust sanity checks on their arguments.
  - R CMD Rd2pdf (used by R CMD check) has a more robust sanity check on the
    format of \alias{} commands.
  - psigamma(x, deriv) for negative x now also works for deriv = 4 and 5; their
    underlying C level dpsifn() is documented in ‘Writing R Extensions’.
  - The HTML help system now uses HTML5 (wish of PR#18149).
  - ks.test() now provides exact p-values also with ties and MC p-values in the
    two-sample (Smirnov) case. By Torsten Hothorn.
  - ks.test() gains a formula interface, with y ~ 1 for the one-sample
    (Kolmogorov) test and y ~ group for the two-sample (Smirnov) test.
    Contributed by Torsten Hothorn.
  - The return value from ks.test() now has class c("ks.test", "htest") –
    packages using try() need to take care to use inherits() and not == on the
    class.
  - New functions psmirnov(), qsmirnov() and rsmirnov() in package stats
    implementing the asymptotic and exact distributions of the two-sample
    Smirnov statistic.
  - iconv() now allows sub = "c99" to use C99-style escapes for UTF-8 inputs
    which cannot be converted to encoding to.
  - In a forward pipe |> expression it is now possible to use a named argument
    with the placeholder _ in the rhs call to specify where the lhs is to be
    inserted. The placeholder can only appear once on the rhs.
  - The included LAPACK sources have been updated to version 3.10.0, except for
    the four Fortran 77 routines which 3.10.0 has re-implemented in Fortran 90
    (where the older versions have been retained as the R build process does not
    support Fortran 90).
  - path.expand() and most other uses of tilde expansion now warn if a path
    would be too long if expanded. (An exception is file.exists(), which
    silently returns false.)
  - trunc(<Date>, *) now supports units = "months" or "years" for consistency
    with the POSIXt method, thanks to Dirk Eddelbuettel's proposal in PR#18099.
  - list2DF() now checks that its arguments are of the same length, rather than
    use recycling.
  - The HTML help system has several new features: LaTeX-like math can be
    typeset using either KaTeX or MathJax, usage and example code is
    highlighted using Prism, and for dynamic help the output of examples and
    demos can be shown within the browser if the knitr package is installed.
    These features can be disabled by setting the environment variable
    _R_HELP_ENABLE_ENHANCED_HTML_ to a false value.
- GRAPHICS
  - The graphics engine version, R_GE_version, has been bumped to 15 and so
    packages that provide graphics devices should be reinstalled.
  - The grid package now allows the user to specify a “vector” of pattern
    fills. The fill argument to gpar() accepts a list of gradients and/or
    patterns and the functions linearGradient(), radialGradient(), and pattern()
    have a new group argument.
  - Points grobs (data symbols) can now also have a pattern fill.
  - The grobCoords() function now returns a more informative and complex
    result.
  - The grid package has new functions for drawing isolated groups:
    grid.group(), grid.define(), and grid.use(). These functions add
    compositing operators and affine transformations to R's graphics
    capabilities.
  - The grid package also has new functions for stroking and filling paths:
    grid.stroke(), grid.fill(), and grid.fillStroke().
  - A new function as.path() allows the user to specify the fill rule for a
    path that is to be used for clipping, stroking, or filling; available
    options are "winding" and "evenodd". A new function as.mask() allows the
    user to specify the type of a mask; available options are "alpha" and
    "luminance".
  - These new features are only supported so far (at most) on the Cairo-based
    graphics devices and on the pdf() device.
  - dev.capabilities() reports on device support for the new features.
  - par() now warns about unnamed non-character arguments to prevent misuse
    such as {usr <- par("usr"); par(usr)}.
- INSTALLATION
  - The libraries searched for by --with-blas (without a value) now include
    BLIS (after OpenBLAS but before ATLAS). And on macOS, the Accelerate
    framework (after ATLAS).
  - The included LAPACK sources have been updated to 3.10.1.
  - Facilities for accessing ‘⁠ftp://⁠’ sites are no longer tested (except pro
    tem for curlGetHeaders()) as modern browsers have removed support.
  - R can now be built with ‘⁠DEFS = -DSTRICT_R_HEADERS⁠’ .
- PACKAGE INSTALLATION
  - R CMD INSTALL no longer tangles vignettes. This completes an R CMD build
    change in R 3.0.0 and affects packages built before R 3.0.2. Such packages
    should be re-made with R CMD build to have the tangled R code of vignettes
    shipped with the tarball.
  - USE_FC_LEN_T will become the default: this uses the correct prototypes for
    Fortran BLAS/LAPACK routines called from C/C++, and requires adjustment of
    most such calls – see ‘Writing R Extensions’ §6.6.2. (This has been
    supported since R 3.6.2.)
  - Package installation speed for packages installed with keep.source has been
    improved. This resolve the issue reported by Ofek Shilon in PR#18236.
- UTILITIES
  - Setting environment variable _R_CHECK_RD_VALIDATE_RD2HTML_ to false value
    will override R CMD check --as-cran and turn off HTML validation. This
    provides a way to circumvent a problematic tidy such as the 2006 version
    that ships with macOS.
  - R CMD check can optionally report files/directories left behind in home,
    ‘/tmp’ (even though TMPDIR is set) and other directories. See the “R
    Internals” manual for details.
  - R CMD check now reports byte-compilation errors during installation. These
    are not usually fatal but may result in parts of the package not being
    byte-compiled.
  - _R_CHECK_DEPENDS_ONLY_ can be applied selectively to examples, tests and/or
    vignettes in R CMD check: see the “R Internals” manual.
  - _R_CHECK_SRC_MINUS_W_IMPLICIT_ now defaults to true: recent versions of
    Apple clang on macOS have made implicit function declarations in C into a
    compilation error.
  - R CMD check --as-cran makes use of the environment variable AUTORECONF. See
    the “R Internals” manual §8 for further details.
  - R CMD check --use-valgrind also uses valgrind when re-building vignettes as
    some non-Sweave vignettes unhelpfully comment out all their code when R CMD
    check runs vignettes.
  - Errors in re-building vignettes (unless there are LaTeX errors) are
    reported by R CMD check as ‘⁠ERROR⁠’ rather than ‘⁠WARNING⁠’ when running
    vignettes has been skipped (as it frequently is in CRAN checks and by
    --as-cran).
  - R CMD Rd2pdf gains a --quiet option that is used by R CMD build when
    building the PDF package manual.
  - R CMD Rd2pdf now always runs LaTeX in batch mode, consistent with Texinfo
    \ge≥ 6.7. The --batch option is ignored.
  - R CMD build and R CMD check now include the Rd file name and line numbers
    in the error message of an ⁠\Sexpr⁠ evaluation failure.
  - For packages using the ⁠\doi⁠ Rd macro (now an install-time ⁠\Sexpr⁠) but
    no other dynamic Rd content, R CMD build now produces a smaller tarball and
    is considerably faster – skipping temporary package installation.
  - R CMD check can optionally (but included in --as-cran) validate the HTML
    produced from the packages ‘.Rd’ files. 
- C-LEVEL FACILITIES
  - The non-API header ‘R_ext/R-ftp-http.h’ is no longer provided, as the entry
    points it covered are now all defunct.
  - A number of non-API declarations and macro definitions have been moved from
    the installed header ‘Rinternals.h’ to the internal header ‘Defn.h’.
    Packages that only use entry points and definitions documented to be part of
    the API as specified in ‘Writing R Extensions’ §6 should not be affected.
  - The macro USE_RINTERNALS no longer has any effect when compiling package
    code. Packages which also use R_NO_REMAP will need to ensure that the
    remapped names are used for calls to API functions that were formerly also
    made available as macros.
  - The deprecated legacy S-compatibility macros PROBLEM, MESSAGE, ERROR, WARN,
    WARNING, RECOVER, ... are no longer defined in ‘R_exts/RS.h’ (included by
    ‘R.h’). Replace these by calls to Rf_error and Rf_warning (defined in header
    ‘R_ext/Error.h’ included by ‘R.h’).
  - Header ‘R_ext/RS.h’ no longer includes ‘R_ext/Error.h’.
  - Header ‘R_ext/Constants.h’ (included by ‘R.h’) when included from C++ now
    includes the C++ header ‘cfloat’ rather than the C header ‘float.h’ (now
    possible as C++11 is required).
  - The legacy S-compatibility macros DOUBLE_* in ‘R_ext/Constants.h’ (included
    by ‘R.h’) are deprecated.
  - The deprecated S-compatibility macros SINGLE_* in ‘R_ext/Constants.h’
    (included by ‘R.h’) have been removed.
  - R_Calloc, R_Free and R_Realloc are preferred to their unprefixed forms and
    error messages now use the prefix. These forms were introduced in R 3.4.0
    and are available even when STRICT_R_HEADERS is defined.
  - rmultinom has been documented in ‘Writing R Extensions’ §6 so is now part
    of the R API.
  - Similarly, Rtanpi, called from R level tanpi() is now part of the R API.
  - The long-deprecated, undocumented and non-API entry point call_R is no
    longer declared in ‘R_ext/RS.h’ (included by ‘R.h’).
  - The header ‘S.h’ which has been unsupported since Jan 2016 has been
    removed. Use ‘R.h’ instead.
- DEPRECATED AND DEFUNCT
  - The (non-default and deprecated) method = "internal" for download.file()
    and url() no longer supports ‘⁠http://⁠’ nor ‘⁠ftp://⁠’ URIs. (It is used
    only for ‘⁠file://⁠’ URIs.)
  - default.stringsAsFactors() is now formally deprecated, where that was only
    mentioned on its regular help page, previously. So it now gives a warning
    if called.
  - unix.time() is defunct now; it had been deprecated since R 3.4.0.
- BUG FIXES
  - library() now passes its lib.loc argument when requiring Depends packages;
    reported (with fix) in PR#18331 by Mikael Jagan.
  - Setting digits = 0 in format(), print.default() (and hence typically
    print()) or options() is again invalid. Its behaviour was
    platform-dependent, and it is unclear what “zero significant digits” should
    mean (PR#18098).
  - Messages from C code in the ‘cairo’ section of package grDevices are now
    also offered for translation, thanks to Michael Chirico's PR#18123.
  - mean(x) with finite x now is finite also without "long.double" capability.
  - R CMD Rd2pdf no longer leaves an empty build directory behind when it
    aborts due to an already existing output file. (Thanks to Sebastian Meyer's
    PR#18141.)
  - density(x, weights = w, na.rm = TRUE) when anyNA(x) is true, now removes
    weights “in parallel” to x, fixing PR#18151, reported by Matthias Gondan.
    Additionally, it gets a subdensity option.
  - Conversion of ⁠\Sexpr[]{<expR>}⁠ to LaTeX or HTML no longer produces long
    blocks of empty lines when <expR> itself contains several lines all
    producing empty output. Thanks to a report and patch by Ivan Krylov posted
    to R-devel.
  - R CMD build no longer fails if a package vignette uses child documents and
    ‘inst/doc’ exists. (Thanks to Sebastian Meyer's PR#18156.)
  - When an R documentation (‘help’ source) file ‘man/foo.Rd’ in a package has
    ⁠\donttest{..}⁠ examples with a syntax error, it is now signalled as ERROR
    and with correct line numbers relating to the ‘*-Ex.R’ file, thanks to
    Duncan Murdoch and Sebastian Meyer's reports and patch proposals in
    PR#17501.
  - Improved determination of the correct translation domain in non-base
    packages, addressing the combination of PR#18092 and PR#17998 (#c6) with
    reports and augmented patch #2904 by Suharto Anggono.
  - Note that "R-base" is no longer the default domain e.g., for top-level
    calls to gettext(); rather translation needs explicit domain = *
    specification in such cases.
  - identical(attrib.as.set=FALSE) now works correctly with data frames with
    default row names (Thanks to Charlie Gao's PR#18179).
  - txtProgressBar() now enforces a non-zero width for argument char, without
    which no progress can be visible.
  - dimnames(table(d)) is more consistent in the case where d is a list with a
    single component, thanks to Thomas Soeiro's report to R-devel.
  - Further, table(d1, d2) now gives an error when d1 and d2 are data frames as
    suggested by Thomas in PR#18224.
  - The deparser now wraps sub-expressions such as if(A) .. with parentheses
    when needed; thanks to Duncan Murdoch's PR#18232 and Lionel Henry's patches
    there.
  - remove.packages() no longer tries to uninstall Priority: base packages,
    thanks to a report and suggestions by Colin Fay in PR#18227.
  - x[i] and x[[i]] for non-integer i should now behave in all cases as always
    documented: the index used is equivalent to as.integer(i) unless that would
    overflow where trunc(i) is used instead; thanks to Suharto Anggono's report
    and patch proposals in PR#17977.
  - asOneSidedFormula() now associates the resulting formula with the global
    environment rather than the evaluation environment created for the call.
  - <bibentry>$name now matches the field name case-insensitively, consistent
    with bibentry() creation and the replacement method.
  - cbind() failed to detect some length mismatches with a mixture of
    time-series and non-time-series inputs.
  - The default LaTeX style file ‘Sweave.sty’ used by the RweaveLatex driver no
    longer loads the obsolete ‘⁠ae⁠’ package; thanks to a report by Thomas
    Soeiro in PR#18271. Furthermore, it now skips ‘⁠\usepackage[T1]{fontenc}⁠’
    for engines other than pdfTeX (if detected) or if the new ‘⁠[nofontenc]⁠’
    option is used.
  - smooth.spline() now stores its logical cv argument more safely, fixing a
    rare bug when printing, and also stores n.
  - smooth.spline(x,y,*) now computes the cv.crit statistic correctly, also
    when is.unsorted(x), fixing PR#18294.
  - The data.frame method of rbind() now warns when binding
    not-wholly-recycling vectors, by analogy to the default method (for
    matrices).
  - setAs() finds the correct class for name to when multiple packages define a
    class with that name. Thanks to Gabor Csardi for the report.
  - Fix for detaching a package when two classes of the same name are present
    in method signatures for the same generic. Thanks to Gabor Csardi for the
    report.
  - match.arg("", c("", "a", "B")) gives a better error message, in part from
    PR#17959, thanks to Elin Waring.
  - R CMD Sweave --clean no longer removes pre-existing files or subdirectories
    (PR#18242).
  - The quartz() device no longer splits polylines into subpaths. That has
    caused narrowly-spaced lines with many points to always look solid even
    when dashed line type was used due to dash phase restarts.
  - Deparsing constructs such as quote(1 + `!`(2) + 3) works again as before R
    3.5.0, thanks to the report and patch in PR#18284 by Suharto Anggono.
  - as.list(f) for a factor f now keeps names(f), fixing PR#18309.
  - qbeta(.001, .9, .009) and analogous qf() calls now return a correct value
    instead of NaN or wrongly 1, all with a warning; thanks to the report by
    Ludger Goeminne in PR#18302.
  - plot.lm() failed to produce the plot of residuals vs. factor levels (i.e.,
    which=5 when leverages are constant) for models with character predictors
    (PR#17840).
  - interaction.plot(..., xtick = TRUE) misplaced the x-axis line (PR#18305).
  - Not strictly fixing a bug, format()ing and print()ing of non-finite Date
    and POSIXt values NaN and \pm±Inf no longer show as NA but the respective
    string, e.g., Inf, for consistency with numeric vector's behaviour,
    fulfilling the wish of PR#18308.
  - R CMD check no longer runs test scripts generated from corresponding ‘.Rin’
    files twice and now signals an ERROR if processing an ‘.Rin’ script fails.
  - tools::Rd2txt() used for plain-text help pages now renders ⁠\href⁠s (if
    tools::Rd2txt_options(showURLs = TRUE)) and ⁠\url⁠s with percent-encoding
    and standards-compliant delimiting style (angle brackets and no ‘⁠URL: ⁠’
    prefix). ⁠\email⁠ is now rendered with a ‘⁠mailto:⁠’ prefix.

* Fri Mar 11 2022 Shane Sturrock <shane.sturrock@gmail.com> - 4.1.3-1
- NEW FEATURES:
  - The default version of Bioconductor has been changed to 3.14.
    (This is used by setRepositories and the menus in GUIs.)
- UTILITIES:
  - R CMD check --as-cran has a workaround for a bug in versions of
    file up to at least 5.41 which mis-identify DBF files last
    changed in 2022 as executables.
- C-LEVEL FACILITIES:
  - The legacy S-compatibility macros SINGLE_* in R_ext/Constants.h
    (included by R.h) are deprecated and will be removed in R 4.2.0.
- BUG FIXES:
  - Initialization of self-starting nls() models with initialization
    functions following the pre-R-4.1.0 API (without the ...
    argument) works again for now, with a deprecation warning.
  - Fixed quoting of ~autodetect~ in Java setting defaults to avoid
    inadvertent user lookup due to leading ~, reported in PR#18231 by
    Harold Gutch.
  - substr(., start, stop) <- v now treats _negative_ stop values
    correctly.  Reported with a patch in PR#18228 by Brodie Gaslam.
  - Subscripting an array x without dimnames by a
    length(dim(x))-column character matrix gave "random" non-sense,
    now an error; reported in PR#18244 by Mikael Jagan.
  - ...names() now matches names(list(...)) closely, fixing PR#18247.
  - all.equal(*, scale = s) now works as intended when length(s) > 1,
    partly thanks to Michael Chirico's PR#18272.
  - print(x) for long vectors x now also works for named atomic
    vectors or lists and prints the correct number when reaching the
    getOption("max.print") limit; partly thanks to a report and
    proposal by Hugh Parsonage to the R-devel list.
  - all.equal(<selfStart>, *) no longer signals a deprecation
    warning.
  - reformulate(*, response=r) gives a helpful error message now when
    length(r) > 1, thanks to Bill Dunlap's PR#18281.
  - Modifying globalCallingHandlers inside withCallingHandlers() now
    works or fails correctly, thanks to Henrik Bengtsson's PR#18257.
  - hist(<Date>, breaks = "days") and hist(<POSIXt>, breaks = "secs")
    no longer fail for inputs of length 1.
  - qbeta(.001, .9, .009) and similar cases now converge correctly
    thanks to Ben Bolker's report in PR#17746.
  - window(x, start, end) no longer wrongly signals “'start' cannot
    be after 'end'”, fixing PR#17527 and PR#18291.
  - data() now checks that its (rarely used) list argument is a
    character vector - a couple of packages passed other types and
    gave incorrect results.
  - which() now checks its arr.ind argument is TRUE rather coercing
    to logical and taking the first element - which gave incorrect
    results in package code.
  - model.weights() and model.offset() more carefully extract their
    model components, thanks to Ben Bolker and Tim Taylor's R-devel
    post.
  - list.files(recursive = TRUE) now shows all broken symlinks
    (previously, some of them may have been omitted, PR#18296).

* Fri Nov 05 2021 Shane Sturrock <shane.sturrock@gmail.com> - 4.1.2-1
- C-LEVEL FACILITIES
  - The workaround in headers ‘R.h’ and ‘Rmath.h’ (using namespace std;) for
    the Oracle Developer Studio compiler is no longer needed now C++11 is
    required so has been removed. A couple more usages of log() (which should
    have been std::log()) with an int argument are reported on Solaris.
  - The undocumented limit of 4095 bytes on messages from the S-compatibility
    macros PROBLEM and MESSAGE is now documented and longer messages will be
    silently truncated rather than potentially causing segfaults.
  - If the R_NO_SEGV_HANDLER environment variable is non-empty, the signal
    handler for SEGV/ILL/BUS signals (which offers recovery user interface) is
    not set. This allows more reliable debugging of crashes that involve the
    console.
- DEPRECATED AND DEFUNCT
  - The legacy S-compatibility macros PROBLEM, MESSAGE, ERROR, WARN, WARNING,
    RECOVER, ... are deprecated and will be hidden in R 4.2.0. R's native
    interface of Rf_error and Rf_warning has long been preferred.
- BUG FIXES
  - .mapply(F, dots, .) no longer segfaults when dots is not a list and uses
    match.fun(F) as always documented; reported by Andrew Simmons in PR#18164.
  - hist(<Date>, ...) and hist(<POSIXt>, ...) no longer pass arguments for
    rect() (such as col and density) to axis(). (Thanks to Sebastian Meyer's
    PR#18171.)
  - \Sexpr{ch} now preserves Encoding(ch). (Thanks to report and patch by
    Jeroen Ooms in PR#18152.)
  - Setting the RNG to "Marsaglia-Multicarry" e.g., by RNGkind(), now warns in
    more places, thanks to André Gillibert's report and patch in PR#18168.
  - gray(numeric(), alpha=1/2) no longer segfaults, fixing PR#18183, reported
    by Till Krenz.
  - Fixed dnbinom(x, size=<very_small>, .., log=TRUE) regression, reported by
    Martin Morgan.
  - as.Date.POSIXlt(x) now keeps names(x), thanks to Davis Vaughan's report and
    patch in PR#18188.
  - model.response() now strips an "AsIs" class typically, thanks to Duncan
    Murdoch's report and other discussants in PR#18190.
  - try() is considerably faster in case of an error and long call, as e.g.,
    from some do.call(). Thanks to Alexander Kaever's suggestion posted to
    R-devel.
  - qqline(y = <object>) such as y=I(.), now works, see also PR#18190.
  - Non-integer mgp par() settings are now handled correctly in axis() and
    mtext(), thanks to Mikael Jagan and Duncan Murdoch's report and suggestion
    in PR#18194.
  - formatC(x) returns length zero character() now, rather than "" when x is of
    length zero, as documented, thanks to Davis Vaughan's post to R-devel.
  - removeSource(fn) now retains (other) attributes(fn).

* Tue Aug 18 2021 Shane Sturrock <shane.sturrock@gmail.com> - 4.1.1-1
- NEW FEATURES
  - require(pkg, quietly = TRUE) is quieter and in particular does not warn if
    the package is not found.
- DEPRECATED AND DEFUNCT
  - Use of ftp:// URIs should be regarded as deprecated, with on-going support
    confined to method = "libcurl" and not routinely tested. (Nowadays no major
    browser supports them.)
  - The non-default method = "internal" is deprecated for http:// and ftp://
    URIs for both download.file and url.
  - For ftp:// URIs the default method is now "libcurl" if available (which it
    is on CRAN builds).
  - method = "wininet" remains the default for http:// and https:// URIs but if
    libcurl is available, using method = "libcurl" is preferred.
- INSTALLATION
  - make check now works also without a LaTeX installation. (Thanks to
    Sebastian Meyer's PR#18103.)
- BUG FIXES
  - .mapply(F, dots, .) no longer segfaults when dots is not a list and ensures
    F is a function; reported by Andrew Simmons in PR#18164.
  - make check-devel works again in an R build configured with
    --without-recommended-packages.
  - qnbinom(p, size, mu) for large size/mu is correct now in a range of cases
    (PR#18095); similarly for the (size, prob) parametrization of the negative
    binomial. Also qpois() and qbinom() are better and or faster for extreme
    cases.  The underlying C code has been modularized and is common to all
    four cases of discrete distributions.
  - gap.axis is now part of the axis() arguments which are passed from bxp(),
    and hence boxplot(). (Thanks to Martin Smith's report and suggestions in
    PR#18109.)
  - .First and .Last can again be set from the site profile.
  - seq.int(from, to, *) and seq.default(..) now work better in large range
    cases where from-to is infinite where the two boundaries are finite.
  - all.equal(x,y) now returns TRUE correctly also when several entries of
    abs(x) and abs(y) are close to .Machine$double.xmax, the largest finite
    numeric.
  - model.frame() now clears the object bit when removing the class attribute
    of a value via na.action (PR#18100).
  - encodeString() on Solaris now works again in Latin-1 encoding on characters
    represented differently in UTF-8. Support for surrogate pairs on Solaris
    has been improved.
  - pretty(x) with finite x now returns finite values also in the case where
    the extreme x values are close in size to the maximal representable number
    .Machine$double.xmax.
  - Also, it's been tweaked for very small ranges and when a boundary is close
    (or equal) to zero; e.g., pretty(c(0,1e-317)) no longer has negative
    numbers, currently still warning about a very small range, and
    pretty(2^-(1024 - 2^-1/(c(24,10)))) is more accurate.
  - The error message for not finding vignette files when weaving has correct
    file sizes now. (Thanks to Sebastian Meyer's PR#18154.)
  - dnbinom(20, <large>, 1) now correctly gives 0, and similar cases are more
    accurate with underflow precaution. (Reported by Francisco Vera Alcivar in
    PR#18072.)

* Fri May 21 2021 Shane Sturrock <shane.sturrock@gmail.com> - 4.1.0-1
- FUTURE DIRECTIONS
  - It is planned that the 4.1.x series will be the last to support 32-bit
    Windows, with production of binary packages for that series continuing
    until early 2023.
- SIGNIFICANT USER-VISIBLE CHANGES
  - Data set esoph in package datasets now provides the correct numbers of
    controls; previously it had the numbers of cases added to these. (Reported
    by Alexander Fowler in PR#17964.)
- NEW FEATURES
  - require(pkg, quietly = TRUE) is quieter and in particular does not warn if
    the package is not found.
  - www.omegahat.net is no longer one of the repositories known by default to
    setRepositories(). (Nowadays it only provides source packages and is often
    unavailable.)
  - Function package_dependencies() (in package tools) can now use different
    dependency types for direct and recursive dependencies.
  - The checking of the size of tarball in R CMD check --as-cran <pkg> may be
    tweaked via the new environment variable
    _R_CHECK_CRAN_INCOMING_TARBALL_THRESHOLD_, as suggested in PR#17777 by Jan
    Gorecki.
  - Using c() to combine a factor with other factors now gives a factor, an
    ordered factor when combining ordered factors with identical levels.
  - apply() gains a simplify argument to allow disabling of simplification of
    results.
  - The format() method for class "ftable" gets a new option justify.
    (Suggested by Thomas Soeiro.)
  - New ...names() utility. (Proposed by Neal Fultz in PR#17705.)
  - type.convert() now warns when its as.is argument is not specified, as the
    help file always said it should. In that case, the default is changed to
    TRUE in line with its change in read.table() (related to stringsAsFactor)
    in R 4.0.0.
  - When printing list arrays, classed objects are now shown via their format()
    value if this is a short enough character string, or by giving the first
    elements of their class vector and their length.
  - capabilities() gets new entry "Rprof" which is TRUE when R has been
    configured with the equivalent of --enable-R-profiling (as it is by
    default). (Related to Michael Orlitzky's report PR#17836.)
  - str(xS4) now also shows extraneous attributes of an S4 object xS4.
  - Rudimentary support for vi-style tags in rtags() and R CMD rtags has been
    added. (Based on a patch from Neal Fultz in PR#17214.)
  - checkRdContents() is now exported from tools; it and also checkDocFiles()
    have a new option chkInternal allowing to check Rd files marked with
    keyword "internal" as well. The latter can be activated for R CMD check via
    environment variable _R_CHECK_RD_INTERNAL_TOO_.
  - New functions numToBits() and numToInts() extend the raw conversion
    utilities to (double precision) numeric.
  - Functions URLencode() and URLdecode() in package utils now work on vectors
    of URIs. (Based on patch from Bob Rudis submitted with PR#17873.)
  - path.expand() can expand ~user on most Unix-alikes even when readline is
    not in use. It tries harder to expand ~, for example should environment
    variable HOME be unset.
  - For HTML help (both dynamic and static), Rd file links to help pages in
    external packages are now treated as references to topics rather than file
    names, and fall back to a file link only if the topic is not found in the
    target package. The earlier rule which prioritized file names over topics
    can be restored by setting the environment variable
    _R_HELP_LINKS_TO_TOPICS_ to a false value.
  - c() now removes NULL arguments before dispatching to methods, thus
    simplifying the implementation of c() methods, but for back compatibility
    keeps NULL when it is the first argument. (From a report and patch proposal
    by Lionel Henry in PR#17900.)
  - Vectorize()'s result function's environment no longer keeps unneeded
    objects.
  - Function ...elt() now propagates visibility consistently with ..n. (Thanks
    to Lionel Henry's PR#17905.)
  - capture.output() no longer uses non-standard evaluation to evaluate its
    arguments. This makes evaluation of functions like parent.frame() more
    consistent. (Thanks to Lionel Henry's PR#17907.)
  - packBits(bits, type="double") now works as inverse of numToBits(). (Thanks
    to Bill Dunlap's proposal in PR#17914.)
  - curlGetHeaders() has two new arguments, timeout to specify the timeout for
    that call (overriding getOption("timeout")) and TLS to specify the minimum
    TLS protocol version to be used for https:// URIs (inter alia providing a
    means to check for sites using deprecated TLS versions 1.0 and 1.1).
  - For nls(), an optional constant scaleOffset may be added to the denominator
    of the relative offset convergence test for cases where the fit of a model
    is expected to be exact, thanks to a proposal by John Nash. nls(*,
    trace=TRUE) now also shows the convergence criterion.
  - Numeric differentiation via numericDeriv() gets new optional arguments eps
    and central, the latter for taking central divided differences. The latter
    can be activated for nls() via nls.control(nDcentral = TRUE).
  - nls() now passes the trace and control arguments to getInitial(), notably
    for all self-starting models, so these can also be fit in zero-noise
    situations via a scaleOffset. For this reason, the initial function of a
    selfStart model must now have ... in its argument list.
  - bquote(splice = TRUE) can now splice expression vectors with attributes:
    this makes it possible to splice the result of parse(keep.source = TRUE).
    (Report and patch provided by Lionel Henry in PR#17869.)
  - textConnection() gets an optional name argument.
  - get(), exists(), and get0() now signal an error if the first argument has
    length greater than 1. Previously additional elements were silently
    ignored. (Suggested by Antoine Fabri on R-devel.)
  - R now provides a shorthand notation for creating functions, e.g. \(x) x + 1
    is parsed as function(x) x + 1.
  - R now provides a simple native forward pipe syntax |>. The simple form of
    the forward pipe inserts the left-hand side as the first argument in the
    right-hand side call. The pipe implementation as a syntax transformation was
    motivated by suggestions from Jim Hester and Lionel Henry.
  - all.equal(f, g) for functions now by default also compares their
    environment(.)s, notably via new all.equal method for class function.
    Comparison of nls() fits, e.g., may now need all.equal(m1, m2,
    check.environment = FALSE).
  - .libPaths() gets a new option include.site, allowing to not include the
    site library. (Thanks to Dario Strbenac's suggestion and Gabe Becker's
    PR#18016.)
  - Lithuanian translations are now available. (Thanks to Rimantas Žakauskas.)
  - names() now works for DOTSXP objects. On the other hand, in ‘R-lang’, the R
    language manual, we now warn against relying on the structure or even
    existence of such dot-dot-dot objects.
  - all.equal() no longer gives an error on DOTSXP objects.
  - capabilities("cairo") now applies only to the file-based devices as it is
    now possible (if very unusual) to build R with Cairo support for those but
    not for X11().
  - There is optional support for tracing the progress of loadNamespace() — see
    its help.
  - (Not Windows.) l10n_info() reports an additional element, the name of the
    encoding as reported by the OS (which may differ from the encoding part (if
    any) of the result from Sys.getlocale("LC_CTYPE").
  - New function gregexec() which generalizes regexec() to find all disjoint
    matches and well as all substrings corresponding to parenthesized
    subexpressions of the given regular expression. (Contributed by Brodie
    Gaslam.)
  - New function charClass() in package utils to query the wide-character
    classification functions in use (such as iswprint).
  - The names of quantile()'s result no longer depend on the global
    getOption("digits"), but quantile() gets a new optional argument digits = 7
    instead.
  - grep(), sub(), regexp and variants work considerably faster for long
    factors with few levels. (Thanks to Michael Chirico's PR#18063.)
  - Provide grouping of x11() graphics windows within a window manager such as
    Gnome or Unity; thanks to a patch by Ivan Krylov posted to R-devel.
  - The split() method for class data.frame now allows the f argument to be
    specified as a formula.
  - sprintf now warns on arguments unused by the format string.
  - New palettes "Rocket" and "Mako" for hcl.colors() (approximating palettes
    of the same name from the 'viridisLite' package).
  - The base environment and its namespace are now locked (so one can no longer
    add bindings to these or remove from these).
  - Rterm handling of multi-byte characters has been improved, allowing use of
    such characters when supported by the current locale.
  - Rterm now accepts ALT+ +xxxxxxxx sequences to enter Unicode characters as
    hex digits.
  - Environment variable LC_ALL on Windows now takes precedence over LC_CTYPE
    and variables for other supported categories, matching the POSIX behaviour.
  - duplicated() and anyDuplicated() are now optimized for integer and real
    vectors that are known to be sorted via the ALTREP framework. Contributed
    by Gabriel Becker via PR#17993.
- GRAPHICS
  - The graphics engine version, R_GE_version, has been bumped to 14 and so
    packages that provide graphics devices should be reinstalled.
  - Graphics devices should now specify deviceVersion to indicate what version
    of the graphics engine they support.
  - Graphics devices can now specify deviceClip. If TRUE, the graphics engine
    will never perform any clipping of output itself.
  - The clipping that the graphics engine does perform (for both canClip = TRUE
    and canClip = FALSE) has been improved to avoid producing unnecessary
    artifacts in clipped output.
  - The grid package now allows gpar(fill) to be a linearGradient(), a
    radialGradient(), or a pattern(). The viewport(clip) can now also be a
    grob, which defines a clipping path, and there is a new viewport(mask) that
    can also be a grob, which defines a mask.
  - These new features are only supported so far on the Cairo-based graphics
    devices and on the pdf() device.
  - (Not Windows.) A warning is given when a Cairo-based type is specified for
    a png(), jpeg(), tiff() or bmp() device but Cairo is unsupported (so type =
    "Xlib" is tried instead).
  - grSoftVersion() now reports the versions of FreeType and FontConfig if they
    are used directly (not via Pango), as is most commonly done on macOS.
- C-LEVEL FACILITIES
  - The standalone ‘libRmath’ math library and R's C API now provide log1pexp()
    again as documented, and gain log1mexp().
- INSTALLATION on a UNIX-ALIKE
  - configure checks for a program pkgconf if program pkg-config is not found.
    These are now only looked for on the path (like almost all other programs)
    so if needed specify a full path to the command in PKG_CONFIG, for example
    in file ‘config.site’.
  - C99 function iswblank is required – it was last seen missing ca 2003 so the
    workaround has been removed.
  - There are new configure options --with-internal-iswxxxxx,
    --with-internal-towlower and --with-internal-wcwidth which allows the
    system functions for wide-character classification, case-switching and width
    (wcwidth and wcswidth) to be replaced by internal ones. The first has long
    been used on macOS, AIX (and Windows) but this enables it to be unselected
    there and selected for other platforms (it is the new default on Solaris).
    The second is new in this version of R and is selected by default on macOS
    and Solaris. The third has long been the default and remains so as it
    contains customizations for East Asian languages.
  - System versions of these functions are often minimally implemented
    (sometimes only for ASCII characters) and may not cover the full range of
    Unicode points: for example Solaris (and Windows) only cover the Basic
    Multilingual Plane.
  - Cairo installations without X11 are more likely to be detected by
    configure, when the file-based Cairo graphics devices will be available but
    not X11(type = "cairo").
  - There is a new configure option --with-static-cairo which is the default on
    macOS. This should be used when only static cairo (and where relevant,
    Pango) libraries are available.
  - Cairo-based graphics devices on platforms without Pango but with
    FreeType/FontConfig will make use of the latter for font selection.
- LINK-TIME OPTIMIZATION on a UNIX-ALIKE
  - Configuring with flag --enable-lto=R now also uses LTO when installing the
    recommended packages.
  - R CMD INSTALL and R CMD SHLIB have a new flag --use-LTO to use LTO when
    compiling code, for use with R configured with --enable-lto=R. For R
    configured with --enable-lto, they have the new flag --no-use-LTO.
  - Packages can opt in or out of LTO compilation via a UseLTO field in the
    ‘DESCRIPTION’ file. (As usual this can be overridden by the command-line
    flags.)
- PACKAGE INSTALLATION
  - The default C++ standard has been changed to C++14 where available (which
    it is on all currently checked platforms): if not (as before) C++11 is used
    if available otherwise C++ is not supported.
  - Packages which specify C++11 will still be installed using C++11.
  - C++14 compilers may give deprecation warnings, most often for
    std::random_shuffle (deprecated in C++14 and removed in C++17). Either
    specify C++11 (see ‘Writing R Extensions’) or modernize the code and if
    needed specify C++14. The latter has been supported since R 3.4.0 so the
    package's ‘DESCRIPTION’ would need to include something like 
        Depends: R (>= 3.4)
- UTILITIES
  - R CMD check can now scan package functions for bogus return statements,
    which were possibly intended as return() calls (wish of PR#17180, patch by
    Sebastian Meyer). This check can be activated via the new environment
    variable _R_CHECK_BOGUS_RETURN_, true for --as-cran.
  - R CMD build omits tarballs and binaries of previous builds from the
    top-level package directory. (PR#17828, patch by Sebastian Meyer.)
  - R CMD check now runs sanity checks on the use of LazyData, for example that
    a ‘data’ directory is present and that LazyDataCompression is not specified
    without LazyData and has a documented value. For packages with large
    LazyData databases without specifying LazyDataCompression, there is a
    reference to the code given in ‘Writing R Extensions’ §1.1.6 to test the
    choice of compression (as in all the CRAN packages tested a non-default
    method was preferred).
  - R CMD build removes LazyData and LazyDataCompression fields from the
    ‘DESCRIPTION’ file of packages without a ‘data’ directory.
- ENCODING-RELATED CHANGES
  - The parser now treats \Unnnnnnnn escapes larger than the upper limit for
    Unicode points (\U10FFFF) as an error as they cannot be represented by
    valid UTF-8.
  - Where such escapes are used for outputting non-printable (including
    unassigned) characters, 6 hex digits are used (rather than 8 with leading
    zeros). For clarity, braces are used, for example \U{0effff}.
  - The parser now looks for non-ASCII spaces on Solaris (as previously on most
    other OSes).
  - There are warnings (including from the parser) on the use of unpaired
    surrogate Unicode points such as \uD834. (These cannot be converted to
    valid UTF-8.)
  - Functions nchar(), tolower(), toupper() and chartr() and those using
    regular expressions have more support for inputs with a marked Latin-1
    encoding.
  - The character-classification functions used (by default) to replace the
    system iswxxxxx functions on Windows, macOS and AIX have been updated to
    Unicode 13.0.0.
  - The character-width tables have been updated to include new assignments in
    Unicode 13.0.0.
  - The code for evaluating default (extended) regular expressions now uses the
    same character-classification functions as the rest of R (previously they
    differed on Windows, macOS and AIX).
  - There is a build-time option to replace the system's wide-character wctrans
    C function by tables shipped with R: use configure option
    --with-internal-towlower or (on Windows) -DUSE_RI18N_CASE in CFLAGS when
    building R. This may be needed to allow tolower() and toupper() to work with
    Unicode characters beyond the Basic Multilingual Plane where not supported
    by system functions (e.g. on Solaris where it is the new default).
  - R is more careful when truncating UTF-8 and other multi-byte strings that
    are too long to be printed, passed to the system or libraries or placed
    into an internal buffer. Truncation will no longer produce incomplete
    multibyte characters.
- DEPRECATED AND DEFUNCT
  - Using the non-default method = "internal" for http:// and ftp:// URIs is
    deprecated for download.file and url.
  - Function plclust() from the package stats and package.dependencies(),
    pkgDepends(), getDepList(), installFoundDepends(), and vignetteDepends()
    from package tools are defunct.
  - Defunct functions checkNEWS() and readNEWS() from package tools and
    CRAN.packages() from utils have been removed.
  - R CMD config CXXCPP is defunct (it was deprecated in R 3.6.2).
  - parallel::detectCores() drops support for Irix (retired in 2013).
  - The LINPACK argument to chol.default(), chol2inv(), solve.default() and
    svd() has been defunct since R 3.1.0. It was silently ignored up to R 4.0.3
    but now gives an error.
  - Subsetting/indexing, such as ddd[*] or ddd$x on a DOTSXP (dot-dot-dot)
    object ddd has been disabled; it worked by accident only and was
    undocumented.
- BUG FIXES
  - make check-devel works again in an R build configured with
    --without-recommended-packages.
  - Many more C-level allocations (mainly by malloc and strdup) are checked for
    success with suitable alternative actions.
  - Bug fix for replayPlot(); this was turning off graphics engine display list
    recording if a recorded plot was replayed in the same session. The impact
    of the bug became visible if resize the device after replay OR if attempted
    another savePlot() after replay (empty display list means empty screen on
    resize or empty saved plot).
  - R CMD check etc now warn when a package exports non-existing S4 classes or
    methods, also in case of no “methods” presence. (Reported by Alex Bertram;
    reproducible example and patch by Sebastian Meyer in PR#16662.)
  - boxplot() now also accepts calls for labels such as ylab, the same as
    plot(). (Reported by Marius Hofert.)
  - The help page for xtabs() now correctly states that addNA is setting
    na.action = na.pass among others. (Reported as PR#17770 by Thomas Soeiro.)
  - The R CMD check <pkg> gives a longer and more comprehensible message when
    ‘DESCRIPTION’ misses dependencies, e.g., in Imports:. (Thanks to the
    contributors of PR#17179.)
  - update.default() now calls the generic update() on the formula to work
    correctly for models with extended formulas. (As reported and suggested by
    Neal Fultz in PR#17865.)
  - The horizontal position of leaves in a dendrogram is now correct also with
    center = FALSE. (PR#14938, patch from Sebastian Meyer.)
  - all.equal.POSIXt() no longer warns about and subsequently ignores
    inconsistent "tzone" attributes, but describes the difference in its return
    value (PR#17277). This check can be disabled via the new argument
    check.tzone = FALSE as suggested by Sebastian Meyer.
  - as.POSIXct() now populates the "tzone" attribute from its tz argument when
    x is a logical vector consisting entirely of NA values.
  - x[[2^31]] <- v now works. (Thanks to the report and patch by Suharto
    Anggono in PR#17330.)
  - In log-scale graphics, axis() ticks and label positions are now computed
    more carefully and symmetrically in their range, typically providing more
    ticks, fulfilling wishes in PR#17936. The change really corresponds to an
    improved axisTicks() (package grDevices), potentially influencing grid and
    lattice, for example.
  - qnorm(<very large negative>, log.p=TRUE) is now correct to at least five
    digits where it was catastrophically wrong, previously.
  - sum(df) and similar "Summary"- and "Math"-group member functions now work
    for data frames df with logical columns, notably also of zero rows.
    (Reported to R-devel by Martin “b706”.)
  - unsplit() had trouble with tibbles due to unsound use of rep(NA,
    len)-indexing, which should use NA_integer_ (Reported to R-devel by Mario
    Annau.)
  - pnorm(x, log.p = TRUE) underflows to -Inf slightly later.
  - show(<hidden S4 generic>) prints better and without quotes for non-hidden
    S4 generics.
  - read.table() and relatives treated an "NA" column name as missing when
    check.names = FALSE PR#18007.
  - Parsing strings containing UTF-16 surrogate pairs such as "\uD834\uDD1E"
    works better on some (uncommon) platforms. sprintf("%X",
    utf8ToInt("\uD834\uDD1E")) should now give "1D11E" on all platforms.
  - identical(x,y) is no longer true for differing DOTSXP objects, fixing
    PR#18032.
  - str() now works correctly for DOTSXP and related exotics, even when these
    are doomed.
  - Additionally, it no longer fails for lists with a class and “irregular”
    method definitions such that e.g. lapply(*) will necessarily fail, as
    currently for different igraph objects.
  - Too long lines in environment files (e.g. Renviron) no longer crash R. This
    limit has been increased to 100,000 bytes. (PR#18001.)
  - There is a further workaround for FreeType giving incorrect italic font
    faces with cairo-based graphics devices on macOS.
  - add_datalist(*, force = TRUE) (from package tools) now actually updates an
    existing ‘data/datalist’ file for new content. (Thanks to a report and
    patch by Sebastian Meyer in PR#18048.)
  - cut.Date() and cut.POSIXt() could produce an empty last interval for breaks
    = "months" or breaks = "years". (Reported as PR#18053 by Christopher
    Carbone.)
  - Detection of the encoding of ‘regular’ macOS locales such as en_US (which
    is UTF-8) had been broken by a macOS change: fortunately these are now
    rarely used with en_US.UTF-8 being preferred.
  - sub() and gsub(pattern, repl, x, *) now keep attributes of x such as
    names() also when pattern is NA (PR#18079).
  - Time differences ("difftime" objects) get a replacement and a rep() method
    to keep "units" consistent. (Thanks to a report and patch by Nicolas
    Bennett in PR#18066.)
  - The \RdOpts macro, setting defaults for \Sexpr options in an Rd file, had
    been ineffective since R 2.12.0: it now works again. (Thanks to a report
    and patch by Sebastian Meyer in PR#18073.)
  - mclapply and pvec no longer accidentally terminate parallel processes
    started before by mcparallel or related calls in package parallel
    (PR#18078).
  - grep and other functions for evaluating (extended) regular expressions
    handle in Unicode also strings not explicitly flagged UTF-8, but flagged
    native when running in UTF-8 locale.
  - Fixed a crash in fifo implementation on Windows (PR#18031).
  - Binary mode in fifo on Windows is now properly detected from argument open
    (PR#15600, PR#18031).

* Thu Apr 15 2021 Shane Sturrock <shane.sturrock@gmail.com> - 4.0.5-1
- BUG FIXES
  - The change to the internal table in R 4.0.4 for iswprint has been reverted:
    it contained some errors in printability of ‘East Asian’ characters.
  - For packages using LazyData, R CMD build ignored the --resave-data option
    and the BuildResaveData field of the ‘DESCRIPTION’ file (in R versions
    4.0.0 to 4.0.4).

* Fri Mar 05 2021 Shane Sturrock <shane.sturrock@gmail.com> - 4.0.4-1
- NEW FEATURES
  - File ‘share/texmf/tex/latex/jss.cls’ has been updated to work with LaTeX
    versions since Oct 2020.
  - Unicode character width tables (as used by nchar(, type = "w")) have been
    updated to Unicode 12.1 by Brodie Gaslam (PR#17781), including many emoji.
  - The internal table for iswprint (used on Windows, macOS and AIX) has been
    updated to include many recent Unicode characters.
- INSTALLATION on a UNIX-ALIKE
  - If an external BLAS is specified by --with-blas=foo or via environment
    variable BLAS_LIBS is not found, this is now a configuration error. The
    previous behaviour was not clear from the documentation: it was to continue
    the search as if --with-blas=yes was specified.
- BUG FIXES
  - all.equal(x,y) now “sees” the two different NAs in factors, thanks to Bill
    Dunlap and others in PR#17897.
  - (~ NULL)[1] and similar formula subsetting now works, thanks to a report
    and patch by Henrik Bengtsson in PR#17935. Additionally, subsetting leaving
    an empty formula now works too, thanks to suggestions by Suharto Anggono.
  - .traceback(n) keeps source references again, as before R 4.0.0, fixing a
    regression; introduced by the PR#17580, reported including two patch
    proposals by Brodie Gaslam.
  - unlist(plst, recursive=FALSE) no longer drops content for pairlists with
    list components, thanks to the report and patch by Suharto Anggono in
    PR#17950.
  - iconvlist() now also works on MUSL based (Linux) systems, from a report and
    patch suggestion by Wesley Chan in PR#17970.
  - round() and signif() no longer tolerate wrong argument names, notably in
    1-argument calls; reported by Shane Mueller on R-devel (mailing list);
    later reported as PR#17976.
  - .Machine has longdouble.* elements only if capabilities("long.double") is
    true, as documented. (Previously they were included if the platform had
    long double identical to double, as ARM does.)
  - p.adjust(numeric(), n=0) now works, fixing PR#18002.
  - identical(x,y) no longer prints "Unknown Type .." for typeof(x) == "..."
    objects.
  - Fix (auto-)print()ing of named complex vectors, see PR#17868 and PR#18019.
  - all.equal(<language>, <...>) now works, fixing PR#18029.
  - as.data.frame.list(L, row.names=NULL) now behaves in line with
    data.frame(), disregarding names of components of L, fixing PR#18034,
    reported by Kevin Tappe.
  - checkRdaFiles(ff)$version is now correct also when ff contains files of
    different versions, thanks to a report and patch from Sebastian Meyer in
    PR#18041.
  - Message translation domains, e.g., for errors and warnings, are now
    correctly determined also when e.g., a base function is called from
    “top-level” function (i.e., defined in globalenv()), thanks to a patch from
    Joris Goosen fixing PR#17998.
  - macOS: Quartz device live drawing could fail (no plot is shown) if the
    system changes the drawing context after view update (often the case since
    macOS Big Sur). System log may show "CGContextDelegateCreateForContext:
    invalid context" error.

* Fri Nov 20 2020 Shane Sturrock <shane.sturrock@gmail.com> - 4.0.3-1
- NEW FEATURES:
  - On platforms using configure option ‘--with-internal-tzcode’, additional
    values "internal" and (on macOS only) "macOS" are accepted for the
    environment variable TZDIR. (See ?TZDIR.)
  - On macOS, "macOS" is used by default if the system timezone database is a
    newer version than that in the R installation.
  - When install.packages(type = "source") fails to find a package in a
    repository it mentions package versions which are excluded by their R
    version requirement and links to hints on why a package might not be found.
  - The default value for options("timeout") can be set from enviromnent
    variable R_DEFAULT_INTERNET_TIMEOUT, still defaulting to 60 (seconds) if
    that is not set or invalid.
  - This may be needed when child R processes are doing downloads, for example
    during the installation of source packages which download jars or other
    forms of data.
- LINK-TIME OPTIMIZATION on a UNIX-ALIKE:
  - There is now support for parallelized Link-Time Optimization (LTO) with GCC
    and for ‘thin’ LTO with clang via setting the ‘LTO’ macro.
  - There is support for setting a different LTO flag for the Fortran compiler,
    including to empty when mixing clang and gfortran (as on macOS). See file
    ‘config.site’.
  - There is a new ‘LTO_LD’ macro to set linker options for LTO compilation,
    for example to select an alternative linker or to parallelize thin LTO.
- DEPRECATED AND DEFUNCT:
  - The LINPACK argument to chol.default(), chol2inv(), solve.default() and
    svd() has been defunct since R 3.1.0. Using it now gives a warning which
    will become an error in R 4.1.0.
- BUG FIXES:
  - The code mitigating stack overflow with PCRE regexps on very long strings
    is enabled for PCRE2 < 10.30 also when JIT is enabled, since stack
    overflows have been seen in that case.
  - Fix to correctly show the group labels in dotchart() (which were lost in
    the ylab improvement for R 4.0.0).
  - addmargins(*,..) now also works when fn() is a local function, thanks to
    bug report and patch PR#17124 from Alex Bertram.
  - rank(x) and hence sort(x) now work when x is an object (as per
    is.object(x)) of type "raw" and provides a valid [ method, e.g., for
    gmp::as.bigz(.) numbers. chisq.test(*,simulate.p.value=TRUE) and r2dtable()
    now work correctly for large table entries (in the millions). Reported by
    Sebastian Meyer and investigated by more helpers in PR#16184.
  - Low-level socket read/write operations have been fixed to correctly signal
    communi- cation errors. Previously, such errors could lead to a segfault
    due to invalid memory access. Reported and debugged by Dmitriy Selivanov in
    PR#17850. quantile(x,pr) works more consistently for pr values slightly
    outside [0,1], thanks to Suharto Anggono’s PR#17891.
  - Further, quantile(x,prN,names=FALSE) now works even when prN contains NAs,
    thanks to Anggono’s PR#17892. Ditto for ordered factors or Date objects
    when type = 1 or 3, thanks to PR#17899.
  - Libcurl-based internet access, including curlGetHeaders(), was not
    respecting the "timeout" option. If this causes unanticipated timeouts,
    consider increasing the default by setting R_DEFAULT_INTERNET_TIMEOUT.
  - as.Date(<char>) now also works with an initial "", thanks to Michael
    Chirico’s PR#17909.
  - isS3stdGeneric(f) now detects an S3 generic also when it it is trace()d,
    thanks to Gabe Becker’s PR#17917.
  - R_allocLD() has been fixed to return memory aligned for long double type
    PR#16534.
  - fisher.test() no longer segfaults when called again after its internal
    stack has been exceeded PR#17904.
  - Accessing a long vector represented by a compact integer sequence no longer
    segfaults (reported and debugged by Hugh Parsonage).
    duplicated()nowworksalsoforstringswithmultipleencodingsinsideasinglevector
    PR#17809.
  - phyper(11,15,0,12,log.p=TRUE) no longer gives NaN; reported as PR#17271 by
    Alexey Stukalov.
  - Fix incorrect calculation in logLik.nls() PR#16100, patch from Sebastian
    Meyer. A very old bug could cause a segfault in model.matrix() when terms
    involved logical variables. Part of PR#17879.
  - model.frame.default() allowed data = 1, leading to involuntary variable
    capture (rest of PR#17879).
  - tar() no longer skips non-directory files, thanks to a patch by Sebastian
    Meyer, fixing the remaining part of PR#16716.

* Mon Aug 24 2020 Shane Sturrock <shane.sturrock@gmail.com> - 4.0.2-1
- UTILITIES:
  - R CMD check skips vignette re-building (with a warning) if the
    ‘VignetteBuilder’ package(s) are not available.
- BUG FIXES:
  - Paths with non-ASCII characters caused problems for package loading on
    Windows PR#17833.
  - Using tcltk widgets no longer crashes R on Windows.
  - source(*,echo=TRUE) no longer fails in some cases with empty lines;
    reported by Bill Dunlap in PR#17769.
  - on.exit() now correctly matches named arguments, thanks to PR#17815
    (including patch) by Brodie Gaslam.
  - regexpr(*,perl=TRUE) no longer returns incorrect positions into text
    containing characters outside of the Unicode Basic Multilingual Plane on
    Windows.

* Tue Apr 07 2020 Shane Sturrock <shane.sturrock@gmail.com> - 3.6.3-1
- CHANGES IN R 3.6.3
  - NEW FEATURES:
    - The included LAPACK has been updated to version 3.9.0 (for the included
      routines, just bug fixes).
  - BUG FIXES:
    - Fixed a C level integer overflow in rhyper(); reported by Benjamin Tyner
      in PR#17694.
    - Uses of url(gzcon(.)) needing to extend buffer size have failed (with
      HTTP/2 servers), reported by G´abor Cs´ardi.
    - predict(loess(..),se=TRUE) now errors out (instead of seg.faulting etc)
      PR#17121.
    - tools:assertCondition(.,"error") and hence assertError() no longer return
      errors twice (invisibly).
    - update(form,new) in the case of a long new formula sometimes wrongly
      eliminated the intercept from form, or (more rarely) added a garbage term
      (or seg.faulted !); the fix happened by simplifying the C-level logic of
      terms.formula(). Reported by Mathias Ambuhl in ¨ PR#16326.
    - The error message from stopifnot(..,<error producing call>) again
      contains the full "stopifnot(.......)" call: Its attempted suppression
      did not work consistently.
    - On Windows, download.file(.,,"wininet",headers=character()) would fail;
      reported with patch proposal by Kevin Ushey in PR#17710.
- CHANGES IN R 3.6.2
  - NEW FEATURES:
    - runmed(x,*) gains a new option na.action determining how to handle NaN or
      NA in x.
    - dotchart() gains new options ann, xaxt, frame.plot and log.
  - INSTALLATION on a UNIX-ALIKE:
    - Detection of the C stack direction has been moved from run-time to
      configure: this is safer with LTO builds and allows the detection to be
      overridden – see file 'config.site'.
    - Source-code changes enable installation on platforms using gcc
      -fno-common (the expected default for gcc 10.x).
  - C-LEVEL FACILITIES:
    - installTrChar (which is nowadays is wrapped by installChar) is defined in
      'Rinternals.h'. (Neither are part of the API.)
  - PACKAGE INSTALLATION:
    - Header 'Rconfig.h' contains the value of FC_LEN_T deduced at installation
      which is used by the prototypes in headers 'R_ext/BLAS.h' and
      'R_ext/Lapack.h' but to avoid extensive breakage this is only exposed when
      USE_FC_LEN_T is defined. If a package's C/C++ calls to BLAS/LAPACK allow
      for the 'hidden' arguments used by most Fortran compilers to pass the
      lengths of Fortran character arguments, define USE_FC_LEN_T and include
      'Rconfig.h' (possibly via 'R.h') before including 'R_ext/BLAS.h' or
      'R_ext/Lapack.h'.
    - A package with Fortran source code and perhaps C (but not C++) sources
      can request for its shared object/DLL to be linked by the Fortran
      compiler by including a line USE_FC_TO_LINK= in 'src/Makevars[.win]' and
      using $(SHLIB_OPENMP_FFLAGS) as part of PKG_LIBS. The known reason for
      doing so is a package which uses Fortran (only) OpenMP on a platform
      where the Fortran OpenMP runtime is incompatible with the C one (e.g.
      gfortran 9.x with clang).
  - UTILITIES:
    - R CMD check has a new option to mitigate checks leaving files/directories
      in '/tmp'. See the 'R Internals' manual – this is part of --as-cran.
  - Windows:
    - The default standard for C++ in package installation is C++11 (as it has
      been on other platforms where available since R 3.6.0: the default
      toolchain on Windows was defaulting to C++98).
  - DEPRECATED AND DEFUNCT:
    - Support for specifying C++98 in package installation is deprecated.
    - Support in R CMD config for 'F77', 'FCPIFCPLAGS', 'CPP', 'CXXCPP' and
      'CXX98' and similar is deprecated. ('CPP' is found from the system make
      and may well not be set.) Use '$CC -E' and '$CXX -E' instead of 'CPP' and
      'CXXCPP.
  - BUG FIXES:
    - runmed(x,*) when x contains missing values now works consistently for
      both algorithm="Stuetzle" and "Turlach", and no longer segfaults for
      "Turlach", as reported by Hilmar Berger.
    - apply(diag(3),2:3,mean) now gives a helpful error message.
    - dgamma(x,shape,log=TRUE) now longer overflows to Inf for shape < 1 and
      very small x, fixing PR#17577, reported by Jonathan Rougier.
    - Buffer overflow in building error messages fixed. Reported by Benjamin
      Tremblay.
    - options(str = .) is correctly initialized at package utils load time,
      now. A consequence is that str() in scripts now is more consistent to
      interactive use, e.g., when displaying function(**) argument lists.
    - as.numeric(<call>) now gives correct error message.
    - Printing ls.str() no longer wrongly shows "<missing>" in rare cases.
    - Auto-printing S4 objects no longer duplicates the object, for faster
      speed and reduced memory consumption. Reported by Aaron Lun.
    - pchisq(<LRG>,<LRG>,ncp=100) no longer takes practically forever in some
      cases. Hence ditto for corresponding qchisq() calls.
    - x %% L for finite x no longer returns NaN when L is infinite, nor suffers
      from cancellation for large finite L, thanks to Long Qu's PR#17611.
      Analogously, x %/% L and L %/% x suffer less from cancellation and return
      values corresponding to limits for large L.
    - grepl(NA,*) now returns logical as documented.
    - options(warn=1e11) is an error now, instead of later leading to C stack
      overflow because of infinite recursion.
    - R_tryCatch no longer transfers control for all conditions. Reported and
      patch provided by Lionel Henry in PR#17617.
    - format(object.size(.),digits=NULL) now works, fixing PR#17628 reported by
      Jonathan Carroll.
    - get_all_vars(f,d) now also works for cases, e.g. where d contains a
      matrix. Reported by Simon Wood in 2009 and patch provided by Ben Bolker
      in PR#13624. Additionally, it now also works when some variables are data
      frames, fixing PR#14905, reported by Patrick Breheny.
    - barplot() could get spacings wrong if there were exactly two bars
      PR#15522. Patch by Michael Chirico.
    - power.t.test() works in more cases when returning values of n smaller
      than 2.
    - dotchart(*,pch=.,groups=.) now works better. Reported by Robert and
      confirmed by Nic Rochette in PR#16953.
    - canCoerce(obj,cl) no longer assumes length(class(obj)) == 1.
    - plot.formula(*,subset = *) now also works in a boundary case reported by
      Robert Schlicht (TU Dresden).
    - readBin() and writeBin() of a rawConnection() now also work in large
      cases, thanks to a report and proposal by Taeke Harkema in PR#17665.

* Fri Jul 26 2019 Shane Sturrock <shane.sturrock@gmail.com> - 3.6.1-1
- UTILITIES
  - R CMD config knows the values of AR and RANLIB, often set for LTO builds.
- DEPRECATED AND DEFUNCT
  - The use of a character vector with .Fortran() is formally deprecated and
    gives a non-portability warning. (It has long been strongly discouraged in
    'Writing R Extensions'.)
- BUG FIXES
  - On Windows, GUI package installation via menuInstallPkgs() works again,
    thanks to Len Weil's and Duncan Murdoch's PR#17556.
  - R CMD check on data() fixing PR#17558 thanks to Duncan Murdoch.
  - quasi(*, variance = list(..)) now works more efficiently, and should work
    in all cases fixing PR#17560. Further, quasi(var = mu(1-mu)) and quasi(var
    = "mu ^ 3") now work, and quasi(variance = "log(mu)") now gives a correct
    error message.
  - Creation of lazy loading database during package installation is again
    robust to Rprofile changing the current working directory (PR#17559).
  - boxplot(y ~ f, horizontal=TRUE) now produces correct x- and y-labels.
  - rbind.data.frame() allows to keep <NA> levels from factor columns
    (PR#17562) via new option factor.exclude.
  - Additionally, it works in one more case with matrix-columns which had been
    reported on 2017-01-16 by Krzysztof Banas.
  - Correct messaging in C++ pragma checks in tools code for R CMD check,
    fixing PR#17566 thanks to Xavier Robin.
  - print()ing and auto-printing no longer differs for functions with a user
    defined print.function, thanks to Bill Dunlap's report.
  - On Windows, writeClipboard(.., format = <n>) now does correctly pass format
    to the underlying C code, thanks to a bug report (with patch) by Jenny
    Bryan.
  - as.data.frame() treats 1D arrays the same as vectors, PR#17570.
  - Improvements in smoothEnds(x, *) working with NAs (towards runmed() working
    in that case, in the next version of R).
  - vcov(glm(<quasi>), dispersion = *) works correctly again, fixing PR#17571
    thanks to Pavel Krivitsky.
  - R CMD INSTALL of binary packages on Windows now works also with
    per-directory locking.
  - R CMD INSTALL and install.packages() on Windows are now more robust against
    a locked file in an earlier installation of the package to be installed.
    The default value of option install.lock on Windows has been changed to 
    TRUE.
  - On Unix alikes (when readline is active), only expand tilde (~) file names
    starting with a tilde, instead of almost all tildes.
  - In R documentation ('*.Rd') files, \item [..] is no longer treated
    specially when rendered in LaTeX and hence pdf, but rather shows the
    brackets in all cases.

* Tue Jun 11 2019 Shane Sturrock <shane.sturrock@gmail.com> - 3.6.0-1
- SIGNIFICANT USER-VISIBLE CHANGES
  - Serialization format version 3 becomes the default for serialization and
    saving of the workspace (save(), serialize(), saveRDS(),
    compiler::cmpfile()). Serialized data in format 3 cannot be read by
    versions of R prior to version 3.5.0. Serialization format version 2 is 
    still supported and can be selected by version = 2 in the
    save/serialization functions. The default can be changed back for the whole
    R session by setting environment variables R_DEFAULT_SAVE_VERSION and
    R_DEFAULT_SERIALIZE_VERSION to 2. For maximal back-compatibility, files
    'vignette.rds' and 'partial.rdb' generated by R CMD build are in
    serialization format version 2, and resave by default produces files in
    serialization format version 2 (unless the original is already in format
    version 3).
  - The default method for generating from a discrete uniform distribution
    (used in sample(), for instance) has been changed. This addresses the fact,
    pointed out by Ottoboni and Stark, that the previous method made sample()
    noticeably non-uniform on large populations. See PR#17494 for a discussion.
    The previous method can be requested using RNGkind() or RNGversion() if
    necessary for reproduction of old results. Thanks to Duncan Murdoch for
    contributing the patch and Gabe Becker for further assistance.
  - The output of RNGkind() has been changed to also return the 'kind' used by
    sample().
- NEW FEATURES
  - Sys.setFileTime() has been vectorized so arguments path and time of length
    greater than one are now supported.
  - axis() gets new option gap.axis = NA for specifying a multiplication factor
    for the minimal “gap” (distance) between axis labels drawn. Its default is
    1 for labels parallel to the axis, and 0.25 for perpendicular ones.
  - Perpendicular labels no longer overlap, fixing bug PR#17384.
  - The default method of plot() gains new arguments xgap.axis = NA and
    ygap.axis = NA to be passed to the x– and y– axis(.., gap.axis=*) calls.
  - removeSource() now works not only for functions but also for some language
    objects.
  - as.call(), rep.int(), rep_len() and nchar() dispatch internally.
  - is(object, class2) looks for class2 in the calling namespace after looking
    in the namespace of class(object).
  - extendrange(.., f) with a length-2 f now extends separately to the left and
    the right.
  - lengths() dispatches internally to S4 methods.
  - download.file() on Windows now uses URLdecode() to determine the file
    extension, and uses binary transfer (mode = "wb") also for file extension
    '.rds'.
  - The help page for download.file() now contains the same information on all
    platforms.
  - Setting C locale for collation via environment variables LC_ALL and
    LC_COLLATE and via a call to Sys.setlocale() now takes precedence over
    environment variable R_ICU_LOCALE.
  - There is a new function, nullfile(), to give the file name of the null
    system device (e.g., '/dev/null') on the current platform.
  - There are two new options, keep.parse.data and keep.parse.data.pkgs, which
    control whether parse data are included into sources when keep.source or
    keep.source.pkgs is TRUE. By default, keep.parse.data.pkgs is now FALSE,
    which changes previous behavior and significantly reduces space and time
    overhead when sources are kept when installing packages.
  - In rapply(x, ..), x can also be “list-like” and of length >= 2^{31}.
  - trimws() gets new optional whitespace argument, allowing more extensive
    definitions of “space”, such as including Unicode spaces (as wished in
    PR#17431).
  - weighted.mean() no longer coerces the weights to a double/numeric vector,
    since sum() now handles integer overflow. This makes weighted.mean() more
    polymorphic and endomorphic, but be aware that the results are no longer
    guaranteed to be a vector of type double.
  - When loading namespaces, S3 method registrations which overwrite previous
    registrations are now noted by default (using packageStartupMessage()).
  - compiler::cmpfile() gains a version argument, for use when the output file
    should be saved in serialization format 2.
  - The axis labeling in the default method of pairs() may now be toggled by
    new options horOdd and verOdd.
  - (Not Windows nor macOS.) Package tcltk now supports an environment variable
    R_DONT_USE_TK which if set disables Tk initialization. This is intended for
    use to circumvent errors in loading the package, e.g. with recent Linux
    running under an address sanitizer.
  - The numeric method of all.equal() gets optional arguments countEQ and
    formatFUN. If countEQ is true, the mean error is more sensible when many
    entries are equal.
  - outer(x,y, FUN = "*") is more efficient using tcrossprod(u,v) instead of u
    %*% t(v).
  - vcov(<mlm>) is more efficient via new optional arguments in summary.mlm().
  - The default method of summary() gets an option to choose the kind of
    quantile()s to use; wish of PR#17438.
  - Fitting multiple linear models via lm() does work with matrix offsets, as
    suggested in PR#17407.
  - The new functions mem.maxVSize() and mem.maxMSize() allow the maximal size
    of the vector heap and the maximal number of nodes allowed in the current R
    process to be queried and set.
  - news() gains support for 'NEWS.md' files.
  - An effort has been started to have our reference manuals, i.e., all help
    pages. show platform-independent information (rather than Windows or
    Unix-alike specifics visible only on that platform). Consequently, the
    Windows version of X11() / x11() got identical formal arguments to the Unix
    one.
  - sessionInfo()$running has been factored out in a new variable osVersion.
  - slice.index() now also works for multi-dimensional margins.
  - untar() used with an external tar command assumes this supports
    decompression including xz and automagically detecting the compression
    type. This has been true of all mainstream implementations since 2009 (for
    GNU tar, since version 1.22): older implementations are still supported via
    the new argument support_old_tars whose default is controlled by environment
    variable R_SUPPORT_OLD_TARS. (It looks like NetBSD and OpenBSD have 'older'
    tar commands for this purpose.)
  - The new function asplit() allow splitting an array or matrix by its
    margins.
  - New functions errorCondition() and warningCondition() provide a convenient
    way to create structured error and warning objects.
  - .Deprecated() now signals a warning of class "deprecatedWarning", and
    .Defunct() now signals an error of class "defunctError".
  - Many 'package not found' errors are now signaled as errors of class
    "packageNotFoundError".
  - As an experimental feature, when loadNamespace() fails because the
    requested package is not available the error is initially signaled with a
    retry_loadNamespace restart available. This allows a calling handler to try
    to install the package and continue.
  - S3method() directives in 'NAMESPACE' can now also be used to perform
    delayed S3 method registration.
  - Experimentally, setting environment variable _R_CHECK_LENGTH_1_LOGIC2_ will
    lead to warnings (or errors if the variable is set to a 'true' value) when
    && or || encounter and use arguments of length more than one.
  - Added "lines" and "chars" coordinate systems to grconvertX() and
    grconvertY().
  - getOption() is more efficient notably for the rare case when called with
    two arguments, from several contributors in PR#17394.
  - In .col(dim) and .row(dim), dim now may also be an integer-valued "double".
  - sQuote() and dQuote() get an explicit q argument with obvious default
    instead of using getOption("fancyQuotes") implicitly and unconditionally.
  - unzip() can list archives with comments and with spaces in file names even
    using an external unzip command.
  - Command line completion has a new setting rc.settings(dots = FALSE) to
    remove ... from the list of possible function arguments.
  - library() no longer checks packages with compiled code match
    R.version$platform. loadNamespace() never has, and increasingly the
    'canonical name' does not reflect the important characteristics of compiled
    code.
  - The primitive functions drop() and unclass() now avoid duplicating their
    data for atomic vectors that are large enough, by returning ALTREP wrapper
    objects with adjusted attributes. R-level assignments to change attributes
    will also use wrapper objects to avoid duplicating data for larger atomic
    vectors. R functions like structure() and unname() will therefore not
    duplicate data in these settings. Generic vectors as produced by list() are
    not yet covered by this optimization but may be in due course.
  - In formals(), envir becomes an optional argument instead of being
    hardwired.
  - Instead of signalling an error for an invalid S4 object x, str(x) now gives
    a warning and subsequently still shows most parts of x, e.g., when slots
    are missing.
  - gamma(x) and lgamma(x) no longer warn when correctly returning Inf or
    underflowing to zero. This helps maximum likelihood and similar
    computations.
  - convertColor() is now vectorized, so a lot faster for converting many
    colours at once. The new argument vectorized to colorConverter() ensures
    that non-vectorized colour converters still work. (Thanks to Brodie Gaslam.)
  - download.file() and url() get new argument headers for custom HTTP headers,
    e.g., allowing to perform basic http authentication, thanks to a patch
    contributed by Gábor Csárdi.
  - File-based connection functions file(), gzfile(), bzfile() and xzfile() now
    signal an error when used on a directory.
  - For approx(), splinefun() etc, a new setting ties = c("ordered", <fun>)
    allows skipping the sorting and still treat ties.
  - format(x) gives a more user friendly error message in the case where no
    method is defined. A minimal method is provided in format.default(x) when
    isS4(x) is true.
  - which(x) now also works when x is a long vector, thanks to Suharto
    Anggono's PR#17201. NB: this may return a double result, breaking the
    previous guarantee of an integer result.
  - seq.default() is more careful to return an integer (as opposed to double)
    result when its arguments are large and/or classed objects; see comment #9
    of Suharto Anggono's PR#17497.
  - The plot() method for lm and glm fits, plot.lm(), gains a new option
    iter.smooth with a default of 0 for binomial fits, no longer down-weighting
    when smoothing the residuals.
  - zip() passes its list of files via standard input to the external command
    when too long for the command line (on some platforms).
  - data() gains an overwrite argument.
  - t.test() now also returns the standard error (in list component stderr).
  - model.matrix(*, contrasts.arg = CC) now warns about invalid contrasts.args.
  - Performance of substr() and substring() has been improved.
  - stopifnot() has been simplified thanks to Suharto Anggono's proposals to
    become considerably faster for cheap expressions.
  - The default 'user agent' has been changed when accessing http:// and
    https:// sites using libcurl. (A site was found which caused libcurl to
    infinite-loop with the previous default.)
  - sessionInfo() now also contains RNGkind() and prints it when it differs
    from the default; based on a proposal and patch by Gabe Becker in PR#17535.
    Also, RNGversion(getRversion()) works directly.
  - library() and require() now allow more control over handling search path
    conflicts when packages are attached. The policy is controlled by the new
    conflicts.policy option.
  - barplot() gets a formula method, thanks to a patch proposal by Arni
    Magnusson in PR#17521.
  - pmax() and pmin(x) now also work for long vectors, thanks to Suharto
    Anggono's PR#17533.
  - bxp() now warns when omitting duplicated arguments.
  - New hcl.colors() function to provide wide range of HCL-based colour
    palettes with much better perceptual properties than the existing
    RGB/HSV-based palettes like rainbow().
  - Also a new hcl.pals() function to list available palette names for
    hcl.colors().
  - The default colours for image() and filled.contour() are now based on
    hcl.colors().
  - The palette-generating functions rainbow(), gray.colors(), etc. get a new
    rev argument to facilitate reversing the order of colors.
  - New str2lang() and str2expression() as streamlined versions of
    parse(text=., keep.source=FALSE) allow to abstract typical call
    constructions, e.g., in formula manipulations. (Somewhat experimental)
  - Add update_PACKAGES() for incrementally updating a package repository
    index, instead of rebuilding the index from scratch. Thanks to Gabe Becker
    in PR#17544 for the patch, based on part of his switchr package.
- PACKAGE INSTALLATION
  - Source package installation is by default 'staged': the package is
    installed into a temporary location under the final library directory and
    moved into place once the installation is complete. The benefit is that
    partially-installed packages are hidden from other R sessions.
  - The overall default is set by environment variable R_INSTALL_STAGED. R CMD
    INSTALL has new options --staged-install and --no-staged-install, and
    packages can use the StagedInstall field in their 'DESCRIPTION' file to opt
    out. (That opt-out is a temporary measure which may be withdrawn in future.)
  - Staged installation requires either --pkglock or --lock, one of which is
    used by default.
  - The interpretation of source code with extension '.f' is changing.
    Previously this denoted FORTRAN 77 code, but current compilers no longer
    have a FORTRAN 77 mode and interpret it as 'fixed-form' Fortran 90 (or later
    where supported) code. Extensions '.f90' and '.f95' continue to indicate
    'free-form' Fortran code.
  - Legal FORTRAN 77 code is also legal fixed-form Fortran 9x; however this
    change legitimizes the use of later features, in particular to replace
    features marked 'obsolescent' in Fortran 90 and 'deleted' in Fortran 2018
    which gfortran 8.x and later warn about.
  - Packages containing files in the 'src' directory with extensions '.f90' or
    '.f95' are now linked using the C or C++ compiler rather than the Fortran
    9x compiler. This is consistent with fixed-form Fortran code and allows
    mixing of C++ and free-form Fortran on most platforms.
  - Consequentially, a package which includes free-form Fortran 9x code which
    uses OpenMP should include SHLIB_OPENMP_CFLAGS (or the CXXFLAGS version if
    they also include C++ code) in PKG_LIBS rather than SHLIB_OPENMP_FCFLAGS —
    fortunately on almost all current platforms they are the same flag.
  - Macro PKG_FFLAGS will be used for the compilation of both fixed-form and
    free-form Fortran code unless PKG_FCFLAGS is also set (in 'src/Makevars' or
    'src/Makevars.win').
  - The make macro F_VISIBILITY is now preferred for both fixed-form and
    free-form Fortran, for use in 'src/Makevars' and similar.
  - R CMD INSTALL gains a new option --strip which (where supported) strips
    installed shared object(s): this can also be achieved by setting the
    environment variable _R_SHLIB_STRIP_ to a true value.
  - The new option --strip-lib attempts stripping of static and shared
    libraries installed under 'lib'.
  - These are most useful on platforms using GNU binutils (such as Linux) and
    compiling with -g flags.
  - There is more support for installing UTF-8-encoded packages in a strict
    Latin-1 locale (and probably for other Latin locales): non-ASCII comments
    in R code (and 'NAMESPACE' files) are worked around better.
- UTILITIES
  - R CMD config knows the values of AR and RANLIB, often set for LTO builds.
  - R CMD check now optionally checks makefiles for correct and portable use of
    the SHLIB_OPENMP_*FLAGS macros.
  - R CMD check now evaluates \Sexpr{} expressions (including those in macros)
    before checking the contents of 'Rd' files and so detects issues both in
    evaluating the expressions and in the expanded contents.
  - R CMD check now lists missing packages separated by commas and with regular
    quotes such as to be useful as argument in calling install.packages(c(..));
    from a suggestion by Marcel Ramos.
  - tools::Rd2latex() now uses UTF-8 as its default output encoding.
  - R CMD check now checks line endings of files with extension '.hpp' and
    those under 'inst/include'. The check now includes that a non-empty file is
    terminated with a newline.
  - R CMD build will correct line endings in such files.
  - R CMD check now tries re-building all vignettes rather than stopping at the
    first error: whilst doing so it adds 'bookmarks' to the log. By default
    (see the 'R Internals' manual) it re-builds each vignette in a separate
    process.
  - It now checks for duplicated vignette titles (also known as 'index
    entries'): they are used as hyperlinks on CRAN package pages and so do need
    to be unique.
  - R CMD check has more comprehensive checks on the 'data' directory and the
    functioning of data() in a package.
  - R CMD check now checks autoconf-generated 'configure' files have their
    corresponding source files, including optionally attempting to regenerate
    them on platforms with autoreconf.
  - R CMD build has a new option --compression to select the compression used
    for the tarball.
  - R CMD build now removes 'src/*.mod' files on all platforms.
- C-LEVEL FACILITIES
  - New pointer protection C functions R_PreserveInMSet and R_ReleaseFromMSet
    have been introduced to replace UNPROTECT_PTR, which is not safe to mix
    with UNPROTECT (and with PROTECT_WITH_INDEX). Intended for use in parsers
    only.
  - NAMEDMAX has been raised to 7 to allow further protection of intermediate
    results from (usually ill-advised) assignments in arguments to BUILTIN
    functions. Properly written package code should not be affected.
  - R_unif_index is now considered to be part of the C API.
  - R_GetCurrentEnv() allows C code to retrieve the current environment.
- DEPRECATED AND DEFUNCT
  - The use of a character vector with .Fortran() is formally deprecated and
    gives a non-portability warning. (It has long been strongly discouraged in
    'Writing R Extensions'.)
  - Argument compressed of untar() is deprecated — it is only used for external
    tar commands which increasingly for extraction auto-detect compression and
    ignore their zjJ flags.
  - var(f) and hence sd(f) now give an error for factor arguments; they gave a
    deprecation warning since R 3.2.3, PR#16564.
  - Package tools' vignetteDepends() has been deprecated (it called a function
    deprecated since Feb 2016), being partly replaced by newly exported
    vignetteInfo().
  - The f77_f2c script has been removed: it no longer sufficed to compile the
    '.f' files in R.
  - The deprecated legacy support of make macros such as CXX1X has been
    removed: use the CXX11 forms instead.
  - Make macro F77_VISIBILITY is deprecated in favour of F_VISIBILITY.
  - Make macros F77, FCPIFCPLAGS and SHLIB_OPENMP_FCFLAGS are deprecated in
    favour of FC, FPICFLAGS and SHLIB_OPENMP_FFLAGS respectively.
  - $.data.frame had become an expensive version of the default method, so has
    been removed. (Thanks to Radford Neal for picking this up and to Duncan
    Murdoch for providing a patch.)
- BUG FIXES
  - On Windows, GUI package installation via menuInstallPkgs() works again,
    thanks to Len Weil's and Duncan Murdoch's PR#17556.
  - R CMD check on data() fixing PR#17558 thanks to Duncan Murdoch.
  - quasi(*, variance = list(..)) now works more efficiently, and should work
    in all cases fixing PR#17560. Further, quasi(var = mu(1-mu)) and quasi(var
    = "mu ^ 3") now work, and quasi(variance = "log(mu)") now gives a correct
    error message.
  - Creation of lazy loading database during package installation is again
    robust to Rprofile changing the current working directory (PR#17559).
  - boxplot(y ~ f, horizontal=TRUE) now produces correct x- and y-labels.
  - rbind.data.frame() allows to keep <NA> levels from factor columns
    (PR#17562) via new option factor.exclude.
  - Additionally, it works in one more case with matrix-columns which had been
    reported on 2017-01-16 by Krzysztof Banas.
  - Correct messaging in C++ pragma checks in tools code for R CMD check,
    fixing PR#17566 thanks to Xavier Robin.
  - print()ing and auto-printing no longer differs for functions with a user
    defined print.function, thanks to Bill Dunlap's report.
  - [On Windows only], writeClipboard(.., format = <n>) now does correctly pass
    format to the underlying C code, thanks to a bug report (with patch) by
    Jenny Bryan.
  - as.data.frame() treats 1D arrays the same as vectors, PR#17570.
  - runmed(x, *) when x contains missing values now works for
    algorithm="Stuetzle", also based on smoothEnds(y) working with NA's, and no
    longer segfaults for the "Turlach" algorithm; reported by Hilmar Berger.
  - vcov(glm(<quasi>), dispersion = *) works correctly again, fixing PR#17571
    thanks to Pavel Krivitsky.
  - replayPlot(r) now also works in the same R session when r has been
    “reproduced” from serialization, typically after saving to and reading from
    an RDS file.
  - substr() and substring() now signal an error when the input is invalid
    UTF-8.
  - file.copy() now works also when its argument to is of length greater than
    one.
  - mantelhaen.test() no longer suffers from integer overflow in largish cases,
    thanks to Ben Bolker's PR#17383.
  - Calling setGeneric("foo") in a package no longer fails when the enclosing
    environment of the implicit generic foo() is .GlobalEnv.
  - untar(file("<some>.tar.gz"), *) now gives a better error message,
    suggesting to use gzfile() instead.
  - Method dispatch uses more relevant environments when looking up class
    definitions.
  - The documentation for identify() incorrectly claimed that the indices of
    identified points were returned in the order that the points were selected.
    identify() now has a new argument order to allow the return value to include
    the order in which points were identified; the documentation has been
    updated.  Reported by Richard Rowe and Samuel Granjeaud.
  - order(...., decreasing=c(TRUE, FALSE)) could fail in some cases. Reported
    from StackOverflow via Karl Nordström.
  - User macros in Rd files now accept empty and multi-line arguments.
  - Changes in print.*(), thanks to Lionel Henry's patches in PR#17398:
  - Printing lists, pairlists or attributes containing calls with S3 class no
    longer evaluate those.
  - Printing S4 objects within lists and pairlists dispatches with show()
    rather than print(), as with auto-printing.
  - The indexing tags (names or [[<n>]]) of recursive data structures are now
    printed correctly in complex cases.
  - Arguments supplied to print() are now properly forwarded to methods when
    printing lists, pairlists or attributes containing S3 objects.
  - The print parameters are now preserved when printing S3 objects or
    deparsing symbols and calls. Previously, printing lists containing S3
    objects or expressions would reset these parameters.
  - Printing lists, pairlists or attributes containing functions now uses
    srcref attributes if present.
  - Calling install.packages() with a length zero pkgs argument now is a no-op
    (PR#17422).
  - unlist(x) now returns a correct factor when x is a nested list with factor
    leaves, fixing PR#12572 and PR#17419.
  - The documentation help(family) gives more details about the aic component,
    thanks to Ben Bolker's prompting.
  - The documentation for attributes and `attributes<-` now gives x as name of
    the first and main argument which the implementation has been requiring,
    fixing PR#17434. For consistency, the first argument name is also changed
    from obj to x for `mostattributes<-`.
  - strwidth() now uses par("font") as default font face (PR#17352).
  - plot(<table>, log="x") no longer warns about log.
  - The print() method for "htest" objects now formats the test statistic and
    parameter directly and hence no longer rounds to units before the decimal
    point. Consequently, printing of t.test() results with a small number of
    digits now shows non-large df's to the full precision (PR#17444).
  - kruskal.test() and fligner.test() no longer erroneously insist on numeric g
    group arguments (PR#16719).
  - Printing a news db via the browser now does a much better job (PR#17433).
  - print.aov() missed column names in the multivariate case due to misspelling
    (reported by Chris Andrews).
  - axis() now creates valid at locations also for small subnormal number
    ranges in log scale plots.
  - format.POSIXlt() now also recycles the zone and gmtoff list components to
    full length when needed, and its internal C code detects have_zone in more
    cases. In some cases, this changes its output to become compatible with
    format.POSIXct().
  - On Windows, detectCores() in package parallel now detects processors in all
    processor groups, not just the group R is running in (impacts particularly
    systems with more than 64 logical processors). Reported by Arunkumar
    Srinivasan.
  - On Windows, socketSelect() would hang with more than 64 sockets, and hence
    parallel::clusterApplyLB() would hang with more than 64 workers. Reported
    by Arunkumar Srinivasan.
  - as(1L, "double") now does coerce (PR#17457).
  - lm.influence(), influence.measures(), rstudent() etc now work (more)
    correctly for multivariate models ("mlm"), thanks to (anonymous)
    stackoverflow remarks.
  - sample.int(2.9, *, replace=TRUE) again behaves as documented and as in R <
    3.0.0, namely identically to sample.int(2, ..).
  - Fixes to convertColor() for chromatic adaptation; thanks to Brodie Gaslam
    PR#17473.
  - Using \Sexpr[stage=install]{..} to create an 'Rd' section no longer gives a
    warning in R CMD check; problem originally posted by Gábor Csárdi, then
    reported as PR#17479 with a partial patch by Duncan Murdoch.
  - Parse data now include a special node for equal assignment.
  - split.default() no longer relies on [[<-(), so it behaves as expected when
    splitting an object by a factor with the empty string as one of its levels.
    Thanks to Brad Friedman for the report.
  - Line numbers in messages about '.Rd' files are now more reliable, thanks to
    a patch from Duncan Murdoch.
  - In the numeric method for all.equal(), a numeric scale argument is now
    checked to be positive and allowed to be of length > 1. (The latter worked
    originally and with a warning in recent years).
  - Deferred string conversions now record the OutDec option setting when not
    equal to the default. Reported by Michael Sannella.
  - When y is numeric and f a factor, plot(y ~ f) nicely uses "y" and "f" as y-
    and x-labels. The more direct boxplot(y ~ f) now does too. The new argument
    ann = FALSE may be used to suppress these.
  - Subassignment to no/empty rows of a data frame is more consistent and
    typically a no-op in all cases instead of sometimes an error; part of Emil
    Bode's PR#17483.
  - Calls like formatC(*, zero.print = "< 0.001") no longer give an error and
    are further improved via new optional argument replace.zero. Reported by
    David Hugh-Jones.
  - methods::formalArgs("<fn>") now finds the same function as formals("<fn>"),
    fixing Emil Bode's PR#17499.
  - The methods package better handles duplicated class names across packages.
  - The default method of seq() now avoids integer overflow, thanks to the
    report and "cumsum" patch of Suharto Anggono's PR#17497.
  - sub() no longer loses encodings for non-ASCII replacements (PR#17509).
  - Fix for rotated raster image on X11 device. (Partial fix for PR#17148;
    thanks to Mikko Korpela).
  - formula(model.frame(frml, ..)) now returns frml in all cases, thanks to
    Bill Dunlap. The previous behavior is available as
    DF2formula(<model.frame>).
  - ar.ols() also returns scalar var.pred in univariate case (PR#17517).
  - normalizePath() now treats NA path as non-existent and normalizes it to NA.
    file.access() treats NA file name as non-existent. file.edit() and
    connection functions such as file() now treat NA file names as errors.
  - The internal regularize.values() auxiliary of approx(), splinefun() etc now
    warns again when there are ties and the caller did not specify ties.
    Further, it no longer duplicates x and y unnecessarily when x is already
    sorted (PR#17515).
  - strtoi("", base) now gives NA on all platforms, following its
    documentation. Reported by Michael Chirico.
  - In the definition of an S4 class, prototype elements are checked against
    the slots of the class, with giving a prototype for an undefined slot now
    being an error. (Reported by Bill Dunlap.)
  - From setClassUnion(), if environment variable
    _R_METHODS_SHOW_CHECKSUBCLASSES is set to true, the internal
    .checkSubclasses() utility prints debugging info to see where it is used.
  - max.col(m) with an m of zero columns now returns integer NA (instead of 1).
  - axTicks() no longer returns small “almost zero” numbers (in exponential
    format) instead of zero, fixing Ilario Gelmetti's PR#17534.
  - isSymmetric(matrix(0, dimnames=list("A","b"))) is FALSE again, as always
    documented.
  - The cairo_pdf graphics device (and other Cairo-based devices) now clip
    correctly to the right and bottom border.
  - There was an off-by-one-pixel bug, reported by Lee Kelvin.
  - as.roman(3) <= 2:4 and all other comparisons now work, as do group
    "Summary" function calls such as max(as.roman(sample(20))) and
    as.roman(NA). (Partly reported by Bill Dunlap in PR#17542.)
  - reformulate("x", response = "sin(y)") no longer produces extra back quotes,
    PR#17359, and gains new optional argument env.
  - When reading console input from 'stdin' with re-encoding (R --encoding=enc
    < input) the code on a Unix-alike now ensures that each converted input
    line is terminated with a newline even if re-encoding fails.
  - as.matrix.data.frame() now produces better strings from logicals, thanks to
    PR#17548 from Gabe Becker.
  - The S4 generic signature of rowSums(), rowMeans(), colSums() and colMeans()
    is restricted to "x".
  - match(x, tab) now works for long character vectors x, thanks to PR#17552 by
    Andreas Kersting.
  - Class unions are unloaded when their namespace is unloaded (PR#17531,
    adapted from a patch by Brodie Gaslam).
  - selectMethod() is robust to ANY-truncation of method signatures (thanks to
    Herve Pages for the report).

* Fri Mar 22 2019 Shane Sturrock <shane.sturrock@gmail.com> - 3.5.3-1
- INSTALLATION on a UNIX-ALIKE
  - Detection of flags for C++98/11/14/17 has been improved: in particular if
    CXX??STD is set, it is tried first with no additional flags.
- PACKAGE INSTALLATION
  - New macro F_VISIBILITY as an alternative to F77_VISIBILITY. This will
    become the preferred form in R 3.6.0.
- BUG FIXES
  - writeLines(readLines(fnam), fnam) now works as expected, thanks to Peter
    Meissner's PR#17528.
  - setClassUnion() no longer warns, but uses message() for now, when
    encountering “non local” subclasses of class members.
  - stopifnot(exprs = T) no longer fails.

* Fri Feb 01 2019 Shane Sturrock <shane.sturrock@gmail.com> - 3.5.2-1
- PACKAGE INSTALLATION
  - New macro CXX_VISIBILITY analogous to C_VISIBILITY (which several packages
    have been misusing for C++ code) for the default C++ compiler (but not
    necessarily one used for non-default C++ dialects like C++14).
- TESTING
  - The random number generator tests in 'tests/p-r-random-tests.R' no longer
    fail occasionally as they now randomly sample from “certified” random
    seeds.
- BUG FIXES
  - The "glm" method of drop1() miscalculated the score test (test="Rao") when
    the model contained an offset.
  - Linear multiple empty models such as lm(y ~ 0) now have a correctly
    dimensioned empty coefficient matrix; reported by Brett Presnell.
  - vcov(<empty mlm>) and hence confint() now work (via a consistency change in
    summary.lm()).
  - confint(<multiple lm()>) now works correctly; reported on R-devel by Steven
    Pav.
  - quade.test() now also works correctly when its arguments are not yet sorted
    along groups, fixing PR#15842.
  - Installation on a Unix-alike tries harder to link to the pthread library
    where required (rather than relying on OpenMP to provide it: configuring
    with --disable-openmp was failing on some Linux systems).
  - The data.frame method for print(x) is fast now also for large data frames x
    and got an optional argument max, thanks to suggestions by Juan Telleria.
  - hist() no longer integer overflows in very rare cases, fixing PR#17450.
  - untar() ignored a character compressed argument: however many external tar
    programs ignore the flags which should have been set and automagically
    choose the compression type, and if appropriate gzip or bzip2 compression
    would have been chosen from the magic header of the tarball.
  - zapsmall(x) now works for more “number-like” objects.
  - The tools-internal function called from R CMD INSTALL now gets a warnOption
    = 1 argument and only sets options(warn = warnOption) when that increases
    the warning level (PR#17453).
  - Analogously, the tools-internal function called from R CMD check gets a
    warnOption = 1 argument and uses the larger of that and getOption("warn"),
    also allowing to be run with increased warning level.
  - Parse data now have deterministic parent nodes (PR#16041).
  - Calling match() with length one x and POSIXlt table gave a segfault
    (PR#17459).
  - Fork clusters could hang due to a race condition in cluster initialization
    (makeCluster()).
  - nextn(n) now also works for larger n and no longer loops infinitely for
    e.g, n <- 214e7.
  - cooks.distance() and rstandard() now work correctly for multiple linear
    models ("mlm").
  - polym() and corresponding lm() prediction now also work for a boundary
    "vector" case fixing PR#17474, reported by Alexandre Courtiol.
  - With a very large number of variables terms() could segfault (PR#17480).
  - cut(rep(0, 7)) now works, thanks to Joey Reid and Benjamin Tyner
    (PR#16802).
  - download.file(*, method = "curl", cacheOK = FALSE) should work now on
    Windows, thanks to Kevin Ushey's patch in PR#17323.
  - duplicated(<dataframe with 'f'>) now works, too, thanks to Andreas
    Kersting's PR#17485; ditto for anyDuplicated().
  - legend(*, cex = 1:2) now works less badly.
  - The print() method for POSIXct and POSIXlt now correctly obeys
    getOption("max.print"), fixing a long-standing typo, and it also gets a
    corresponding optional max argument.
  - Unserialization of raw vectors serialized in ASCII representation now works
    correctly.
  - <data frame>[TRUE, <new>] <- list(c1, c2) now works correctly, thanks to
    Suharto Anggono's PR#15362 and Emil Bode's patch in PR#17504.
  - seq.int(*, by=by, length=n) no longer wrongly “drops fractional parts” when
    by is integer, thanks to Suharto Anggono's report PR#17506.
  - Buffering is disabled for file() connections to non-regular files (like
    sockets), as well as fifo() and pipe() connections. Fixes PR#17470,
    reported by Chris Culnane.

* Tue Sep 11 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.5.1-2
- Fixed issue with linked libraries

* Fri Jul 06 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.5.1-1
- BUG FIXES
  - file("stdin") is no longer considered seekable.
  - dput() and dump() are no longer truncating when options(deparse.max.lines =
    *) is set.
  - Calls with an S3 class are no longer evaluated when printed, fixing part of
    PR#17398, thanks to a patch from Lionel Henry.
  - Allow file argument of Rscript to include space even when it is first on
    the command line.
  - callNextMethod() uses the generic from the environment of the calling
    method. Reported by Hervé Pagès with well documented examples.
  - Compressed file connections are marked as blocking.
  - optim(*, lower = c(-Inf, -Inf)) no longer warns (and switches the method),
    thanks to a suggestion by John Nash.
  - predict(fm, newdata) is now correct also for models where the formula has
    terms such as splines::ns(..) or stats::poly(..), fixing PR#17414, based on
    a patch from Duncan Murdoch.
  - simulate.lm(glm(*, gaussian(link = <non-default>))) has been corrected,
    fixing PR#17415 thanks to Alex Courtiol.
  - unlist(x) no longer fails in some cases of nested empty lists. Reported by
    Steven Nydick.
  - qr.coef(qr(<all 0, w/ colnames>)) now works. Reported by Kun Ren.
  - The radix sort is robust to vectors with >1 billion elements (but long
    vectors are still unsupported). Thanks to Matt Dowle for the fix.
  - Terminal connections (e.g., stdin) are no longer buffered. Fixes PR#17432.
  - deparse(x), dput(x) and dump() now respect c()'s argument names recursive
    and use.names, e.g., for x <- setNames(0, "recursive"), thanks to Suharto
    Anggono's PR#17427.
  - Unbuffered connections now work with encoding conversion. Reported by
    Stephen Berman.
  - '.Renviron' on Windows with Rgui is again by default searched for in user
    documents directory when invoked via the launcher icon. Reported by Jeroen
    Ooms.
  - printCoefmat() now also works with explicit right=TRUE.
  - print.noquote() now also works with explicit quote=FALSE.
  - The default method for pairs(.., horInd=*, verInd=*) now gets the correct
    order, thanks to reports by Chris Andrews and Gerrit Eichner. Additionally,
    when horInd or verInd contain only a subset of variables, all the axes are
    labeled correctly now.
  - agrep("..|..", .., fixed=FALSE) now matches when it should, thanks to a
    reminder by Andreas Kolter.
  - str(ch) now works for more invalid multibyte strings.

* Fri Apr 27 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.5.0-1
- SIGNIFICANT USER-VISIBLE CHANGES
  - All packages are by default byte-compiled on installation. This makes the
    installed packages larger (usually marginally so) and may affect the format
    of messages and tracebacks (which often exclude .Call and similar).
- NEW FEATURES
  - factor() now uses order() to sort its levels, rather than sort.list(). This
    allows factor() to support custom vector-like objects if methods for the
    appropriate generics are defined. It has the side effect of making factor()
    succeed on empty or length-one non-atomic vector(-like) types (e.g.,
    "list"), where it failed before.
  - diag() gets an optional names argument: this may require updates to
    packages defining S4 methods for it.
  - chooseCRANmirror() and chooseBioCmirror() no longer have a useHTTPS
    argument, not needed now all R builds support https:// downloads.
  - New summary() method for warnings() with a (somewhat experimental) print()
    method.
  - (methods package.) .self is now automatically registered as a global
    variable when registering a reference class method.
  - tempdir(check = TRUE) recreates the tempdir() directory if it is no longer
    valid (e.g. because some other process has cleaned up the '/tmp'
    directory).
  - New askYesNo() function and "askYesNo" option to ask the user binary
    response questions in a customizable but consistent way. (Suggestion of
    PR#17242.)
  - New low level utilities ...elt(n) and ...length() for working with ...
    parts inside a function.
  - isTRUE() is more tolerant and now true in
       x <- rlnorm(99) 
       isTRUE(median(x) == quantile(x)["50%"]) 
    New function isFALSE() defined analogously to isTRUE().
  - The default symbol table size has been increased from 4119 to 49157; this
    may improve the performance of symbol resolution when many packages are
    loaded. (Suggested by Jim Hester.)
  - line() gets a new option iter = 1.
  - Reading from connections in text mode is buffered, significantly improving
    the performance of readLines(), as well as scan() and read.table(), at
    least when specifying colClasses.
  - order() is smarter about picking a default sort method when its arguments
    are objects.
  - available.packages() has two new arguments which control if the values from
    the per-session repository cache are used (default true, as before) and if
    so how old cached values can be to be used (default one hour).  These
    arguments can be passed from install.packages(), update.packages() and
    functions calling that: to enable this available.packages(), packageStatus()
    and download.file() gain a ... argument.
  - packageStatus()'s upgrade() method no longer ignores its ... argument but
    passes it to install.packages().
  - installed.packages() gains a ... argument to allow arguments (including
    noCache) to be passed from new.packages(), old.packages(),
    update.packages() and packageStatus().
  - factor(x, levels, labels) now allows duplicated labels (not duplicated
    levels!). Hence you can map different values of x to the same level
    directly.
  - Attempting to use names<-() on an S4 derivative of a basic type no longer
    emits a warning.
  - The list method of within() gains an option keepAttrs = FALSE for some
    speed-up.
  - system() and system2() now allow the specification of a maximum elapsed
    time ('timeout').
  - debug() supports debugging of methods on any object of S4 class
    "genericFunction", including group generics.
  - Attempting to increase the length of a variable containing NULL using
    length()<- still has no effect on the target variable, but now triggers a
    warning.
  - type.convert() becomes a generic function, with additional methods that
    operate recursively over list and data.frame objects. Courtesy of Arni
    Magnusson (PR#17269).
  - lower.tri(x) and upper.tri(x) only needing dim(x) now work via new
    functions .row() and .col(), so no longer call as.matrix() by default in
    order to work efficiently for all kind of matrix-like objects.
  - print() methods for "xgettext" and "xngettext" now use encodeString() which
    keeps, e.g. "\n", visible. (Wish of PR#17298.)
  - package.skeleton() gains an optional encoding argument.
  - approx(), spline(), splinefun() and approxfun() also work for long vectors.
  - deparse() and dump() are more useful for S4 objects, dput() now using the
    same internal C code instead of its previous imperfect workaround R code.
    S4 objects now typically deparse perfectly, i.e., can be recreated
    identically from deparsed code.  dput(), deparse() and dump() now print the
    names() information only once, using the more readable (tag = value)
    syntax, notably for list()s, i.e., including data frames.  These functions
    gain a new control option "niceNames" (see .deparseOpts()), which when set
    (as by default) also uses the (tag = value) syntax for atomic vectors. On
    the other hand, without deparse options "showAttributes" and "niceNames",
    names are no longer shown also for lists. as.character(list( c (one = 1)))
    now includes the name, as as.character(list(list(one = 1))) has always done.
    m:n now also deparses nicely when m > n.
    The "quoteExpressions" option, also part of "all", no longer quote()s
    formulas as that may not re-parse identically. (PR#17378)
  - If the option setWidthOnResize is set and TRUE, R run in a terminal using a
    recent readline library will set the width option when the terminal is
    resized. Suggested by Ralf Goertz.
  - If multiple on.exit() expressions are set using add = TRUE then all
    expressions will now be run even if one signals an error.
  - mclapply() gets an option affinity.list which allows more efficient
    execution with heterogeneous processors, thanks to Helena Kotthaus.
  - The character methods for as.Date() and as.POSIXlt() are more flexible via
    new arguments tryFormats and optional: see their help pages.
  - on.exit() gains an optional argument after with default TRUE. Using after =
    FALSE with add = TRUE adds an exit expression before any existing ones.
    This way the expressions are run in a first-in last-out fashion. (From
    Lionel Henry.)
  - On Windows, file.rename() internally retries the operation in case of error
    to attempt to recover from possible anti-virus interference.
  - Command line completion on :: now also includes lazy-loaded data.
  - If the TZ environment variable is set when date-time functions are first
    used, it is recorded as the session default and so will be used rather than
    the default deduced from the OS if TZ is subsequently unset.
  - There is now a [ method for class "DLLInfoList".
  - glm() and glm.fit get the same singular.ok = TRUE argument that lm() has
    had forever. As a consequence, in glm(*, method = <your_own>), user
    specified methods need to accept a singular.ok argument as well.
  - aspell() gains a filter for Markdown ('.md' and '.Rmd') files.
  - intToUtf8(multiple = FALSE) gains an argument to allow surrogate pairs to
    be interpreted.
  - The maximum number of DLLs that can be loaded into R e.g. via dyn.load()
    has been increased up to 614 when the OS limit on the number of open files
    allows.
  - Sys.timezone() on a Unix-alike caches the value at first use in a session:
    inter alia this means that setting TZ later in the session affects only the
    current time zone and not the system one.
  - Sys.timezone() is now used to find the system timezone to pass to the code
    used when R is configured with --with-internal-tzcode.
  - When tar() is used with an external command which is detected to be GNU tar
    or libarchive tar (aka bsdtar), a different command-line is generated to
    circumvent line-length limits in the shell.
  - system(*, intern = FALSE), system2() (when not capturing output),
    file.edit() and file.show() now issue a warning when the external command
    cannot be executed.
  - The “default” ("lm" etc) methods of vcov() have gained new optional
    argument complete = TRUE which makes the vcov() methods more consistent
    with the coef() methods in the case of singular designs. The former
    (back-compatible) behavior is given by vcov(*, complete = FALSE).
  - coef() methods (for lm etc) also gain a complete = TRUE optional argument
    for consistency with vcov(). 
  - For "aov", both coef() and vcov() methods remain back-compatibly
    consistent, using the other default, complete = FALSE.
  - attach(*, pos = 1) is now an error instead of a warning.
  - New function getDefaultCluster() in package parallel to get the default
    cluster set via setDefaultCluster().
  - str(x) for atomic objects x now treats both cases of is.vector(x)
    similarly, and hence much less often prints "atomic". This is a slight
    non-back-compatible change producing typically both more informative and
    shorter output.
  - write.dcf() gets optional argument useBytes.
  - New, partly experimental packageDate() which tries to get a valid "Date"
    object from a package 'DESCRIPTION' file, thanks to suggestions in
    PR#17324.
  - tools::resaveRdaFiles() gains a version argument, for use when packages
    should remain compatible with earlier versions of R.
  - ar.yw(x) and hence by default ar(x) now work when x has NAs, mostly thanks
    to a patch by Pavel Krivitsky in PR#17366. The ar.yw.default()'s AIC
    computations have become more efficient by using determinant().
  - New warnErrList() utility (from package nlme, improved).
  - By default the (arbitrary) signs of the loadings from princomp() are chosen
    so the first element is non-negative.
  - If --default-packages is not used, then Rscript now checks the environment
    variable R_SCRIPT_DEFAULT_PACKAGES. If this is set, then it takes
    precedence over R_DEFAULT_PACKAGES. If default packages are not specified on
    the command line or by one of these environment variables, then Rscript now
    uses the same default packages as R. For now, the previous behavior of not
    including methods can be restored by setting the environment variable
    R_SCRIPT_LEGACY to yes.
  - When a package is found more than once, the warning from find.package(*,
    verbose=TRUE) lists all library locations.
  - POSIX objects can now also be rounded or truncated to month or year.
  - stopifnot() can be used alternatively via new argument exprs which is nicer
    and useful when testing several expressions in one call.
  - The environment variable R_MAX_VSIZE can now be used to specify the maximal
    vector heap size. On macOS, unless specified by this environment variable,
    the maximal vector heap size is set to the maximum of 16GB and the available
    physical memory. This is to avoid having the R process killed when macOS
    over-commits memory.
  - sum(x) and sum(x1,x2,..,x<N>) with many or long logical or integer vectors
    no longer overflows (and returns NA with a warning), but returns double
    numbers in such cases.
  - Single components of "POSIXlt" objects can now be extracted and replaced
    via [ indexing with 2 indices.
  - S3 method lookup now searches the namespace registry after the top level
    environment of the calling environment.
  - Arithmetic sequences created by 1:n, seq_along, and the like now use
    compact internal representations via the ALTREP framework. Coercing integer
    and numeric vectors to character also now uses the ALTREP framework to defer
    the actual conversion until first use.
  - Finalizers are now run with interrupts suspended.
  - merge() gains new option no.dups and by default suffixes the second of two
    duplicated column names, thanks to a proposal by Scott Ritchie (and Gabe
    Becker).
  - scale.default(x, center, scale) now also allows center or scale to be
    “numeric-alike”, i.e., such that as.numeric(.) coerces them correctly. This
    also eliminates a wrong error message in such cases.
  - par*apply and par*applyLB gain an optional argument chunk.size which allows
    to specify the granularity of scheduling.
  - Some as.data.frame() methods, notably the matrix one, are now more careful
    in not accepting duplicated or NA row names, and by default produce unique
    non-NA row names. This is based on new function .rowNamesDF(x, make.names =
    *) <- rNms where the logical argument make.names allows to specify how
    invalid row names rNms are handled. .rowNamesDF() is a “workaround”
    compatible default.
  - R has new serialization format (version 3) which supports custom
    serialization of ALTREP framework objects. These objects can still be
    serialized in format 2, but less efficiently. Serialization format 3 also
    records the current native encoding of unflagged strings and converts them
    when de-serialized in R running under different native encoding. Format 3
    comes with new serialization magic numbers (RDA3, RDB3, RDX3). Format 3 can
    be selected by version = 3 in save(), serialize() and saveRDS(), but format
    2 remains the default for all serialization and saving of the workspace.
    Serialized data in format 3 cannot be read by versions of R prior to version
    3.5.0.
  - The "Date" and “date-time” classes "POSIXlt" and "POSIXct" now have a
    working `length<-` method, as wished in PR#17387.
  - optim(*, control = list(warn.1d.NelderMead = FALSE)) allows to turn off the
    warning when applying the default "Nelder-Mead" method to 1-dimensional
    problems.
  - matplot(.., panel.first = .) etc now work, as log becomes explicit argument
    and ... is passed to plot() unevaluated, as suggested by Sebastian Meyer in
    PR#17386.
  - Interrupts can be suspended while evaluating an expression using
    suspendInterrupts. Subexpression can be evaluated with interrupts enabled
    using allowInterrupts. These functions can be used to make sure cleanup
    handlers cannot be interrupted.
  - R 3.5.0 includes a framework that allows packages to provide alternate
    representations of basic R objects (ALTREP). The framework is still
    experimental and may undergo changes in future R releases as more
    experience is gained. For now, documentation is provided in
    https://svn.r-project.org/R/branches/ALTREP/ALTREP.html.
- UTILITIES
  - install.packages() for source packages now has the possibility to set a
    'timeout' (elapsed-time limit). For serial installs this uses the timeout
    argument of system2(): for parallel installs it requires the timeout utility
    command from GNU coreutils.
  - It is now possible to set 'timeouts' (elapsed-time limits) for most parts
    of R CMD check via environment variables documented in the 'R Internals'
    manual.
  - The 'BioC extra' repository which was dropped from Bioconductor 3.6 and
    later has been removed from setRepositories(). This changes the mapping for
    6–8 used by setRepositories(ind=).
  - R CMD check now also applies the settings of environment variables
    _R_CHECK_SUGGESTS_ONLY_ and _R_CHECK_DEPENDS_ONLY_ to the re-building of
    vignettes.
  - R CMD check with environment variable _R_CHECK_DEPENDS_ONLY_ set to a true
    value makes test-suite-management packages available and (for the time
    being) works around a common omission of rmarkdown from the VignetteBuilder
    field.
- INSTALLATION on a UNIX-ALIKE
  - Support for a system Java on macOS has been removed — install a fairly
    recent Oracle Java (see 'R Installation and Administration' §C.3.2).
  - configure works harder to set additional flags in SAFE_FFLAGS only where
    necessary, and to use flags which have little or no effect on performance.
  - In rare circumstances it may be necessary to override the setting of
    SAFE_FFLAGS.
  - C99 functions expm1, hypot, log1p and nearbyint are now required.
  - configure sets a -std flag for the C++ compiler for all supported C++
    standards (e.g., -std=gnu++11 for the C++11 compiler). Previously this was
    not done in a few cases where the default standard passed the tests made
    (e.g.  clang 6.0.0 for C++11).
- C-LEVEL FACILITIES
  - 'Writing R Extensions' documents macros MAYBE_REFERENCED, MAYBE_SHARED and
    MARK_NOT_MUTABLE that should be used by package C code instead NAMED or
    SET_NAMED.
  - The object header layout has been changed to support merging the ALTREP
    branch. This requires re-installing packages that use compiled code.
  - 'Writing R Extensions' now documents the R_tryCatch, R_tryCatchError, and
    R_UnwindProtect functions.
  - NAMEDMAX has been raised to 3 to allow protection of intermediate results
    from (usually ill-advised) assignments in arguments to BUILTIN functions.
    Package C code using SET_NAMED may need to be revised.
- DEPRECATED AND DEFUNCT
  - Sys.timezone(location = FALSE) is defunct, and is ignored (with a warning).
  - methods:::bind_activation() is defunct now; it typically has been unneeded
    for years.
  - The undocumented 'hidden' objects .__H__.cbind and .__H__.rbind in package
    base are deprecated (in favour of cbind and rbind).
  - The declaration of pythag() in 'Rmath.h' has been removed — the entry point
    has not been provided since R 2.14.0.
- BUG FIXES
  - printCoefmat() now also works without column names.
  - The S4 methods on Ops() for the "structure" class no longer cause infinite
    recursion when the structure is not an S4 object.
  - nlm(f, ..) for the case where f() has a "hessian" attribute now computes
    LL' = H + µI correctly. (PR#17249).
  - An S4 method that “rematches” to its generic and overrides the default
    value of a generic formal argument to NULL no longer drops the argument
    from its formals.
  - Rscript can now accept more than one argument given on the #! line of a
    script. Previously, one could only pass a single argument on the #! line in
    Linux.
  - Connections are now written correctly with encoding "UTF-16LE". (PR#16737).
  - Evaluation of ..0 now signals an error. When ..1 is used and ... is empty,
    the error message is more appropriate.
  - (Windows mainly.) Unicode code points which require surrogate pairs in
    UTF-16 are now handled. All systems should properly handle surrogate pairs,
    even those systems that do not need to make use of them. (PR#16098)
  - stopifnot(e, e2, ...) now evaluates the expressions sequentially and in
    case of an error or warning shows the relevant expression instead of the
    full stopifnot(..) call.
  - path.expand() on Windows now accepts paths specified as UTF-8-encoded
    character strings even if not representable in the current locale.
    (PR#17120)
  - line(x, y) now correctly computes the medians of the left and right group's
    x-values and in all cases reproduces straight lines.
  - Extending S4 classes with slots corresponding to special attributes like
    dim and dimnames now works.
  - Fix for legend() when fill has multiple values the first of which is NA
    (all colours used to default to par(fg)). (PR#17288)
  - installed.packages() did not remove the cached value for a library tree
    that had been emptied (but would not use the old value, just waste time
    checking it).
  - The documentation for installed.packages(noCache = TRUE) incorrectly
    claimed it would refresh the cache.
  - aggregate(<data.frame>) no longer uses spurious names in some cases.
    (PR#17283)
  - object.size() now also works for long vectors.
  - packageDescription() tries harder to solve re-encoding issues, notably seen
    in some Windows locales. This fixes the citation() issue in PR#17291.
  - poly(<matrix>, 3) now works, thanks to prompting by Marc Schwartz.
  - readLines() no longer segfaults on very large files with embedded '\0' (aka
    'nul') characters. (PR#17311)
  - ns() (package splines) now also works for a single observation.
    interpSpline() gives a more friendly error message when the number of
    points is less than four.
  - dist(x, method = "canberra") now uses the correct definition; the result
    may only differ when x contains values of differing signs, e.g. not for 0-1
    data.
  - methods:::cbind() and methods:::rbind() avoid deep recursion, thanks to
    Suharto Anggono via PR#17300.
  - Arithmetic with zero-column data frames now works more consistently; issue
    raised by Bill Dunlap.
  - Arithmetic with data frames gives a data frame for ^ (which previously gave
    a numeric matrix).
  - pretty(x, n) for large n or large diff(range(x)) now works better (though
    it was never meant for large n); internally it uses the same rounding fuzz
    (1e-10) as seq.default() — as it did up to 2010-02-03 when both were 1e-7.
  - Internal C-level R_check_class_and_super() and hence R_check_class_etc()
    now also consider non-direct super classes and hence return a match in more
    cases. This e.g., fixes behaviour of derived classes in package Matrix.
  - Reverted unintended change in behavior of return calls in on.exit
    expressions introduced by stack unwinding changes in R 3.3.0.
  - Attributes on symbols are now detected and prevented; attempt to add an
    attribute to a symbol results in an error.
  - fisher.test(*, workspace = <n>) now may also increase the internal stack
    size which allows larger problem to be solved, fixing PR#1662.
  - The methods package no longer directly copies slots (attributes) into a
    prototype that is of an “abnormal” (reference) type, like a symbol.
  - The methods package no longer attempts to call length<-() on NULL (during
    the bootstrap process).
  - The methods package correctly shows methods when there are multiple methods
    with the same signature for the same generic (still not fully supported,
    but at least the user can see them).
  - sys.on.exit() is now always evaluated in the right frame. (From Lionel
    Henry.)
  - seq.POSIXt(*, by = "<n> DSTdays") now should work correctly in all cases
    and is faster. (PR#17342)
  - .C() when returning a logical vector now always maps values other than
    FALSE and NA to TRUE (as documented).
  - Subassignment with zero length vectors now coerces as documented
    (PR#17344).
  - Further, x <- numeric(); x[1] <- character() now signals an error
    'replacement has length zero' (or a translation of that) instead of doing
    nothing.
  - (Package parallel.) mclapply(), pvec() and mcparallel() (when mccollect()
    is used to collect results) no longer leave zombie processes behind.
  - R CMD INSTALL <pkg> now produces the intended error message when, e.g., the
    LazyData field is invalid.
  - as.matrix(dd) now works when the data frame dd contains a column which is a
    data frame or matrix, including a 0-column matrix/d.f. .
  - mclapply(X, mc.cores) now follows its documentation and calls lapply() in
    case mc.cores = 1 also in the case mc.preschedule is false. (PR#17373)
  - aggregate(<data.frame>, drop=FALSE) no longer calls the function on <empty>
    parts but sets corresponding results to NA. (Thanks to Suharto Anggono's
    patches in PR#17280).
  - The duplicated() method for data frames is now based on the list method
    (instead of string coercion). Consequently unique() is better
    distinguishing data frame rows, fixing PR#17369 and PR#17381. The methods
    for matrices and arrays are changed accordingly.
  - Calling names() on an S4 object derived from "environment" behaves (by
    default) like calling names() on an ordinary environment.
  - read.table() with a non-default separator now supports quotes following a
    non-whitespace character, matching the behavior of scan().
  - parLapplyLB and parSapplyLB have been fixed to do load balancing (dynamic
    scheduling). This also means that results of computations depending on
    random number generators will now really be non-reproducible, as documented.
  - Indexing a list using dollar and empty string (l$"") returns NULL.
  - Using \usage{ data(<name>, package="<pkg>") } no longer produces R CMD
    check warnings.
  - match.arg() more carefully chooses the environment for constructing default
    choices, fixing PR#17401 as proposed by Duncan Murdoch.
  - Deparsing of consecutive ! calls is now consistent with deparsing unary -
    and + calls and creates code that can be reparsed exactly; thanks to a
    patch by Lionel Henry in PR#17397. (As a side effect, this uses fewer
    parentheses in some other deparsing involving ! calls.)

* Fri Mar 16 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.4.4-1
- NEW FEATURES
  - Sys.timezone() tries more heuristics on Unix-alikes and so is more likely
    to succeed (especially on Linux). For the slowest method, a warning is
    given recommending that TZ is set to avoid the search.
  - The version of LAPACK included in the sources has been updated to 3.8.0
    (for the routines used by R, a very minor bug-fix change).
  - parallel::detectCores(logical = FALSE) is ignored on Linux systems, since
    the information is not available with virtualized OSes.
- INSTALLATION on a UNIX-ALIKE
  - configure will use pkg-config to find the flags to link to jpeg if
    available (as it should be for the recently-released jpeg-9c and
    libjpeg-turbo). (This amends the code added in R 3.3.0 as the module name in
    jpeg-9c is not what that tested for.)
- DEPRECATED AND DEFUNCT
  - Sys.timezone(location = FALSE) (which was a stop-gap measure for Windows
    long ago) is deprecated. It no longer returns the value of environment
    variable TZ (usually a location).
  - Legacy support of make macros such as CXX1X is formally deprecated: use the
    CXX11 forms instead.
- BUG FIXES
  - power.prop.test() now warns when it cannot solve the problem, typically
    because of impossible constraints. (PR#17345)
  - removeSource() no longer erroneously removes NULL in certain cases, thanks
    to Dénes Tóth.
  - nls(`NO [mol/l]` ~ f(t)) and nls(y ~ a) now work. (Partly from PR#17367)
  - R CMD build checks for GNU cp rather than assuming Linux has it. (PR#17370
    says 'Alpine Linux' does not.)
  - Non-UTF-8 multibyte character handling fixed more permanently (PR#16732).
  - sum(<large ints>, <stuff>) is more consistent. (PR#17372)
  - rf() and rbeta() now also work correctly when ncp is not scalar, notably
    when (partly) NA. (PR#17375)
  - is.na(NULL) no longer warns. (PR#16107)
  - R CMD INSTALL now correctly sets C++ compiler flags when all source files
    are in sub-directories of 'src'.

* Fri Dec 01 2017 Shane Sturrock <shane.sturrock@gmail.com> - 3.4.3-1
- INSTALLATION on a UNIX-ALIKE:
  - A workaround has been added for the changes in location of time-zone files
    in macOS 10.13 'High Sierra' and again in 10.13.1, so the default time zone
    is deduced correctly from the system setting when R is configured with
    --with-internal-tzcode (the default on macOS).
  - R CMD javareconf has been updated to recognize the use of a Java 9 SDK on
    macOS.
- BUG FIXES:
  - raw(0) & raw(0) and raw(0) | raw(0) again return raw(0) (rather than
    logical(0)).
  - intToUtf8() converts integers corresponding to surrogate code points to NA
    rather than invalid UTF-8, as well as values larger than the current
    Unicode maximum of 0x10FFFF.  (This aligns with the current RFC3629.)
  - Fix calling of methods on S4 generics that dispatch on ... when the call
    contains ....
  - Following Unicode 'Corrigendum 9', the UTF-8 representations of U+FFFE and
    U+FFFF are now regarded as valid by utf8ToInt().  range(c(TRUE, NA), finite
    = TRUE) and similar no longer return NA. (Reported by Lukas Stadler.)
  - The self starting function attr(SSlogis, "initial") now also works when the
    y values have exact minimum zero and is slightly changed in general,
    behaving symmetrically in the y range.
  - The printing of named raw vectors is now formatted nicely as for
    other such atomic vectors, thanks to Lukas Stadler.

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
    on macOS 10.13 'High Sierra', so the default time zone is deduced correctly
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
    file name extensions (e.g., '*.md.rsp' but not '*.Rmd') failed with an
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
  - Vignettes listed in '.Rbuildignore' were not being ignored properly.
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
  - This was seen from R CMD check with 'inst/doc/*.R' files, and check has
    some additional protection for such files.
  - print.noquote(x) now always returns its argument x (invisibly).
  - Non-UTF-8 multibyte character sets were not handled properly in source
    references. (PR#16732)
