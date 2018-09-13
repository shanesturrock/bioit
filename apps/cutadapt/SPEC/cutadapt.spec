%define priority 118
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		cutadapt
Version:	1.18
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

