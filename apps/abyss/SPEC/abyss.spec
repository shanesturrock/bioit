%define priority 224
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		abyss
Version:	2.2.4
Release:	1%{?dist}
Summary:	Sequence assembler for short reads
Group:		Applications/Engineering
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
ABySS is a de novo, parallel, paired-end sequence assembler that is designed
for short reads. The single-processor version is useful for assembling genomes
up to 100 Mbases in size. The parallel version is implemented using MPI and
is capable of assembling larger genomes.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/ABYSS %{name} /opt/bioit/%{name}/%{version}/bin/ABYSS %{priority} \
   --slave %{_bindir}/ABYSS-P ABYSS-P /opt/bioit/%{name}/%{version}/bin/ABYSS-P \
   --slave %{_bindir}/abyss-align abyss-align /opt/bioit/%{name}/%{version}/bin/abyss-align \
   --slave %{_bindir}/abyss-bloom abyss-bloom /opt/bioit/%{name}/%{version}/bin/abyss-bloom \
   --slave %{_bindir}/abyss-bloom-dbg abyss-bloom-dbg /opt/bioit/%{name}/%{version}/bin/abyss-bloom-dbg \
   --slave %{_bindir}/abyss-bloom-dist.mk abyss-bloom-dist.mk /opt/bioit/%{name}/%{version}/bin/abyss-bloom-dist.mk \
   --slave %{_bindir}/abyss-bowtie abyss-bowtie /opt/bioit/%{name}/%{version}/bin/abyss-bowtie \
   --slave %{_bindir}/abyss-bowtie2 abyss-bowtie2 /opt/bioit/%{name}/%{version}/bin/abyss-bowtie2 \
   --slave %{_bindir}/abyss-bwa abyss-bwa /opt/bioit/%{name}/%{version}/bin/abyss-bwa \
   --slave %{_bindir}/abyss-bwamem abyss-bwamem /opt/bioit/%{name}/%{version}/bin/abyss-bwamem \
   --slave %{_bindir}/abyss-bwasw abyss-bwasw /opt/bioit/%{name}/%{version}/bin/abyss-bwasw \
   --slave %{_bindir}/abyss-db-txt abyss-db-txt /opt/bioit/%{name}/%{version}/bin/abyss-db-txt \
   --slave %{_bindir}/abyss-dida abyss-dida /opt/bioit/%{name}/%{version}/bin/abyss-dida \
   --slave %{_bindir}/abyss-fac abyss-fac /opt/bioit/%{name}/%{version}/bin/abyss-fac \
   --slave %{_bindir}/abyss-fatoagp abyss-fatoagp /opt/bioit/%{name}/%{version}/bin/abyss-fatoagp \
   --slave %{_bindir}/abyss-filtergraph abyss-filtergraph /opt/bioit/%{name}/%{version}/bin/abyss-filtergraph \
   --slave %{_bindir}/abyss-fixmate abyss-fixmate /opt/bioit/%{name}/%{version}/bin/abyss-fixmate \
   --slave %{_bindir}/abyss-fixmate-ssq abyss-fixmate-ssq /opt/bioit/%{name}/%{version}/bin/abyss-fixmate-ssq \
   --slave %{_bindir}/abyss-gapfill abyss-gapfill /opt/bioit/%{name}/%{version}/bin/abyss-gapfill \
   --slave %{_bindir}/abyss-gc abyss-gc /opt/bioit/%{name}/%{version}/bin/abyss-gc \
   --slave %{_bindir}/abyss-index abyss-index /opt/bioit/%{name}/%{version}/bin/abyss-index \
   --slave %{_bindir}/abyss-junction abyss-junction /opt/bioit/%{name}/%{version}/bin/abyss-junction \
   --slave %{_bindir}/abyss-kaligner abyss-kaligner /opt/bioit/%{name}/%{version}/bin/abyss-kaligner \
   --slave %{_bindir}/abyss-layout abyss-layout /opt/bioit/%{name}/%{version}/bin/abyss-layout \
   --slave %{_bindir}/abyss-longseqdist abyss-longseqdist /opt/bioit/%{name}/%{version}/bin/abyss-longseqdist \
   --slave %{_bindir}/abyss-map abyss-map /opt/bioit/%{name}/%{version}/bin/abyss-map \
   --slave %{_bindir}/abyss-map-ssq abyss-map-ssq /opt/bioit/%{name}/%{version}/bin/abyss-map-ssq \
   --slave %{_bindir}/abyss-mergepairs abyss-mergepairs /opt/bioit/%{name}/%{version}/bin/abyss-mergepairs \
   --slave %{_bindir}/abyss-overlap abyss-overlap /opt/bioit/%{name}/%{version}/bin/abyss-overlap \
   --slave %{_bindir}/abyss-paired-dbg abyss-paired-dbg /opt/bioit/%{name}/%{version}/bin/abyss-paired-dbg \
   --slave %{_bindir}/abyss-pe abyss-pe /opt/bioit/%{name}/%{version}/bin/abyss-pe \
   --slave %{_bindir}/abyss-samtoafg abyss-samtoafg /opt/bioit/%{name}/%{version}/bin/abyss-samtoafg \
   --slave %{_bindir}/abyss-scaffold abyss-scaffold /opt/bioit/%{name}/%{version}/bin/abyss-scaffold \
   --slave %{_bindir}/abyss-sealer abyss-sealer /opt/bioit/%{name}/%{version}/bin/abyss-sealer \
   --slave %{_bindir}/abyss-stack-size abyss-stack-size /opt/bioit/%{name}/%{version}/bin/abyss-stack-size \
   --slave %{_bindir}/abyss-tabtomd abyss-tabtomd /opt/bioit/%{name}/%{version}/bin/abyss-tabtomd \
   --slave %{_bindir}/abyss-todot abyss-todot /opt/bioit/%{name}/%{version}/bin/abyss-todot \
   --slave %{_bindir}/abyss-tofastq abyss-tofastq /opt/bioit/%{name}/%{version}/bin/abyss-tofastq \
   --slave %{_bindir}/AdjList AdjList /opt/bioit/%{name}/%{version}/bin/AdjList \
   --slave %{_bindir}/Consensus Consensus /opt/bioit/%{name}/%{version}/bin/Consensus \
   --slave %{_bindir}/DAssembler DAssembler /opt/bioit/%{name}/%{version}/bin/DAssembler \
   --slave %{_bindir}/DistanceEst DistanceEst /opt/bioit/%{name}/%{version}/bin/DistanceEst \
   --slave %{_bindir}/DistanceEst-ssq DistanceEst-ssq /opt/bioit/%{name}/%{version}/bin/DistanceEst-ssq \
   --slave %{_bindir}/KAligner KAligner /opt/bioit/%{name}/%{version}/bin/KAligner \
   --slave %{_bindir}/konnector konnector /opt/bioit/%{name}/%{version}/bin/konnector \
   --slave %{_bindir}/logcounter logcounter /opt/bioit/%{name}/%{version}/bin/logcounter \
   --slave %{_bindir}/MergeContigs MergeContigs /opt/bioit/%{name}/%{version}/bin/MergeContigs \
   --slave %{_bindir}/MergePaths MergePaths /opt/bioit/%{name}/%{version}/bin/MergePaths \
   --slave %{_bindir}/Overlap Overlap /opt/bioit/%{name}/%{version}/bin/Overlap \
   --slave %{_bindir}/ParseAligns ParseAligns /opt/bioit/%{name}/%{version}/bin/ParseAligns \
   --slave %{_bindir}/PathConsensus PathConsensus /opt/bioit/%{name}/%{version}/bin/PathConsensus \
   --slave %{_bindir}/PathOverlap PathOverlap /opt/bioit/%{name}/%{version}/bin/PathOverlap \
   --slave %{_bindir}/PopBubbles PopBubbles /opt/bioit/%{name}/%{version}/bin/PopBubbles \
   --slave %{_bindir}/SimpleGraph SimpleGraph /opt/bioit/%{name}/%{version}/bin/SimpleGraph \
   --slave %{_mandir}/man1/ABYSS.1 ABYSS.1 /opt/bioit/%{name}/%{version}/share/man/man1/ABYSS.1 \
   --slave %{_mandir}/man1/abyss-pe.1 abyss-pe.1 /opt/bioit/%{name}/%{version}/share/man/man1/abyss-pe.1 \
   --slave %{_mandir}/man1/abyss-tofastq.1 abyss-tofastq.1 /opt/bioit/%{name}/%{version}/share/man/man1/abyss-tofastq.1 

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove %{name} /opt/bioit/%{name}/%{version}/bin/ABYSS
fi

