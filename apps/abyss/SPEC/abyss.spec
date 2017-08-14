%define priority 202
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		abyss
Version:	2.0.2
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
   --slave %{_bindir}/abyss-bwasw abyss-bwasw /opt/bioit/%{name}/%{version}/abyss-bwasw \
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
* Tue Aug 15 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.0.2-1
- Fix compile errors with gcc-6 and boost-1.62.
