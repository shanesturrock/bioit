%define priority 0170
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		gvcftools
Version:	0.17.0
Release:	1%{?dist}
Summary:	gVCF file manipulation tools

Group:		Applications/Engineering
License:	Free 
URL:		https://github.com/sequencing/gvcftools
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
gvcftools is a set of utilities to help create and analyze Genome VCF (gVCF)
files. gVCF are VCF 4.1 files which follow a set of conventions for
representing all sites in the genome.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/break_blocks break_blocks /opt/bioit/%{name}/%{version}/bin/break_blocks %{priority} \
   --slave %{_bindir}/check_reference check_reference /opt/bioit/%{name}/%{version}/bin/check_reference \
   --slave %{_bindir}/extract_variants extract_variants /opt/bioit/%{name}/%{version}/bin/extract_variants \
   --slave %{_bindir}/gatk_to_gvcf gatk_to_gvcf /opt/bioit/%{name}/%{version}/bin/gatk_to_gvcf \
   --slave %{_bindir}/getBamAvgChromDepth.pl getBamAvgChromDepth.pl /opt/bioit/%{name}/%{version}/bin/getBamAvgChromDepth.pl \
   --slave %{_bindir}/get_called_regions get_called_regions /opt/bioit/%{name}/%{version}/bin/get_called_regions \
   --slave %{_bindir}/merge_variants merge_variants /opt/bioit/%{name}/%{version}/bin/merge_variants \
   --slave %{_bindir}/remove_region remove_region /opt/bioit/%{name}/%{version}/bin/remove_region \
   --slave %{_bindir}/set_haploid_region set_haploid_region /opt/bioit/%{name}/%{version}/bin/set_haploid_region \
   --slave %{_bindir}/trio trio /opt/bioit/%{name}/%{version}/bin/trio \
   --slave %{_bindir}/twins twins /opt/bioit/%{name}/%{version}/bin/twins

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove break_blocks /opt/bioit/%{name}/%{version}/bin/break_blocks
fi

%files

%changelog
* Thu Feb 04 2021 Shane Sturrock <shane.sturrock@gmail.com> - 0.17.0-1
- add new check_reference tool
- add tty detection for all tools requiring input on stdin
