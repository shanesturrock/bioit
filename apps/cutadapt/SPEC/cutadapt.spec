%define priority 280
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		cutadapt
Version:	2.8
Release:	1%{?dist}
Summary:	Removes adapter sequences, primers etc
Group:		Applications/Engineering
License:	MIT
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
cutadapt removes adapter sequences from high-throughput sequencing data. This
is usually necessary when the read length of the sequencing machine is longer
than the molecule that is sequenced, for example when sequencing microRNAs.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/cutadapt %{name} /opt/bioit/%{name}/%{version}/cutadapt %{priority}

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove %{name} /opt/bioit/%{name}/%{version}/cutadapt
fi

%files

%changelog
* Fri Jan 17 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.8-1
- With option "--revcomp", Cutadapt now searches both the read and its reverse
  complement for adapters. The version that matches best is kept. This can be
  used to "normalize" strandedness.
- "--action=lowercase" now works with linked adapters
- Info files can now be written even for linked adapters.

* Fri Nov 29 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.7-1
- Multicore is now supported even when using --info-file, --rest-file or
  --wildcard-file. The only remaining feature that still does not work with
  multicore is now demultiplexing.
- When running on a single core, Cutadapt no longer spawns external pigz
  processes for writing gzip-compressed files. This is a first step towards
  ensuring that using --cores=n uses only at most n CPU cores.
- This release adds support for Python 3.8.

* Fri Nov 01 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.6-1
- Do not show animated progress when ``--quiet`` is used.
- When two adapters align to a read equally well (in terms of the number of
  matches), prefer the alignment that has fewer errors.
- Give priority to adapters given earlier on the command line. Previously, the
  priority was: All 3' adapters, all 5' adapters, all anywhere adapters. In
  rare cases this could lead to different results.
- Fix an issue preventing Cutadapt from being used on Windows.
- This release no longer supports Python 3.4 (which has reached end of life).

* Fri Sep 13 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.5-1
- Multicore is now supported even when using --untrimmed-output,
  --too-short-output, --too-long-output or the corresponding ...-paired-output
  options.
- Using --info-file no longer crashes when processing paired-end data.
  However, the info file itself will only contain results for R1.
- Options -e/--no-indels/-O were ignored for linked adapters
- When a "Too many open files" error occurs during demultiplexing,
  Cutadapt can now automatically raise the limit and re-try if the limit is a
  "soft" limit.

* Fri Jul 19 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.4-1
- Implement support for demultiplexing paired-end reads that use combinatorial
  indexing (“combinatorial demultiplexing”).
- Speed up reading compressed files by requiring an xopen version that uses an
  external pigz process even for reading compressed input files (not only for
  writing).
- Fix --report=minimal not working.
- Add a --fasta option for forcing that FASTA is written to standard output
  even when input is FASTQ. Previously, forcing FASTA was only possible by
  providing an output file name.

* Fri May 03 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.3-1
- V2.3
  - :issue:`378`: The ``--pair-adapters`` option, added in version 2.1, was not
    actually usable for demultiplexing.
- V2.2
  - :issue:`376`: Fix a crash when using anchored 5' adapters together with
    ``--no-indels`` and trying to trim an empty read.
  - :issue:`369`: Fix a crash when attempting to trim an empty read using a
    ``-g`` adapter with wildcards.

* Fri Mar 22 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.1-1
- Fix problems when combining ``--cores`` with reading from standard input or
  writing to standard output.
- Support :ref:`“paired adapters” <paired-adapters>`. One use case is
  demultiplexing Illumina *Unique Dual Indices* (UDI).

* Fri Mar 08 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.0-1
- This is a major new release with lots of bug fixes and new features, but also
  some backwards-incompatible changes. These should hopefully not affect too
  many users, but please make sure to review them and possibly update your
  scripts!
- Backwards-incompatible changes
  - :issue:`329`: Linked adapters specified with ``-a ADAPTER1...ADAPTER2``
    are no longer anchored by default. To get results consist with the old
    behavior, use ``-a ^ADAPTER1...ADAPTER2`` instead.
  - Support for colorspace data was removed. Thus, the following command-line
    options can no longer be used: ``-c``, ``-d``, ``-t``, ``--strip-f3``,
    ``--maq``, ``--bwa``, ``--no-zero-cap``.
  - “Legacy mode” has been removed. This mode was enabled under certain
    conditions and would change the behavior such that the read-modifying
    options such as ``-q`` would only apply to the forward/R1 reads. This was
    necessary for compatibility with old Cutadapt versions, but became
    increasingly confusing.
  - :issue:`360`: Computation of the error rate of an adapter match no longer
    counts the ``N`` wildcard bases. Previously, an adapter like ``N{18}CC``
    (18 ``N`` wildcards followed by ``CC``) would effectively match
    anywhere because the default error rate of 0.1 (10%) would allow for
    two errors. The error rate of a match is now computed as
    the number of non-``N`` bases in the matching part of the adapter
    divided by the number of errors.
  - This release of Cutadapt requires at least Python 3.4 to run. Python 2.7
    is no longer supported.
