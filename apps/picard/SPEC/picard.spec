%define priority 2101
%define dir_exists() (if [ ! -d /opt/biology/%{name}/%{version} ]; then \
  echo "/opt/biology/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		picard
Version:	2.10.1
Release:	1%{?dist}
Summary:	Java utilities to manipulate SAM files

Group:		Applications/Engineering
License:	MIT
URL:		http://picard.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	java >= 1:1.8.0
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description

Picard comprises Java-based command-line utilities that manipulate SAM
files, and a Java API (SAM-JDK) for creating new programs that read
and write SAM files. Both SAM text format and SAM binary (BAM) format
are supported.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/picard picard /opt/biology/%{name}/%{version}/picard %{priority}

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove picard /opt/biology/%{name}/%{version}/picard
fi


%files

%changelog
* Thu Jul 13 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.1-1
- Bug fix
  - Fix RevertSam to SANITIZE output when read group information is missing
    (#856). The tool considers read group (RG) information missing if the SAM
    file header does not have an @RG line, the read does not have an RG tag or 
    the tag's read group is absent from header groups.
  - For deprecated CrosscheckReadGroupFingerprints, fix option
    EXPECT_ALL_READ_GROUPS_TO_MATCH (#860).
- New feature
  - Fingerprinting tools now read a HaplotypeMap object from a VCF (#793).
    Previously, tools could only read a custom-formatted file. The VCF needs to
    have exactly one sample, HET for all the variants, and haplotype block 
    phasing via phased genotypes (0|1, and 1|0) and the PS format field. The 
    AF field is the AlternateAllele frequency, NOT the minor allele frequency, 
    as it is in the HaplotypeDatabase file. For more details on the file 
    formats, see GATK Article#9526.
