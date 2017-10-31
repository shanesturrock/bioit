%define priority 252
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		vsearch
Version:	2.5.2
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
* Tue Oct 31 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.5.2-1
- Fix bug with '-' not treated as stdin when used as argument to fastq_eestats2
  option.

