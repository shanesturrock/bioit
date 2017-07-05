%define priority 210
%define dir_exists() (if [ ! -d /opt/biology/%{name}/%{version} ]; then \
  echo "/opt/biology/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		hisat2
Version:	2.1.0
Release:	1%{?dist}
Summary:	A fast and sensitive alignment program for mapping NGS reads
Group:		Applications/Bioinformatics
License:	GPL 3.0
URL:		https://ccb.jhu.edu/software/hisat2/index.shtml
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	bowtie2 >= 2.3.2, python >= 2.7.5
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description

HISAT2 is a fast and sensitive alignment program for mapping next-generation
sequencing reads (whole-genome, transcriptome, and exome sequencing data) to a
population of human genomes (as well as to a single reference genome). Based on
an extension of BWT for a graph [1], we designed and implemented a graph FM
index (GFM), an original approach and its first implementation to the best of
our knowledge. In addition to using one global GFM index that represents
general population, HISAT2 uses a large set of small GFM indexes that
collectively cover the whole genome (each index representing a genomic region
of 56 Kbp, with 55,000 indexes needed to cover human population). These small
indexes (called local indexes) combined with several alignment strategies
enable effective alignment of sequencing reads. This new indexing scheme is
called Hierarchical Graph FM index (HGFM). We have developed HISAT2 based on
the HISAT [2] and Bowtie 2 [3] implementations. See the HISAT2 website for more
information.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/hisat2 hisat2 /opt/biology/%{name}/%{version}/bin/hisat2 %{priority} \
   --slave %{_bindir}/extract_exons.py extract_exons.py /opt/biology/%{name}/%{version}/bin/extract_exons.py \
   --slave %{_bindir}/extract_splice_sites.py extract_splice_sites.py /opt/biology/%{name}/%{version}/bin/extract_splice_sites.py \
   --slave %{_bindir}/hisat2-align-l hisat2-align-l /opt/biology/%{name}/%{version}/bin/hisat2-align-l \
   --slave %{_bindir}/hisat2-align-s hisat2-align-s /opt/biology/%{name}/%{version}/bin/hisat2-align-s \
   --slave %{_bindir}/hisat2-build hisat2-build /opt/biology/%{name}/%{version}/bin/hisat2-build \
   --slave %{_bindir}/hisat2-build-l hisat2-build-l /opt/biology/%{name}/%{version}/bin/hisat2-build-l \
   --slave %{_bindir}/hisat2-build-s hisat2-build-s /opt/biology/%{name}/%{version}/bin/hisat2-build-s \
   --slave %{_bindir}/hisat2_extract_exons.py hisat2_extract_exons.py /opt/biology/%{name}/%{version}/bin/hisat2_extract_exons.py \
   --slave %{_bindir}/hisat2_extract_snps_haplotypes_UCSC.py hisat2_extract_snps_haplotypes_UCSC.py /opt/biology/%{name}/%{version}/bin/hisat2_extract_snps_haplotypes_UCSC.py \
   --slave %{_bindir}/hisat2_extract_snps_haplotypes_VCF.py hisat2_extract_snps_haplotypes_VCF.py /opt/biology/%{name}/%{version}/bin/hisat2_extract_snps_haplotypes_VCF.py \
   --slave %{_bindir}/hisat2_extract_splice_sites.py hisat2_extract_splice_sites.py /opt/biology/%{name}/%{version}/bin/hisat2_extract_splice_sites.py \
   --slave %{_bindir}/hisat2-inspect hisat2-inspect /opt/biology/%{name}/%{version}/bin/hisat2-inspect \
   --slave %{_bindir}/hisat2-inspect-l hisat2-inspect-l /opt/biology/%{name}/%{version}/bin/hisat2-inspect-l \
   --slave %{_bindir}/hisat2-inspect-s hisat2-inspect-s /opt/biology/%{name}/%{version}/bin/hisat2-inspect-s \
   --slave %{_bindir}/hisat2_simulate_reads.py hisat2_simulate_reads.py /opt/biology/%{name}/%{version}/bin/hisat2_simulate_reads.py \
   --slave %{_bindir}/hisatgenotype_build_genome.py hisatgenotype_build_genome.py /opt/biology/%{name}/%{version}/bin/hisatgenotype_build_genome.py \
   --slave %{_bindir}/hisatgenotype_extract_reads.py hisatgenotype_extract_reads.py /opt/biology/%{name}/%{version}/bin/hisatgenotype_extract_reads.py \
   --slave %{_bindir}/hisatgenotype_extract_vars.py hisatgenotype_extract_vars.py /opt/biology/%{name}/%{version}/bin/hisatgenotype_extract_vars.py \
   --slave %{_bindir}/hisatgenotype_hla_cyp.py hisatgenotype_hla_cyp.py /opt/biology/%{name}/%{version}/bin/hisatgenotype_hla_cyp.py \
   --slave %{_bindir}/hisatgenotype_locus.py hisatgenotype_locus.py /opt/biology/%{name}/%{version}/bin/hisatgenotype_locus.py \
   --slave %{_bindir}/hisatgenotype.py hisatgenotype.py /opt/biology/%{name}/%{version}/bin/hisatgenotype.py

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove hisat2 /opt/biology/%{name}/%{version}/bin/hisat2
fi

%files

%changelog
* Wed Jun 28 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.1.0-1
- This major version includes the first release of HISAT-genotype, which
  currently performs HLA typing, DNA fingerprinting analysis, and CYP typing on
  whole genome sequencing (WGS) reads. We plan to extend the system so that it
  can analyze not just a few genes, but a whole human genome. Please refer to 
  the HISAT-genotype website for more details.
- HISAT2 can be directly compiled and executed on Windows system using Visual
  Studio, thanks to Nigel Dyer.
- Implemented --new-summary option to output a new style of alignment summary,
  which is easier to parse for programming purposes.
- Implemented --summary-file option to output alignment summary to a file in
  addition to the terminal (e.g. stderr).
- Fixed discrepancy in HISAT2’s alignment summary.
- Implemented --no-templatelen-adjustment option to disable automatic template
  length adjustment for RNA-seq reads.
