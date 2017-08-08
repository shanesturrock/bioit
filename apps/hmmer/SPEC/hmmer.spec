%define priority 3102
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		hmmer
Version:	3.1b2
Release:	1%{?dist}
Summary:	HMMER database search and aligner
Group:		Applications/Engineering
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
HMMER is used for searching sequence databases for sequence homologs, and for
making sequence alignments. It implements methods using probabilistic models
called profile hidden Markov models (profile HMMs). 

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/hmmalign %{name} /opt/bioit/%{name}/%{version}/hmmalign %{priority} \
   --slave %{_bindir}/alimask alimask /opt/bioit/%{name}/%{version}/alimask \
   --slave %{_bindir}/esl-afetch esl-afetch /opt/bioit/%{name}/%{version}/esl-afetch \
   --slave %{_bindir}/esl-alimanip esl-alimanip /opt/bioit/%{name}/%{version}/esl-alimanip \
   --slave %{_bindir}/esl-alimap esl-alimap /opt/bioit/%{name}/%{version}/esl-alimap \
   --slave %{_bindir}/esl-alimask esl-alimask /opt/bioit/%{name}/%{version}/esl-alimask \
   --slave %{_bindir}/esl-alimerge esl-alimerge /opt/bioit/%{name}/%{version}/esl-alimerge \
   --slave %{_bindir}/esl-alipid esl-alipid /opt/bioit/%{name}/%{version}/esl-alipid \
   --slave %{_bindir}/esl-alistat esl-alistat /opt/bioit/%{name}/%{version}/esl-alistat \
   --slave %{_bindir}/esl-cluster esl-cluster /opt/bioit/%{name}/%{version}/esl-cluster \
   --slave %{_bindir}/esl-compalign esl-compalign /opt/bioit/%{name}/%{version}/esl-compalign \
   --slave %{_bindir}/esl-compstruct esl-compstruct /opt/bioit/%{name}/%{version}/esl-compstruct \
   --slave %{_bindir}/esl-construct esl-construct /opt/bioit/%{name}/%{version}/esl-construct \
   --slave %{_bindir}/esl-histplot esl-histplot /opt/bioit/%{name}/%{version}/esl-histplot \
   --slave %{_bindir}/esl-mask esl-mask /opt/bioit/%{name}/%{version}/esl-mask \
   --slave %{_bindir}/esl-reformat esl-reformat /opt/bioit/%{name}/%{version}/esl-reformat \
   --slave %{_bindir}/esl-selectn esl-selectn /opt/bioit/%{name}/%{version}/esl-selectn \
   --slave %{_bindir}/esl-seqrange esl-seqrange /opt/bioit/%{name}/%{version}/esl-seqrange \
   --slave %{_bindir}/esl-seqstat esl-seqstat /opt/bioit/%{name}/%{version}/esl-seqstat \
   --slave %{_bindir}/esl-sfetch esl-sfetch /opt/bioit/%{name}/%{version}/esl-sfetch \
   --slave %{_bindir}/esl-shuffle esl-shuffle /opt/bioit/%{name}/%{version}/esl-shuffle \
   --slave %{_bindir}/esl-ssdraw esl-ssdraw /opt/bioit/%{name}/%{version}/esl-ssdraw \
   --slave %{_bindir}/esl-stranslate esl-stranslate /opt/bioit/%{name}/%{version}/esl-stranslate \
   --slave %{_bindir}/esl-weight esl-weight /opt/bioit/%{name}/%{version}/esl-weight \
   --slave %{_bindir}/hmmbuild hmmbuild /opt/bioit/%{name}/%{version}/hmmbuild \
   --slave %{_bindir}/hmmc2 hmmc2 /opt/bioit/%{name}/%{version}/hmmc2 \
   --slave %{_bindir}/hmmconvert hmmconvert /opt/bioit/%{name}/%{version}/hmmconvert \
   --slave %{_bindir}/hmmemit hmmemit /opt/bioit/%{name}/%{version}/hmmemit \
   --slave %{_bindir}/hmmerfm-exactmatch hmmerfm-exactmatch /opt/bioit/%{name}/%{version}/hmmerfm-exactmatch \
   --slave %{_bindir}/hmmfetch hmmfetch /opt/bioit/%{name}/%{version}/hmmfetch \
   --slave %{_bindir}/hmmlogo hmmlogo /opt/bioit/%{name}/%{version}/hmmlogo \
   --slave %{_bindir}/hmmpgmd hmmpgmd /opt/bioit/%{name}/%{version}/hmmpgmd \
   --slave %{_bindir}/hmmpress hmmpress /opt/bioit/%{name}/%{version}/hmmpress \
   --slave %{_bindir}/hmmscan hmmscan /opt/bioit/%{name}/%{version}/hmmscan \
   --slave %{_bindir}/hmmsearch hmmsearch /opt/bioit/%{name}/%{version}/hmmsearch \
   --slave %{_bindir}/hmmsim hmmsim /opt/bioit/%{name}/%{version}/hmmsim \
   --slave %{_bindir}/hmmstat hmmstat /opt/bioit/%{name}/%{version}/hmmstat \
   --slave %{_bindir}/jackhmmer jackhmmer /opt/bioit/%{name}/%{version}/jackhmmer \
   --slave %{_bindir}/makehmmerdb makehmmerdb /opt/bioit/%{name}/%{version}/makehmmerdb \
   --slave %{_bindir}/nhmmer nhmmer /opt/bioit/%{name}/%{version}/nhmmer \
   --slave %{_bindir}/nhmmscan nhmmscan /opt/bioit/%{name}/%{version}/nhmmscan \
   --slave %{_bindir}/phmmer phmmer /opt/bioit/%{name}/%{version}/phmmer

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove %{name} /opt/bioit/%{name}/%{version}/hmmalign
fi

