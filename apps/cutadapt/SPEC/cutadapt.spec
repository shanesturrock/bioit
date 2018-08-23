%define priority 117
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		cutadapt
Version:	1.17
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

