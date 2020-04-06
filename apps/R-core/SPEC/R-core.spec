%global pkgbase R
%define priority 363
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:           R-core
Version:        3.6.3
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
      for large sample sizes, thanks to a report and patch by Benjamin Tyner in
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
