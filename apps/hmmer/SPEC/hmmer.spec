%define priority 3301
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		hmmer
Version:	3.3.1
Release:	2%{?dist}
Summary:	HMMER database search and aligner
Group:		Applications/Engineering
License:	BSD
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
   --install %{_bindir}/hmmalign %{name} /opt/bioit/%{name}/%{version}/bin/hmmalign %{priority} \
   --slave %{_bindir}/alimask alimask /opt/bioit/%{name}/%{version}/bin/alimask \
   --slave %{_bindir}/esl-afetch esl-afetch /opt/bioit/%{name}/%{version}/bin/esl-afetch \
   --slave %{_bindir}/esl-alimanip esl-alimanip /opt/bioit/%{name}/%{version}/bin/esl-alimanip \
   --slave %{_bindir}/esl-alimap esl-alimap /opt/bioit/%{name}/%{version}/bin/esl-alimap \
   --slave %{_bindir}/esl-alimask esl-alimask /opt/bioit/%{name}/%{version}/bin/esl-alimask \
   --slave %{_bindir}/esl-alimerge esl-alimerge /opt/bioit/%{name}/%{version}/bin/esl-alimerge \
   --slave %{_bindir}/esl-alipid esl-alipid /opt/bioit/%{name}/%{version}/bin/esl-alipid \
   --slave %{_bindir}/esl-alirev esl-alirev /opt/bioit/%{name}/%{version}/bin/esl-alirev \
   --slave %{_bindir}/esl-alistat esl-alistat /opt/bioit/%{name}/%{version}/bin/esl-alistat \
   --slave %{_bindir}/esl-compalign esl-compalign /opt/bioit/%{name}/%{version}/bin/esl-compalign \
   --slave %{_bindir}/esl-compstruct esl-compstruct /opt/bioit/%{name}/%{version}/bin/esl-compstruct \
   --slave %{_bindir}/esl-construct esl-construct /opt/bioit/%{name}/%{version}/bin/esl-construct \
   --slave %{_bindir}/esl-histplot esl-histplot /opt/bioit/%{name}/%{version}/bin/esl-histplot \
   --slave %{_bindir}/esl-mask esl-mask /opt/bioit/%{name}/%{version}/bin/esl-mask \
   --slave %{_bindir}/esl-reformat esl-reformat /opt/bioit/%{name}/%{version}/bin/esl-reformat \
   --slave %{_bindir}/esl-selectn esl-selectn /opt/bioit/%{name}/%{version}/bin/esl-selectn \
   --slave %{_bindir}/esl-seqrange esl-seqrange /opt/bioit/%{name}/%{version}/bin/esl-seqrange \
   --slave %{_bindir}/esl-seqstat esl-seqstat /opt/bioit/%{name}/%{version}/bin/esl-seqstat \
   --slave %{_bindir}/esl-sfetch esl-sfetch /opt/bioit/%{name}/%{version}/bin/esl-sfetch \
   --slave %{_bindir}/esl-shuffle esl-shuffle /opt/bioit/%{name}/%{version}/bin/esl-shuffle \
   --slave %{_bindir}/esl-ssdraw esl-ssdraw /opt/bioit/%{name}/%{version}/bin/esl-ssdraw \
   --slave %{_bindir}/esl-translate esl-translate /opt/bioit/%{name}/%{version}/bin/esl-translate \
   --slave %{_bindir}/esl-weight esl-weight /opt/bioit/%{name}/%{version}/bin/esl-weight \
   --slave %{_bindir}/hmmalign hmmalign /opt/bioit/%{name}/%{version}/bin/hmmalign \
   --slave %{_bindir}/hmmbuild hmmbuild /opt/bioit/%{name}/%{version}/bin/hmmbuild \
   --slave %{_bindir}/hmmconvert hmmconvert /opt/bioit/%{name}/%{version}/bin/hmmconvert \
   --slave %{_bindir}/hmmemit hmmemit /opt/bioit/%{name}/%{version}/bin/hmmemit \
   --slave %{_bindir}/hmmfetch hmmfetch /opt/bioit/%{name}/%{version}/bin/hmmfetch \
   --slave %{_bindir}/hmmlogo hmmlogo /opt/bioit/%{name}/%{version}/bin/hmmlogo \
   --slave %{_bindir}/hmmpgmd hmmpgmd /opt/bioit/%{name}/%{version}/bin/hmmpgmd \
   --slave %{_bindir}/hmmpress hmmpress /opt/bioit/%{name}/%{version}/bin/hmmpress \
   --slave %{_bindir}/hmmscan hmmscan /opt/bioit/%{name}/%{version}/bin/hmmscan \
   --slave %{_bindir}/hmmsearch hmmsearch /opt/bioit/%{name}/%{version}/bin/hmmsearch \
   --slave %{_bindir}/hmmsim hmmsim /opt/bioit/%{name}/%{version}/bin/hmmsim \
   --slave %{_bindir}/hmmstat hmmstat /opt/bioit/%{name}/%{version}/bin/hmmstat \
   --slave %{_bindir}/jackhmmer jackhmmer /opt/bioit/%{name}/%{version}/bin/jackhmmer \
   --slave %{_bindir}/makehmmerdb makehmmerdb /opt/bioit/%{name}/%{version}/bin/makehmmerdb \
   --slave %{_bindir}/nhmmer nhmmer /opt/bioit/%{name}/%{version}/bin/nhmmer \
   --slave %{_bindir}/nhmmscan nhmmscan /opt/bioit/%{name}/%{version}/bin/nhmmscan \
   --slave %{_bindir}/phmmer phmmer /opt/bioit/%{name}/%{version}/bin/phmmer

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove %{name} /opt/bioit/%{name}/%{version}/bin/hmmalign
fi