- Features
  - A progress indicator is printed while Cutadapt is working. If you redirect
    standard error to a file, the indicator is disabled.
  - Reading of FASTQ files has gotten faster due to a new parser. The FASTA
    and FASTQ reading/writing functions are now available as part of the
    `dnaio library <https://github.com/marcelm/dnaio/>`_. This is a separate
    Python package that can be installed independently from Cutadapt.
    There is one regression at the moment: FASTQ files that use a second
    header (after the "+") will have that header removed in the output.
  - Some other performance optimizations were made. Speedups of up to 15%
    are possible.
  - Demultiplexing has become a lot faster :ref:`under certain conditions
    <speed-up-demultiplexing>`.
  - :issue:`335`: For linked adapters, it is now possible to :ref:`specify
    which of the two adapters should be required <linked-override>`, overriding
    the default.
  - :issue:`166`: By specifying ``--action=lowercase``, it is now possible
    to not trim adapters, but to instead convert the section of the read
    that would have been trimmed to lowercase.
- Bug fixes
  - Removal of legacy mode fixes also :issue:`345`: ``--length`` would not
    enable legacy mode.
  - The switch to ``dnaio`` also fixed :issue:`275`: Input files with
    non-standard names now no longer lead to a crash. Instead the format
    is now recognized from the file content.
  - Fix :issue:`354`: Sequences given using ``file:`` can now be unnamed.
  - Fix :issue:`257` and :issue:`242`: When only R1 or only R2 adapters are
    given, the ``--pair-filter`` setting is now forced to ``both`` for the
    ``--discard-untrimmed`` (and ``--untrimmed-(paired-)output``) filters.
    Otherwise, with the default ``--pair-filter=any``, all pairs would be
    considered untrimmed because one of the reads in the pair is always
    untrimmed.
- Other
  - :issue:`359`: The ``-f``/``--format`` option is now ignored and a warning
    will be printed if it is used. The input file format is always
    auto-detected.

* Fri Sep 14 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.18-1
- Features
  - Close #327: Maximum and minimum lengths can now be specified separately for
    R1 and R2 with -m LENGTH1:LENGTH2. One of the lengths can be omitted, in
    which case only the length of the other read is checked (as in -m 17: or -m
    :17).
  - Close #322: Use -j 0 to auto-detect how many cores to run on. This should
    even work correctly on cluster systems when Cutadapt runs as a batch job to
    which fewer cores than exist on the machine have been assigned. Note that
    the number of threads used by pigz cannot be controlled at the moment, see
    #290.
  - Close #225: Allow setting the maximum error rate and minimum overlap length
    per adapter. A new syntax for adapter-specific parameters was added for
    this. Example: -a "ADAPTER;min_overlap=5".
  - Close #152: Using the new syntax for adapter-specific parameters, it is now
    possible to allow partial matches of a 3' adapter at the 5' end (and
    partial matches of a 5' adapter at the 3' end) by specifying the anywhere
    parameter (as in -a "ADAPTER;anywhere").
  - Allow --pair-filter=first in addition to both and any. If used, a read pair
    is discarded if the filtering criterion applies to R1; and R2 is ignored.
  - Close #112: Implement a --report=minimal option for printing a succinct
    two-line report in tab-separated value (tsv) format. Thanks to @jvolkening
    for coming up with an initial patch!
- Bug fixes
  - Fix #128: The "Reads written" figure in the report incorrectly included
    both trimmed and untrimmed reads if --untrimmed-output was used.
- Other
  - The options --no-trim and --mask-adapter should now be written as
    --action=mask and --action=none. The old options still work.
  - This is the last release to support colorspace data.
  - This is the last release to support Python 2.

* Fri Aug 24 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.17-1
- Close :issue:`53`: Implement adapters :ref:`that disallow internal matches
  <non-internal>`. This is a bit like anchoring, but less strict: The adapter
  sequence can appear at different lengths, but must always be at one of the
  ends. Use ``-a ADAPTERX`` (with a literal ``X``) to disallow internal matches
  for a 3' adapter. Use ``-g XADAPTER`` to disallow for a 5' adapter.
- :user:`klugem` contributed PR :issue:`299`: The ``--length`` option (and its
  alias ``-l``) can now be used with negative lengths, which will remove bases
  from the beginning of the read instead of from the end.
- Close :issue:`107`: Add a ``--discard-casava`` option to remove reads that
  did not pass CASAVA filtering (this is possibly relevant only for older
  datasets).
- Fix :issue:`318`: Cutadapt should now be installable with Python 3.7.
- Running Cutadapt under Python 3.3 is no longer supported (Python 2.7 or 3.4+
  are needed)
- Planned change: One of the next Cutadapt versions will drop support for
  Python 2 entirely, requiring Python 3.

* Thu Feb 22 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.16-1
- Install sphinx_issues into docs testenv

* Fri Dec 01 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.15-1
- Require the most recent xopen

* Tue Aug 15 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.14-1
- Fix: Statistics for 3' part of a linked adapter were reported incorrectly
- Fix `issue #244 <https://github.com/marcelm/cutadapt/issues/244>`_: Quality
  trimming with ``--nextseq-trim`` would not apply to R2 when trimming
  paired-end reads.
- ``--nextseq-trim`` now disables legacy mode.
- Fix `issue #246 <https://github.com/marcelm/cutadapt/issues/246>`_:
  installation failed on non-UTF8 locale