%files

%changelog
* Thu Feb 06 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.2.4-1
- 2.2.2
  - Fix abyss-overlap for 32-bit systems
- 2.2.3
  - Revert memory consumption of Bloom filters to pre 2.2.0 behaviour.
    ABySS will now share the specified memory among all Bloom filters
    instead of just the counting Bloom filter.
  - Fix gcc-9 compilation warnings
- 2.2.4
  - General:
    - Refactor deprecated functions in clang-8
  - Sealer:
    - Remove unsupported -D option from help page
  - abyss-bloom:
    - Add counting Bloom Filter instruction to help page
  - abyss-bloom-dbg:
    - Report coverage information of unitigs

* Fri Aug 16 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.2.1-1
- Release version 2.2.1
- Fix abyss-bloom for macOS

* Fri Aug 09 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.2.0-1
- Construct a counting bloom filter instead of a cascading bloom filter.
- abyss-bloom:
  - Add 'counting' as valid argument to '-t' option to build a counting bloom
    filter

* Fri Dec 07 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.5-1
- Compiler fixes and increase stack size limits to avoid stack overflows.
- Abyss-pe:
  - Add 'ulimit' statements to the Makefile to increase a thread's stack size
    to 64MB.

* Fri Nov 16 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.4-1
- This release provides major improvements to Bloom filter assembly contiguity
  and correctness. Bloom filter assemblies now have equivalent scaffold
  contiguity and better correctness than MPI assemblies of the same data, while
  still requiring less than 1/10th of the memory. On human, Bloom filter
  assembly times are still a few hours longer than MPI assemblies (e.g. 17
  hours vs. 13 hours, using 48 threads).
