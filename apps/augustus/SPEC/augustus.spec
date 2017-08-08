%define priority 33
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		augustus
Version:	3.3
Release:	1%{?dist}
Summary:	AUGUSTUS is a gene prediction program for eukaryotes
Group:		Applications/Engineering
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
Augustus can be used as an ab initio program, which means it bases its
prediction purely on the sequence. AUGUSTUS may also incorporate hints on the
gene structure coming from extrinsic sources such as EST, MS/MS, protein
alignments and syntenic genomic alignments. Since version 3.0 AUGUSTUS can also
predict the genes simultaneously in several aligned genomes.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/augustus %{name} /opt/bioit/%{name}/%{version}/bin/augustus %{priority} \
   --slave %{_bindir}/bam2hints bam2hints /opt/bioit/%{name}/%{version}/bin/bam2hints \
   --slave %{_bindir}/etraining etraining /opt/bioit/%{name}/%{version}/bin/etraining \
   --slave %{_bindir}/fastBlockSearch fastBlockSearch /opt/bioit/%{name}/%{version}/bin/fastBlockSearch \
   --slave %{_bindir}/filterBam filterBam /opt/bioit/%{name}/%{version}/bin/filterBam \
   --slave %{_bindir}/homGeneMapping homGeneMapping /opt/bioit/%{name}/%{version}/bin/homGeneMapping \
   --slave %{_bindir}/joingenes joingenes /opt/bioit/%{name}/%{version}/bin/joingenes \
   --slave %{_bindir}/prepareAlign prepareAlign /opt/bioit/%{name}/%{version}/bin/prepareAlign

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove %{name} /opt/bioit/%{name}/%{version}/bin/augustus
fi

%files

%changelog
* Tue Aug 08 2017 Shane Sturrock <shane.sturrock@gmail.com> - 3.3-1
- new program ESPOCA to estimate selective pressure on codon alignments
- gene finding on ancestral genomes is enabled
- new default parameters for comparative gene prediction (CGP)
- clade parameters training for CGP
- compatibility to Ian Fiddes' Comparative Annotation Toolkit (CAT)
- new scripts eval_dualdecomp.pl,
- more tolerant tree parsing
- bugfixes in augustus, joingenes, load2sqlitedb, transMap2hints.pl,
  splitMfasta.pl, intron2exex.pl, aln2wig
- new functionality in homGeneMapping, joingenes
- new species ciona, mnemiopsis_leidyi, nematostella_vectensis,
  strongylocentrotus_purpuratus