%files

%changelog
* Fri Aug 14 2020 Shane Sturrock <shane.sturrock@gmail.com> - 3.3.1-1
- Most important changes:
  - Default sequence weighting behavior was slightly changed, making it
    independent of whether an RF reference annotation line is present on
    the input alignment or not. Previously, we used the RF line (if
    present) to define consensus columns. This would mean that
    reformatting the same alignment from Stockholm format (with
    reference column annotation) to aligned FASTA format (without it)
    would result in different profile HMM parameters, because of small
    differences in sequence weighting. (iss #180)
  - Revised how nhmmer guesses whether an input query file consists of
    single sequence(s), multiple sequence alignment(s), or profile
    HMM(s). `--qformat` allows user to specify input sequence file format
    (unaligned or aligned formats) and override the guesser;
    `--qsingle_seqs` allows an MSA format to be read as set(s) of single
    query sequences instead of as MSA(s). Also, fixed a problem where
    nhmmer would run on a protein target sequence file without complaint.
    (iss #171, iss #196, PR #194)
- bug fixes:
  - The comparison engine used by hmmsearch, hmmscan, phmmer, and
    jackhmmer has a design limit of 100K residues for target sequence
    length (usually protein sequences, sometimes RNA transcripts).  Only
    nhmmer/nhmmscan are designed for searching arbitrary length genome
    sequences. That limit was not being enforced, and it was possible
    for a user to run hmmsearch inadvertently instead of nhmmer, which
    can cause numerical overflows and give infinite scores, among other
    problems. The comparison engine now exits with an error if the
    target sequence length is >100K.
  - nhmmer now gives a less confusing error message when it tries to
    open a sequence file as FMindex format and fails. (iss #195, PR
    #200)
  - fixed a problem where nhmmer failed to reset its background model
    composition after p7_Decoding() fails with a range error on highly
    repetitive sequence, causing remainder of target sequence
    comparisons to be performed with a corrupted bg. (iss #198, PR
    #199).
  - removed a stray printf() from nhmmer.
  - fixed a problem where if p7_Decoding() failed with a range error on
    a highly repetitive sequence, a trace structure wasn't being reused
    properly, and it could throw an exception with `trace not empty;
    needs to be Reuse()'d?`. (PR #191)
  - `nhmmscan --aliscoreout` was segfaulting. The `--aliscoreout` option
    was only present in nhmmer for some experiment anyway, and was never
    hooked up in hmmscan. Fixed by removing the option. (iss #190)
  - fixed p7_gmx_utest unit test failures (segfaults and malloc
    failures) for large L,M inputs. (iss #176)
  - fixed a problem where nhmmer's sequence windows, when scanning a
    long target sequence, depended on previous sequences in the file,
    thus meaning that subseq windows depended on target database
    order. In some cases, this could affect whether hits were or were
    not found. The fix introduces a flag in esl_sqio_ReadBlock() that
    makes sequence window choices reproducible. (PR #174)
  - fixed possible buffer overflow in
    p7_tophits_GetMaxPositionLength(). (Did not occur in practice;
    required a terabase of target sequence to exercise.)
  - fixed p7_hmmd_search_stats unit test problems with memory corruption
    and leaks, detected on OS/X.
  - fixed problem with `make check` failing on hmmc2 on FreeBSD.

* Fri Dec 06 2019 Shane Sturrock <shane.sturrock@gmail.com> - 3.3-1
- most important changes:
  - We improved the `hmmpgmd` search daemon. (`hmmpgmd` is the compute server
    used at EBI to support their HMMER web servers.) Now `hmmpgmd` handles
    large target sequence databases more efficiently by using "sharding". 
    Instead of loading the entire target sequence database into memory on every
    node, a target database can be sharded across multiple nodes. The `hmmpgmd`
    daemon also now has its own user guide.
  - We improved how we calculate our default sequence weights (Henikoff
    position-based weights), especially on deep alignments of 10-100K+
    sequences. Now we calculate PB weights only on consensus columns, not all
    columns. This avoids some cases of artifactually extreme weights on very
    gappy alignments. We also changed to a better rule for defining sequence
    fragments. These changes give a small improvement in
    sensitivity/specificity benchmarking of HMMER/Pfam searches, and
    substantial speed improvements in building profiles on deep alignments.
    Because of these changes, profile HMMs built with version 3.3 give slightly
    different scores compared to previous HMMER3 versions.
  - Fixed a bug in the `hmmstat` "compKL" (composition KL divergence)
    calculation, which was off by a constant. Now it is reported as a standard
    KL divergence in bits.
- bug fixes:
  - fixed a bug where in some rare and complicated situations, `nhmmer` could
    report overlapping envelopes on reverse strand. [iss#159]
  - Several bugs were fixed in MPI mode, including iss#157 (`hmmsim --mpi` was
    always segfaulting, even on simple examples) and iss#154 (problems in
    `hmmscan` that were corrupting output data).
  - Fixed some 32-bit integer overflow bugs in `hmmpgmd`.
  - Fixed a bug in the `hmmstat` "compKL" (composition KL divergence)
    calculation, which was off by a constant. Now it is reported as a standard
    KL divergence in bits.
  - Fixed a bug where `hmmconvert --outfmt` wasn't recognizing `3/f` as a
    format.
- Smaller changes
  - Our fasta format parser now detects aligned FASTA format (.afa files) more
    robustly, and will not attempt to read a .afa file as an unaligned sequence
    file. [iss#153]
  - Our `make check` tests depend on Python >= 3.5. Added checks in
    `./configure` and `make` to fail gracefully if python3 isn't available.
  - `./configure` now always calls `AC_PROG_CC_STDC` to add compiler flags for
    C99 (even with icc).
  - Removed undocumented `--{tmm,tmi,tmd,tim,tii,tdm,tdd}` options from
    hmmbuild.
  - Data serialization routines (used in `hmmpgmd`) were rewritten and
    improved.

* Thu Jun 13 2019 Shane Sturrock <shane.sturrock@gmail.com> - 3.2.1-2
- Fixed some faulty symlinks

* Tue Jul 10 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.2.1-1
- Larger changes:
  - HMMER is now distributed under the BSD license, instead of the GPL.
  - The 'make install' has been streamlined. Now we install only
    programs and man pages, for 18 HMMER programs and 22 Easel miniapps.
    We don't install development .h headers or .a libraries.
  - We changed our default policy on the number of threads/cores that
    the search programs use. Previously multithreaded programs would use
    all available cores by default; now we use two worker threads by
    default (~2 cores), if multiple cores are available. HMMER3 search
    programs do not scale much beyond 2 cores anyway, due to input
    saturation and memory use.
  - H3 now strictly requires either SSE2 or Altivec/VMX vector
    support. The portable 'dummy' implementation has been removed. This
    was an non-vectorized portable pure C implementation, much slower
    than HMMER3 on x86 and PowerPC platforms with SSE2 or Altivec/VMX
    vector instructions. We had included it because we could -- HMMER3
    implements "generic" non-vectorized versions of its core algorithms
    for unit testing purposes anyway. We thought maybe it'd be useful.
    As far as I can tell, it was never useful, but several packagers on
    non-x86, non-PowerPC platforms packaged and distributed it, ignoring
    the prominent health warnings we put on it.
- Smaller new features include:
  - improved documentation of --mxfile and score matrix file format
  - adds support for EBI's "uncheck all hits" on jackhmmer web site
  - removed experimental hmmbuild --seq_weights_r and --seq_weights_e options
  - appeased new gcc6 --Wmisleading-indentation warning
  - SSI indexing is now robust against duplicate keys
  - autoconf now robust against someone running gnu `autoheader`
  - improved autoconf of SIMD vector support
  - improved autoconf of DAZ,FTZ support on x86 processors
  - improved autodetection of phylip interleaved vs sequential format
  - improved autodetection of A2M vs. aligned FASTA format
  - clarified A2M format parse error when file contains 'O' residue 
  - improved portability to Intel/Solaris
  - FASTA parser now ignores description line after a ctrl-A
  - MSAs output with -A option now include name, acc, desc, author markup.
  - In Easel miniapps, esl-translate replaces previous (buggy) esl-stranslate.
  - Easel miniapps include esl-alirev, reverse complementing RNA/DNA alignment
  - nhmmer/nhmmscan now allow alignments as target dbs
  - target relentropy for DNA models changed from 0.45 to 0.62
  - updated the User Guide
- Fixed bugs include:
  - nhmmscan faulted on old model files because it expected MAXL field
  - --cut-ga wasn't checking that GA line was actually present in model
  - GA thresholds weren't being captured from DNA/RNA Stockholm alignments
  - A2M alignment parsing was corrupted on lines ending in insertions
  - alphabet-guessing failed for FASTA seq >4096 bytes and <4000 residues
  - genbank to fasta format conversion was leaving extra \n in accession
  - NCBI db format: multithreaded nhmmer was failing to read 
  - NCBI db format: 1st database sequence was skipped for second query (#e6)
  - unit test failures in esl_normal, esl_random due to floating point math
  - nhmmer was corrupted by * symbols in input sequence (iss#118)
  - hmmsearch -A crashed if top-ranked hit has no domains (iss#131)
  - new variety of "backconverted subseq" hmmsearch crash on *'s (iss#135)
  - qsort() callbacks now return -1/0/1 as they should. (Infernal iss#11)
  - esl_buffer hangs when input ends with \r (Easel iss#23) 

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
