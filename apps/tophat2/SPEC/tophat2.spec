%define samtools_version 0.1.18
%define priority 211
%define dir_exists() (if [ ! -d /opt/biology/%{name}/%{version} ]; then \
  echo "/opt/biology/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		tophat2
Version:	2.1.1
Release:	1%{?dist}
Summary:	A spliced read mapper for RNA-Seq
Group:		Applications/Engineering
License:	Artistic 2.0
URL:		http://tophat.cbcb.umd.edu/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	bowtie2
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description

TopHat is a fast splice junction mapper for RNA-Seq reads. It aligns
RNA-Seq reads to mammalian-sized genomes using the ultra
high-throughput short read aligner Bowtie, and then analyzes the
mapping results to identify splice junctions between exons.

TopHat is a collaborative effort between the University of Maryland
Center for Bioinformatics and Computational Biology and the University
of California, Berkeley Departments of Mathematics and Molecular and
Cell Biology.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/tophat2 tophat2 /opt/biology/%{name}/%{version}/bin/tophat2 %{priority} \
   --slave %{_bindir}/bam2fastx bam2fastx /opt/biology/%{name}/%{version}/bin/bam2fastx \
   --slave %{_bindir}/bam_merge bam_merge /opt/biology/%{name}/%{version}/bin/bam_merge \
   --slave %{_bindir}/bed_to_juncs bed_to_juncs /opt/biology/%{name}/%{version}/bin/bed_to_juncs \
   --slave %{_bindir}/contig_to_chr_coords contig_to_chr_coords /opt/biology/%{name}/%{version}/bin/contig_to_chr_coords \
   --slave %{_bindir}/fix_map_ordering fix_map_ordering /opt/biology/%{name}/%{version}/bin/fix_map_ordering \
   --slave %{_bindir}/gtf_juncs gtf_juncs /opt/biology/%{name}/%{version}/bin/gtf_juncs \
   --slave %{_bindir}/gtf_to_fasta gtf_to_fasta /opt/biology/%{name}/%{version}/bin/gtf_to_fasta \
   --slave %{_bindir}/juncs_db juncs_db /opt/biology/%{name}/%{version}/bin/juncs_db \
   --slave %{_bindir}/long_spanning_reads long_spanning_reads /opt/biology/%{name}/%{version}/bin/long_spanning_reads \
   --slave %{_bindir}/map2gtf map2gtf /opt/biology/%{name}/%{version}/bin/map2gtf \
   --slave %{_bindir}/prep_reads prep_reads /opt/biology/%{name}/%{version}/bin/prep_reads \
   --slave %{_bindir}/sam_juncs sam_juncs /opt/biology/%{name}/%{version}/bin/sam_juncs \
   --slave %{_bindir}/samtools_0.1.18 samtools_0.1.18 /opt/biology/%{name}/%{version}/bin/samtools_0.1.18 \
   --slave %{_bindir}/segment_juncs segment_juncs /opt/biology/%{name}/%{version}/bin/segment_juncs \
   --slave %{_bindir}/sra_to_solid sra_to_solid /opt/biology/%{name}/%{version}/bin/sra_to_solid \
   --slave %{_bindir}/tophat tophat /opt/biology/%{name}/%{version}/bin/tophat \
   --slave %{_bindir}/tophat-fusion-post tophat-fusion-post /opt/biology/%{name}/%{version}/bin/tophat-fusion-post \
   --slave %{_bindir}/tophat_reports tophat_reports /opt/biology/%{name}/%{version}/bin/tophat_reports

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove tophat2 /opt/biology/%{name}/%{version}/bin/tophat2
fi

%files

%changelog
* Wed Jun 28 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.1-1
- Please note that TopHat has entered a low maintenance, low support stage as
  it is now largely superseded by HISAT2 which provides the same core
  functionality (i.e. spliced alignment of RNA-Seq reads), in a more accurate 
  and much more efficient way.
- TopHat can be now built on more recent Linux distributions with newer GNU C++
  (5.x), as the included SeqAn library was finally upgraded to a newer version.
- improved the detection of linker options for the Boost::Thread library which
  prevented the TopHat build from source on some systems.
- incorporated Luca Venturini's code to support large bowtie2 indexes (.bt2l).
- bam2fastx usage message (-h/--help) was updated in order to better document
  the functions of this program which can be used as a standalone utility for
  converting reads from BAM/SAM to FASTQ/FASTA; the -v/--version option was 
  also added to this utility for easier integration in other pipelines.