- Abyss-pe:
  - Change default value of m from 50 => 0, which has the effect of disallowing
    sequence overlaps < k-1 bp. QUAST tests on E. coli / C. elegans / H.
    sapiens showed that both contiguity and correctness were improved by
    allowing only overlaps of k-1 bp between sequence ends.

* Fri Nov 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.3-1
- This release fixes a SAM-formatting bug that broke the ABySS-LR pipeline
  (Tigmint/ARCS).
- Abyss-bloom:
  - Added graph command for visualizing neighbourhoods of the Bloom filter de
    Bruijn graph (produces GraphViz)
- Abyss-fixmate-ssq:
  - Fixed missing tab in SAM output which broke ABySS linked reads pipeline
    (Tigmint/ARCS)

* Fri Oct 26 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.2-1
- This release improves scaffold N50 on human by ~10%, due to implementation of
  a new --median option for DistanceEst (thanks to @lcoombe!).
- This release also adds a new --max-cost option for konnector and abyss-sealer
  that curbs indeterminately long running times, particularly at low k values.
- abyss-pe:
  - Use the new DistanceEst --median option as the default for the scaffolding
    stage
- Dockerfile:
  - Fix OpenMPI setup
- DistanceEst:
  - Added --median option
- konnector:
  - Added --max-cost option to bound running time
- sealer:
  - Added --max-cost option to bound running time

* Fri Sep 14 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.1-1
- This release provides bug fixes and modest improvements to Bloom filter
  assembly contiguity/correctness. Parallelization of Sealer has also been
  improved, thanks to contributions by @schutzekatze.
- Abyss-bloom-dbg:
  - upgrade to most recent version of ntHash to reduce some assembly/hashing
    artifacts. On a human assembly, this reduced QUAST major misassemblies by
    5% and increased scaffold contiguity by 10%
  - kc parameter now also applies to MPI assemblies (see below)
