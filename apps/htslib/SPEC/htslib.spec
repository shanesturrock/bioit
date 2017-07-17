%define priority 15
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		htslib
Version:	1.5
Release:	1%{?dist}
Summary:	C library for high-throughput sequencing data formats

Group:		Applications/Engineering
License:	MIT
URL:		https://github.com/samtools/htslib
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	samtools
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
HTSlib is an implementation of a unified C library for accessing common file
formats, such as SAM, CRAM and VCF, used for high-throughput sequencing data,
and is the core library used by samtools and bcftools. HTSlib only depends on
zlib. It is known to be compatible with gcc, g++ and clang.

HTSlib implements a generalized BAM index, with file extension .csi
(coordinate-sorted index). The HTSlib file reader first looks for the new index
and then for the old if the new index is absent.

This project also includes the popular tabix indexer, which indexes both .tbi
and .csi formats, and the bgzip compression utility.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/htsfile htslib /opt/bioit/%{name}/%{version}/bin/htsfile %{priority} \
   --slave %{_bindir}/tabix tabix /opt/bioit/%{name}/%{version}/bin/tabix \
   --slave %{_bindir}/bgzip bgzip /opt/bioit/%{name}/%{version}/bin/bgzip \
   --slave %{_mandir}/man1/htsfile.1 htsfile.1 /opt/bioit/%{name}/%{version}/share/man/man1/htsfile.1 \
   --slave %{_mandir}/man1/tabix.1 tabix.1 /opt/bioit/%{name}/%{version}/share/man/man1/tabix.1 \
   --slave %{_mandir}/man5/faidx.5 faidx.5 /opt/bioit/%{name}/%{version}/share/man/man5/faidx.5 \
   --slave %{_mandir}/man5/sam.5 sam.5 /opt/bioit/%{name}/%{version}/share/man/man5/sam.5 \
   --slave %{_mandir}/man5/vcf.5 vcf.5 /opt/bioit/%{name}/%{version}/share/man/man5/vcf.5

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove htslib /opt/bioit/%{name}/%{version}/bin/htsfile
fi

%files

%changelog
* Wed Jul 05 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.5-1
- Added a new logging API: hts_log(), along with hts_log_error(),
  hts_log_warn() etc. convenience macros. Thanks go to Anders Kaplan for the
  implementation. (#499, #543, #551)
- Added a new file I/O option "block_size" (HTS_OPT_BLOCK_SIZE) to alter the
  hFILE buffer size.
- Fixed various bugs, including compilation issues samtools/bcftools#610,
  samtools/bcftools#611 and robustness to corrupted data #537, #538, #541, #546,
  #548, #549, #554.