%files

%changelog
* Tue Aug 08 2017 Shane Sturrock <shane.sturrock@gmail.com> - 3.1b2-1
- New heuristic for accelerating nhmmer roughly 10-fold. 

  We have developed a new algorithm that accelerates DNA search in 
  nhmmer. The acceleration can be tuned, such that greater speed will
  tend to decrease sensitivity. The default settings yield roughly 
  10-fold acceleration while retaining nearly complete sensitivity 
  among hits with E-value < 1e-3 (with a modest loss in sensitivity 
  among marginal hits with  E > 1e-3)
  
  This algorithm requires that the sequence database first be 
  preprocessed into a binary file format. The new tool makehmmerdb 
  performs this task.
  
- New method of deciding if a sequence is a fragment. 
  
  If hmmbuild determines that a sequence is a fragment, all leading and 
  trailing gap symbols (all gaps before the first residue and after the 
  last residue) are treated as missing data symbols, and thus do not 
  count as observed gaps.
  
  In H3.0 and H3.1b1, a sequence was called a fragment if its length was
  less than a specified fraction of the alignment length. In the case of 
  alignments with many sequences, this often resulted in all sequences
  being labeled as fragments, which could lead to unexpected terminal 
  match states when a small fraction of sequences contained a long 
  terminal extension. Now, a sequence is labeled a fragment if its range 
  in the alignment (the number of alignment columns between the first 
  and last positions of the sequence) is not greater than a specified 
  fraction of the full alignment length. This should improve HMMER's 
  ability to model alignments with ragged ends.

- Other changes include:

  - The DNA search tool, nhmmer, depends on a value MAXL, which hmmbuild
    computes as an assertion of the maximum length at which HMMER 
    expects to see an instance of the model. This value could previously 
    become excessively long when building a model from an alignment with 
    many long insertions. The MAXL value computed by hmmbuild for DNA 
    alignments is now limited to 20*M, where M is the # of match states.
  
  - A new tool, called hmmlogo, that computes letter height and indel
    parameters that can be used to produce a profile HMM logo. This tool
    can be thought of as a command-line interface for the data underlying
    the Skylign logo server (skylign.org).

- Bugfixes:
  
  - #h100 hmmalign would segfault on a zero length input sequence. 
  
  - #h101 hmmsearch would segfault when searching a DNA HMM against a 
          protein db (on Linux only).
  
  - #h102 Marginal hits late in a target sequence database were subject 
          to being filtered in an nhmmer search. This was due to a score 
          filter that (a) was intended to accelerate search, but had 
          essentially no impact on speed, and (b) was an overly 
          aggressive filter. Removed the filter.
  
  - #h103 Error printing very small E-values. Closely related to #h98, 
          but occuring in the main thread (#h98 fixed the same problem
          in worker threads).
  
  - #h104 HMMER would not compile on OpenBSD, because netinet/in.h was
          not included. This header file is included via arpa/inet.h 
          on most other systems, but not on OpenBSD.
  
  - #h105 Errors encountered while running 'make clean' and 'make distclean'
          in binary builds. This was the result of the Makefile trying to
          remove the userguide folder and LICENSE.txt file, which are 
          already removed in the release process. The Makefile now accounts
          for this possibility.
          
  - #h106 H3 failed to read some old H2 HMM files. This happened in the 
          cases that (1) there was an empty DESC field in the file, or (2) 
          the model was not normalized. Both cases have been resolved.
          
  - #h107 hmmsim only worked for Amino Acid models. It now works for 
          nucleotide models, also.