- Abyss-fac:
  - change N20 and N80 to N25 and N75, respectively
- ABYSS-P:
  - add --kc option, with implements a hard minimum k-mer multiplicity cutoff
- Abyss-pe:
  - fix zsh: no such option: pipefail error with old versions of zsh (fallback
    to bash instead)
  - adding time=1 now times all assembly commands
- Abyss-sealer:
  - parallelize gap sealing with OpenMP (thanks to @schutzekatze!)
  - add --gap-file option (thanks to @schutzekatze!)
- DistanceEst:
  - add support for GFA output

* Fri Apr 20 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.0-1
- This release adds support for misassembly correction and scaffolding using
  linked reads, using Tigmint and ARCS. (Tigmint and ARCS must be installed
  separately.) In addition, simultaneous optimization of s (seed length) and n
  (min supporting read pairs / Chromium barcodes) is now supported during
  scaffolding.
- Abyss-longseqdist:
  - Fix hang on input SAM containing no alignments with MAPQ > 0
- Abyss-pe:
  - New lr parameter. Provide linked reads (i.e. 10x Genomics Chromium reads)
    via this parameter to perform misassembly correction and scaffolding using
    Chromium barcode information.
  - Requires Tigmint and ARCS tools to be installed in addition to ABySS.
  - Fix bug where j (threads) was not being correctly passed to to bgzip/pigz
  - Fix bug where zsh time/memory profiling was not being used, even when zsh
    was available
- Abyss-scaffold:
  - Simultaneous optimization of n and s using line search or grid search
    [default]
- SimpleGraph:
  - add options -s and -n to filter paired-end paths by seed length and edge
    weight, respectively

* Fri Mar 16 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.0.3-1
- This minor release provides bug fixes and improved reliability for both MPI
  assemblies and Bloom filter assemblies on large datasets. In addition, many
  usability improvements have been made to the abyss-samtobreak program for
  misasssembly assessment.
- Overall:
  - Many compiler fixes for GCC >= 6, Boost >= 1.64
  - Read and write GFA 2 assembly graphs with abyss-pe graph=gfa2
  - Support reading CRAM via samtools
- abyss-bloom:
  - New abyss-bloom build -t rolling-hash option, to pre-build input Bloom
    filters for abyss-bloom-dbg
  - Fix incorrect output of abyss-bloom kmers -r (thanks to @notestaff!)
- abyss-bloom-dbg:
  - New -i option to read Bloom filter files built by abyss-bloom build -t
    rolling-hash
  - Improved error branch trimming (reduces number of small output sequences)
  - Fix intermittent segfaults caused by non-null-terminated strings
- abyss-map:
  - Append BX tag to SAM output (Chromium 10x Genomics data)
- ABYSS-P:
  - Increase default number of sparsehash buckets from 200,000,000 =>
    1,000,000,000
  - Benefit: Allows larger datasets to be assembled without time-consuming
    sparsehash resize operations (e.g. H. sapiens)
  - Caveat: Increases minimum memory requirement per CPU core from 89 MB to 358
    MB
- abyss-pe:
  - Parallelize gzip with pigz, if available
  - Report time/memory for each program with zsh, if available
  - Fix: use N instead of n for scaffold stage, when set by user
- abyss-samtobreak:
  - New --alignment-length (-a) option to exclude alignments shorter than a
    given length
  - New --contig-length (-l) option to exclude contigs shorter than a given
    length
  - New --genome-size (-G) option, for contiguity metrics that depend on the
    reference genome size
  - New --mapq (-q) option for minimum MAPQ score
  - New --patch-gaps (-g) option to join alignments separated by small gaps
  - New TSV output format with additional contiguity stats (e.g. L50, NG50)
  - Fix handling of hard-clipped alignments
- abyss-todot:
  - New --add-complements option
- abyss-tofastq:
  - New --bx option to copy BX tag from from SAM/BAM to FASTQ header comment
    (Chromium 10x Genomics data)

* Tue Aug 15 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.0.2-1
- Fix compile errors with gcc-6 and boost-1.62.
