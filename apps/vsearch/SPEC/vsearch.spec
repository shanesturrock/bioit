%define priority 271
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		vsearch
Version:	2.7.1
Release:	1%{?dist}
Summary:	An alternative to the USEARCH
Group:		Applications/Engineering
License:	GPLv3 
URL:		https://github.com/torognes/vsearch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
VSEARCH stands for vectorized search, as the tool takes advantage of
parallelism in the form of SIMD vectorization as well as multiple threads to
perform accurate alignments at high speed. VSEARCH uses an optimal global
aligner (full dynamic programming Needleman-Wunsch), in contrast to USEARCH
which by default uses a heuristic seed and extend aligner. This results in more
accurate alignments and overall improved sensitivity (recall) with VSEARCH,
especially for alignments with gaps.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/vsearch vsearch /opt/bioit/%{name}/%{version}/bin/vsearch %{priority} \
   --slave %{_mandir}/man1/vsearch.1 vsearch.1 /opt/bioit/%{name}/%{version}/share/man/man1/vsearch.1

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove vsearch /opt/bioit/%{name}/%{version}/bin/vsearch
fi

%files

%changelog
* Thu Feb 22 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.7.1-1
- 2.7.0
  - Added cluster_unoise, uchime2_denovo and uchime3_denovo commands.
- 2.7.1
  - Fixes several bugs on Windows.

* Tue Jan 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.6.2-1
- Fix for partially inactive xsize option.

* Tue Dec 12 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.6.1-1
- Improved parallelisation of paired end reads merging

* Tue Nov 14 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.6.0-1
- Rewritten paired-end reads merger with improved accuracy. 
- Decreased default value for fastq_minovlen option from 16 to 10. 
- The default value for the fastq_maxdiffs option is increased from 5 to 10. 
- There are now other more important restrictions that will avoid merging reads
  that cannot be reliably aligned.

* Tue Oct 31 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.5.2-1
- Fix bug with '-' not treated as stdin when used as argument to fastq_eestats2
  option.

