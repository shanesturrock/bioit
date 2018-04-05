%define priority 18
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		htslib
Version:	1.8
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
* Fri Apr 06 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.8-1
- The URL to get sequences from the EBI reference server has been changed to
  https://. This is because the EBI no longer serve sequences via plain HTTP -
  requests to the http:// endpoint just get redirected. HTSlib needs to be 
  linked against libcurl to download https:// URLs, so CRAM users who want to
  get references from the EBI will need to run configure and ensure libcurl
  support is enabled using the --enable-libcurl option.
- Added libdeflate as a build option for alternative faster compression and
  decompression. Results vary by CPU but compression should be twice as fast
  and decompression faster.
- It is now possible to set the compression level in bgzip. (#675; thanks to
  Nathan Weeks).
- bgzip now gets its own manual page.
- CRAM encoding now stored MD and NM tags verbatim where the reference contains
  'N' characters, to work around ambiguities in the SAM specification (samtools
  #717/762). Also added "store_md" and "store_nm" cram-options for forcing
  these tags to be stored at all locations. This is best when combined with a
  subsequent decode_md=0 option while reading CRAM.
- Multiple CRAM bug fixes, including a fix to free and the subsequent reuse of
  references with -T ref.fa. (#654; reported by Chris Saunders)
- CRAM multi-threading bugs fixed: don't try to call flush on reading;
  processing of multiple range queries; problems with multi-slice containers.
- Fixed crashes caused when decoding some cramtools produced CRAM files.
- Fixed a couple of minor rANS issues with handling invalid data.
- Fixed bug where probaln_glocal() tried to allocate far more memory than
  needed when the query sequence was much longer than the reference. This
  caused crashes in samtools and bcftools mpileup when used on data with very
  long reads. (#572, problem reported by Felix Bemm via minimap2).
- sam_prop_realn() now returns -1 (the same value as for unmapped reads) on
  reads that do not include at least one 'M', 'X' or '=' CIGAR operator, and no
  longer adds BQ or ZQ tags. BAQ adjustments are only made to bases covered by
  these operators so there is no point in trying to align reads that do not have
  them. (#572)

* Thu Feb 01 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.7-1
- BAM: HTSlib now supports BAMs which include CIGARs with more than 65535
  operations as per HTS-Specs 18th November (dab57f4 and 2f915a8).
- BCF/VCF:
  - Removed the need for long double in pileup calculations.
  - Sped up the synced reader in some situations.
  - Bug fixing: removed memory leak in bcf_copy.
- CRAM:
  - Added support for HTS_IDX_START in cram iterators.
  - Easier to build when lzma header files are absent.
  - Bug fixing: a region query with REQUIRED_FIELDS option to disable sequence
    retrieval now gives correct results.
  - Bug fixing: stop queries to regions starting after the last read on a
    chromosome from incorrectly reporting errors (#651, #653; reported by Imran
    Haque and @egafni via pysam).
- Multi-region iterator: The new structure takes a list of regions and iterates
  over all, deduplicating reads in the process, and producing a full list of
  file offset intervals. This is usually much faster than repeatedly using the
  old single-region iterator on a series of regions.
- Curl improvements:
  - Add Bearer token support via HTS_AUTH_LOCATION env (#600).
  - Use CURL_CA_BUNDLE environment variable to override the CA (#622; thanks to
    Garret Kelly & David Alexander).
  - Speed up (removal of excessive waiting) for both http(s) and ftp.
  - Avoid repeatedly reconnecting by removal of unnecessary seeks.
  - Bug fixing: double free when libcurl_open fails.
- BGZF block caching, if enabled, now performs far better (#629; reported by
  Ram Yalamanchili).
- Added an hFILE layer for in-memory I/O buffers (#590; thanks to Thomas
  Hickman).
- Tidied up the drand48 support (intended for systems that do not provide this
  function).

* Tue Oct 03 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.6-1
- Fixed bug where iterators on CRAM files did not propagate error return values
  to the caller correctly. Thanks go to Chris Saunders.
- Overhauled Windows builds. Building with msys2/mingw64 now works correctly
  and passes all tests.
- More improvements to logging output (thanks again to Anders Kaplan).
- Return codes from sam_read1() when reading cram have been made consistent
  with those returned when reading sam/bam. Thanks to Chris Saunders (#575).
- BGZF CRC32 checksums are now always verified.
- It's now possible to set nthreads = 1 for cram files.
- hfile_libcurl has been modified to make it thread-safe. It's also better at
  handling web servers that do not honour byte range requests when attempting
  to seek - it now sets errno to ESPIPE and keeps the existing connection open 
  so callers can revert to streaming mode it they want to.
- hfile_s3 now recalculates access tokens if they have become stale. This fixes
  a reported problem where authentication failed after a file had been in use
  for more than 15 minutes.
- Fixed bug where remote index fetches would fail to notice errors when writing
  files.
- bam_read1() now checks that the query sequence length derived from the CIGAR
  alignment matches the sequence length in the BAM record.

* Wed Jul 05 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.5-1
- Added a new logging API: hts_log(), along with hts_log_error(),
  hts_log_warn() etc. convenience macros. Thanks go to Anders Kaplan for the
  implementation. (#499, #543, #551)
- Added a new file I/O option "block_size" (HTS_OPT_BLOCK_SIZE) to alter the
  hFILE buffer size.
- Fixed various bugs, including compilation issues samtools/bcftools#610,
  samtools/bcftools#611 and robustness to corrupted data #537, #538, #541, #546,
  #548, #549, #554.

