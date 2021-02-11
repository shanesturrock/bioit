%define priority 340
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		augustus
Version:	3.4.0
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
   --slave %{_bindir}/aln2wig aln2wig /opt/bioit/%{name}/%{version}/bin/aln2wig \
   --slave %{_bindir}/bam2hints bam2hints /opt/bioit/%{name}/%{version}/bin/bam2hints \
   --slave %{_bindir}/bam2wig bam2wig /opt/bioit/%{name}/%{version}/bin/bam2wig \
   --slave %{_bindir}/compileSpliceCands compileSpliceCands /opt/bioit/%{name}/%{version}/bin/compileSpliceCands \
   --slave %{_bindir}/etraining etraining /opt/bioit/%{name}/%{version}/bin/etraining \
   --slave %{_bindir}/fastBlockSearch fastBlockSearch /opt/bioit/%{name}/%{version}/bin/fastBlockSearch \
   --slave %{_bindir}/filterBam filterBam /opt/bioit/%{name}/%{version}/bin/filterBam \
   --slave %{_bindir}/getSeq getSeq /opt/bioit/%{name}/%{version}/bin/getSeq \
   --slave %{_bindir}/homGeneMapping homGeneMapping /opt/bioit/%{name}/%{version}/bin/homGeneMapping \
   --slave %{_bindir}/joingenes joingenes /opt/bioit/%{name}/%{version}/bin/joingenes \
   --slave %{_bindir}/load2db load2db /opt/bioit/%{name}/%{version}/bin/load2db \
   --slave %{_bindir}/load2sqlitedb load2sqlitedb /opt/bioit/%{name}/%{version}/bin/load2sqlitedb \
   --slave %{_bindir}/pp_simScore pp_simScore /opt/bioit/%{name}/%{version}/bin/pp_simScore \
   --slave %{_bindir}/prepareAlign prepareAlign /opt/bioit/%{name}/%{version}/bin/prepareAlign \
   --slave %{_bindir}/utrrnaseq utrrnaseq /opt/bioit/%{name}/%{version}/bin/utrrnaseq

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove %{name} /opt/bioit/%{name}/%{version}/bin/augustus
fi

%files

%changelog
* Fri Feb 12 2021 Shane Sturrock <shane.sturrock@gmail.com> - 3.4.0-1
- shortrunning (make test) and longrunning tests for monitoring functionality
  and performance
- drop dependency on static bam library, e.g. of bam2wig
- new program pp_simScore to score a protein against a protein profile (.prfl)
- new option --/CompPred/printExonCandsMSA=1 for CGP to produce MSAs of
  candidate coding regions
- new scripts augustify, fix_in_frame_stop_codon_genes.py
- new default: softmasking is assumed
- compile with CGP and ZIPINPUT support by default
- compile with SQLite and MySQL support for CGP (switch of by adding SQLite =
  false and MySQL = false to common.mk)
- new species Cassiopea xamachana, Ptychodera flava, Argopecten irridians,
  Nemopilema nomurai, Notospermus geniculatus, Chrysaora chesapeakeij,
  Ectocarpus siliculosus, Trichoplax adhaerens, Aurelia aurita, Rhopilema
  esculentum, Encephalitozoon cuniculi, Gonapodya prolifera, Dunaliella_salina
  Sordaria macrospora, Sphaceloma murrayae, Vitrella brassicaformis,
  Monoraphidium neglectum, Raphidocelis subcapita, Ostreococcus tauri,
  Ostreococcus sp. lucimarinus, Micromonas pusilla, Micromonas_commoda,
  Chlamydomonas eustigma, Thalassiosira pseudonana, Pseudo-nitzschia
  multistriata, Phaeodactylum tricornutum, Fragilariopsis cylindrus, Fistulifera
  solaris, Bathycoccus prasinos, Chloropicon primus
- added Windows Subsystem for Linux Installation documentation
- fixes of bugs, compiler warnings

* Fri Sep 27 2019 Shane Sturrock <shane.sturrock@gmail.com> - 3.3.3-1
- new script tfix_in_frame_stop_codon_genes.py that replaces genes where
  spliced in-frame stop codons were predicted
- new scripts: compare_masking.pl, merge_masking.pl
- new program bamToWig.py as alternative to bam2wig C++ binary
- fix warnings on new GCC compiler (8.3)
- introduced unit tests of C++ code (make test)
- bugfixes (lex.cc, autoAug.pl)
- DIAMOND as alternative to BLAST in aa2nonred.pl

* Fri Oct 12 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.3.2-1
- bugfixes in comparative augustus, utrrnaseq
- new species Chiloscyllium punctatum (bamboo shark), Scyliorhinus torazame
  (cat shark), Rhincodon typus (whale shark)
- updated comparative augustus (CGP) tutorial

* Fri May 11 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.3.1-1
- new species pisaster (Pisaster ochraceus, ochre starfish)
- bugfixes of sampling error in intron model and in check of
  frame-compatibility of CDSpart hints without frame
- new auxiliary program utrrnaseq to find training UTRs
- new script setStopCodonFreqs.pl

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
