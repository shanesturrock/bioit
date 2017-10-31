%define priority 133
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		stringtie
Version:	1.3.3b
Release:	1%{?dist}
Summary:	StringTie is a fast and highly efficient assembler of RNA-Seq alignments into potential transcripts.
Group:		Applications/Engineering
License:	Artistic 2.0
URL:		https://ccb.jhu.edu/software/stringtie/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description

StringTie is a fast and highly efficient assembler of RNA-Seq alignments into
potential transcripts. It uses a novel network flow algorithm as well as an
optional de novo assembly step to assemble and quantitate full-length
transcripts representing multiple splice variants for each gene locus. Its
input can include not only the alignments of raw reads used by other transcript
assemblers, but also alignments longer sequences that have been assembled from
those reads.In order to identify differentially expressed genes between
experiments, StringTie's output can be processed by specialized software like
Ballgown, Cuffdiff or other programs (DESeq2, edgeR, etc.).

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/stringtie stringtie /opt/bioit/%{name}/%{version}/stringtie %{priority} 

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove stringtie /opt/bioit/%{name}/%{version}/stringtie
fi

%files

%changelog
* Tue Oct 31 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.3.3b-1
- fixed the computation of the TPM value that was reported incorrectly somtimes
  in the presence of guides (-G option)
- few other minor fixes
