%define priority 1180
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		htslib
Version:	1.18
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
   --slave %{_mandir}/man1/bgzip.1 bgzip.1 /opt/bioit/%{name}/%{version}/share/man/man1/bgzip.1 \
   --slave %{_mandir}/man1/htsfile.1 htsfile.1 /opt/bioit/%{name}/%{version}/share/man/man1/htsfile.1 \
   --slave %{_mandir}/man1/tabix.1 tabix.1 /opt/bioit/%{name}/%{version}/share/man/man1/tabix.1 \
   --slave %{_mandir}/man5/faidx.5 faidx.5 /opt/bioit/%{name}/%{version}/share/man/man5/faidx.5 \
   --slave %{_mandir}/man5/sam.5 sam.5 /opt/bioit/%{name}/%{version}/share/man/man5/sam.5 \
   --slave %{_mandir}/man5/vcf.5 vcf.5 /opt/bioit/%{name}/%{version}/share/man/man5/vcf.5 \
   --slave %{_mandir}/man7/htslib-s3-plugin.7 htslib-s3-plugin.7 /opt/bioit/%{name}/%{version}/share/man/man7/htslib-s3-plugin.7

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove htslib /opt/bioit/%{name}/%{version}/bin/htsfile
fi

%files

%changelog
* Wed Jul 26 2023 Shane Sturrock <shane.sturrock@gmail.com> - 1.18-1
- https://github.com/samtools/htslib/releases/tag/1.18

* Wed Feb 22 2023 Shane Sturrock <shane.sturrock@gmail.com> - 1.17-1
- https://github.com/samtools/htslib/releases/tag/1.17

* Tue Aug 23 2022 Shane Sturrock <shane.sturrock@gmail.com> - 1.16-1
- https://github.com/samtools/htslib/releases/tag/1.16

* Thu May 19 2022 Shane Sturrock <shane.sturrock@gmail.com> - 1.15.1-1
- https://github.com/samtools/htslib/releases/tag/1.15.1

* Tue Feb 23 2022 Shane Sturrock <shane.sturrock@gmail.com> - 1.15-1
- https://github.com/samtools/htslib/releases/tag/1.15

* Mon Nov 08 2021 Shane Sturrock <shane.sturrock@gmail.com> - 1.14-1
- https://github.com/samtools/htslib/releases/tag/1.14

* Tue Jul 20 2021 Shane Sturrock <shane.sturrock@gmail.com> - 1.13-1
- 1.12 https://github.com/samtools/htslib/releases/tag/1.12
- 1.13 https://github.com/samtools/htslib/releases/tag/1.13

* Fri Oct 16 2020 Shane Sturrock <shane.sturrock@gmail.com> - 1.11-1
- Features and Updates
  - Support added for remote reference files. fai_path() can take a remote
    reference file and will return the corresponding index file. Remote indexes
    can be handled by refs_load_fai(). UR tags in @SQ lines can now be set to
    remote URIs. (#1017)
  - Added tabix --separate-regions option, which adds header comment lines
    separating different regions' output records when multiple target regions
    are supplied on the command line. (#1108)
  - Added tabix --cache option to set a BGZF block cache size. Most beneficial
    when the -R option is used and the same blocks need to be re-read multiple
    times. (#1053)
  - Improved error checking in tabix and added a --verbosity option so it is
    possible to change the amount of logging when it runs. (#1040)
  - A note about the maximum chromosome length usable with TBI indexes has been
    added to the tabix manual page. Thanks to John Marshall. (#1070)
  - New method vcf_open_mode() changes the opening mode of a variant file based
    on its file extension. Similar to sam_open_mode(). (#1096)
  - The VCF parser has been made faster and easier to maintain. (#1057)
  - bcf_record_check() has been made faster, giving a 15% speed increase when
    reading an uncompressed BCF file. (#1130)
  - The VCF parser now recognises the <NON_REF> symbolic allele produced by
    GATK. (#1045)
  - Support has been added for simultaneous reading of unindexed VCF/BCF files
    when using the synced_bcf_reader interface. Input files must have the
    chromosomes in the same order as each other and be consistent with the
    order of sequences in the header. (#1089)
  - The VCF and BCF readers will now attempt to fix up invalid INFO/END tags
    where the stored END value is less than POS, resulting in an apparently
    negative record length. Such files have been generated by programs which
    used END incorrectly, and by broken lift-over processes that failed to
    update any END tags present. (#1021; fixed samtools/bcftools#1154)
  - The htsFile interface can now detect the crypt4gh encrypted format (see
    https://samtools.github.io/hts-specs/crypt4gh.pdf). If HTSlib is built with
    external plug-in support, and the hfile_crypt4gh plug-in is present, the
    file will be passed to it for decryption. The plug-in can be obtained from
    https://github.com/samtools/htslib-crypt4gh. (#1046)
  - hts_srand48() now seeds the same POSIX-standard sequences of pseudo-random
    numbers regardless of platform, including on OpenBSD where plain srand48()
    produces a different cryptographically-strong non-deterministic sequence.
    Thanks to John Marshall. (#1002)
  - Iterators now work with 64 bit positions. (#1018)
  - Improved the speed of range queries when using BAI indexes by making better
    use of the linear index data included in the file. The best improvement is
    on low-coverage data. (#1031)
  - Alignments which consume no reference bases are now considered to have
    length 1. This would make such alignments cover 1 reference position in the
    same manner as alignments that are unmapped or have no CIGAR strings. These
    alignments can now be returned by iterator-based queries. Thanks to John
    Marshall. (#1063; fixed samtools/samtools#1240, see also
    samtools/hts-specs#521).
  - A bam_set_seqi() function to modify a single base in the BAM structure has
    been added. This is a companion function to bam_seqi(). (#1022)
  - Writing SAM format is around 30% faster. (#1035)
  - Added sam_format_aux1() which converts a BAM aux tag to a SAM format
    string. (#1134)
  - bam_aux_update_str() no longer requires NUL-terminated strings. It is also
    now possible to create tags containing part of a longer string. (#1088)
  - It is now possible to use external plug-ins in language bindings that
    dynamically load HTSlib. Note that a side-effect of this change is that
    some plug-ins now link against libhts.so, which means that they have to be
    able to find the shared library when they are started up. Thanks to John
    Marshall.  (#1072)
  - bgzf_close(), and therefore hts_close(), will now return non-zero when
    closing a BGZF handle on which errors have been detected. (Part of #1117)
  - Added a special case to the kt_fisher_exact() test for when the table
    probability is too small to be represented in a double. This fixes a bug
    where it would, for some inputs, fail to correctly determine which side of
    the distribution the table was on resulting in swapped p-values being
    returned for the left- and right-tailed tests. The two-tailed test value was
    not affected by this problem. (#1126)
  - Improved error diagnostics in the CRAM decoder (#1042), BGZF (#1049), the
    VCF and BCF readers (#1059), and the SAM parser (#1073).
  - ks_resize() now allocates 1.5 times the requested size when it needs to
    expand a kstring instead of rounding up to the next power of two. This has
    been done mainly to make the inlined function smaller, but it also reduces
    the overhead of storing data in kstrings at the expense of possibly needing
    a few more reallocations. (#1129)
- CRAM improvements
  - Delay CRAM crc32 checks until the data actually needs to be used. With
    other changes this leads to a 20x speed up in indexing and other sub-query
    based actions. (#988)
  - CRAM now handles the transition from mapped to unmapped data in a better
    way, improving compression of the unmapped data. (#961)
  - CRAM can now use libdeflate. (#961)
  - Fixed bug in MD tag generation with b read feature codes, causing the
    numbers in the tag to be too large. Note that HTSlib never uses this
    feature code so it is unlikely that this bug would be seen on real data. The
    problem was found when testing against hand-crafted CRAM files. (#1086)
  - Fixed a regression where the CRAM multi-region iterator became much less
    efficient when using threads. It now works more like the single iterator
    and does not preemptively decode the next container unless it will be used.
    (#1061)
  - Set CRAM default quality in lossy quality modes. If lossy quality is
    enabled and B, q or Q features are used, CRAM starts off with QUAL being
    all 255 (as per BAM spec and * quality) and then modifies individual
    qualities as dictated by the specific features. However that then produces
    ASCII quality " " (space, q=-1) for the unmodified bases. Instead ASCII
    quality "?" (q=30) is used, as per HTSJDK. Quality 255 is still used for
    sequences with no modifications at all. (#1094)
- Bug fixes
  - Fixed hfile_libcurl breakage when using libcurl 7.69.1 or later. Thanks to
    John Marshall for tracking down the exact libcurl change that caused the
    incompatibility. (#1105; fixed samtools/samtools#1254 and
    samtools/samtools#1284)
  - Fixed overflows kroundup32() and kroundup_size_t() which caused them to
    return zero when rounding up values where the most significant bit was set.
    When this happens they now return the highest value that can be stored
    (#1044).  All of the kroundup macro definitions have also been gathered
    together into a unified implementation (#1051).
  - Fixed missing return parameter value in idx_test_and_fetch(). Thanks to
    Lilian Janin. (#1014)
  - Fixed crashes due to inconsistent selection between BGZF and plain (hFILE)
    interfaces when reading files. [fuzz] (#1019)
  - Added and/or fixed byte swapping code for big-endian platforms. Thanks to
    Jun Aruga, John Marshall, Michael R Crusoe and Gianfranco Costamagna for
    their help. (#1023; fixed #119 and #355)
  - Fixed a problem with multi-threaded on-the-fly indexes which would
    occasionally write virtual offsets pointing at the end of a BGZF block.
    Attempting to read from such an offset caused EOF to be incorrectly
    reported.  These offsets are now handled correctly, and the indexer has been
    updated to avoid generating them. (#1028; fixed samtools/samtools#1197)
  - In sam_hdr_create(), free newly allocated SN strings when encountering an
    error. [fuzz] (#1034)
  - Prevent double free in case of idx_test_and_fetch() failure. Thanks to
    @fanwayne for the bug report. (#1047; fixed #1033)
  - In the header, link a new PG line only to valid chains. Prevents an
    explosive growth of PG lines on headers where PG lines are already present
    but not linked together correctly. (#1062; fixed samtools/samtools#1235)
  - Also in the header, when calling sam_hdr_update_line(), update target
    arrays only when the name or length is changed. (#1007)
  - Fixed buffer overflows in CRAM MD5 calculation triggered by files with
    invalid compression headers, or files with embedded references that were
    one byte too short. [fuzz] (#1024, #1068)
  - Fix mpileup regression between 1.9 and 1.10 where overlap detection was
    incorrectly skipped on reads where RNEXT, PNEXT and TLEN were set to the
    "unavailable" values ("*", 0, 0 in SAM). (#1097)
  - kputs() now checks for null pointer in source string. [fuzz] (#1087)
  - Fix potential bcf_update_alleles() crash on 0 alleles. Thanks to John
    Marshall. (#994)
  - Added bcf_unpack() calls to some bcf_update functions to fix a bug where
    updates made after a call to bcf_dup() could be lost. (#1032; fixed #1030)
  - Error message typo "Number=R" instead of "Number=G" fixed in
    bcf_remove_allele_set(). Thanks to Ilya Vorontsov. (#1100)
  - Fixed crashes that could occur in BCF files that use IDX= header
    annotations to create a sparse set of CHROM, FILTER or FORMAT indexes, and
    include records that use one of the missing index values. [fuzz] (#1092)
  - Fixed potential integer overflows in the VCF parser and ensured that the
    total length of FORMAT fields cannot go over 2Gbytes. [fuzz] (#1044, #1104)
  - Download index files atomically in idx_test_and_fetch(). This prevents
    corruption when running parallel jobs on S3 files. Thanks to John Marshall.
    (#1112; samtools/samtools#1242).
  - The pileup constructor callback is now given the copy of the bam1_t struct
    made by pileup instead of the original one passed to bam_plp_push(). This
    makes it the same as the one passed to the destructor and ensures that
    cached data, for example the location of an aux tag, will remain valid.
    (#1127)
  - Fixed possible error in code_sort() on negative CRAM Huffman code length.
    (#1008)
  - Fixed possible undefined shift in cram_byte_array_stop_decode_init().
    (#1009)
  - Fixed a bug where range queries to the end of a given reference would
    return incorrect results on CRAM files. (#1016; fixed
    samtools/samtools#1173)
  - Fixed an integer overflow in cram_read_slice(). [fuzz] (#1026)
  - Fixed a memory leak on failure in cram_decode_slice(). [fuzz] (#1054)
  - Fixed a regression which caused cram_transcode_rg() to fail, resulting in a
    crash in "samtools cat" on CRAM files. (#1093; fixed
    samtools/samtools#1276)
  - Fixed an undersized string reallocation in the threaded SAM reader which
    caused it to crash when reading SAM files with very long lines. Numerous
    memory allocation checks have also been added. (#1117)

* Fri Mar 20 2020 Shane Sturrock <shane.sturrock@gmail.com> - 1.10.2-1
- There are many changes in this release, so the executive summary is:
  - Addition of support for references longer than 2Gb (NB: SAM and VCF formats
    only, not their binary counterparts). This may need changes in code using
    HTSlib. See README.large_positions.md for more information.
  - Added a SAM header API.
  - Major speed up to SAM reading and writing. This also now supports
    multi-threading.
  - We can now auto-index on-the-fly while writing a file. This also includes
    to bgzipped SAM.gz.
  - Overhaul of the S3 interface, which now supports version 4 signatures. This
    also makes writing to S3 work.
  - These also required some ABI changes. See below for full details.
- Features / updates
  - A new SAM/BAM/CRAM header API has been added to HTSlib, allowing header
    data to be updated without having to parse or rewrite large parts of the
    header text. See htslib/sam.h for function definitions and documentation.
    (#812)
  - The header typedef and several pre-existing functions have been renamed to
    have a sam_hdr_ prefix: sam_hdr_t, sam_hdr_init(), sam_hdr_destroy(), and
    sam_hdr_dup(). (The existing bam_hdr_-prefixed names are still provided for
    compatibility with existing code.) (#887, thanks to John Marshall)
  - Changes to hfile_s3, which provides support for the AWS S3 API. (#839)
    - hfile_s3 now uses version 4 signatures by default. Attempting to write to
      an S3 bucket will also now work correctly. It is possible to force
    version 2 signatures by creating environment variable HTS_S3_V2 (the exact
    value does not matter, it just has to exist). Note that writing depends on
    features that need version 4 signatures, so forcing version 2 will disable
    writes.
    - hfile_s3 will automatically retry requests where the region endpoint was
      not specified correctly, either by following the 301 redirect (when using
      path-style requests) or reading the 400 response (when using
      virtual-hosted style requests and version 4 signatures). The first region
      to try can be set by using the AWS_DEFAULT_REGION environment variable, by
      setting region in .aws/credentials or by setting bucket_location in
      .s3cfg.
    - hfile_s3 now percent-escapes the path component of s3:// URLs. For
      backwards-compatibility it will ignore any paths that have already been
      escaped (detected by looking for '%' followed by two hexadecimal digits.)
    - New environment variables HTS_S3_V2, HTS_S3_HOST, HTS_S3_S3CFG and
      HTS_S3_PART_SIZE to force version-2 signatures, control the S3 server
      hostname, the configuration file and upload chunk sizes respectively.
  - Numerous SAM format improvements.
    - Bgzipped SAM files can now be indexed and queried. The library now
      recognises sam.gz as a format name to ease this usage. (#718, #916)
    - The SAM reader and writer now supports multi-threading via the
      thread-pool. (#916) Note that the multi-threaded SAM reader does not
      currently support seek operations. Trying to do this (for example with an
      iterator range request) will result in the SAM readers dropping back to
      single-threaded mode.
    - Major speed up of SAM decoding and encoding, by around 2x. (#722)
    - SAM format can now handle 64-bit coordinates and references. This has
      implications for the ABI too (see below). Note BAM and CRAM currently
      cannot handle references longer than 2Gb, however given the speed and
      threading improvements SAM.gz is a viable workaround. (#709)
  - We can now automatically build indices on-the-fly while writing SAM, BAM,
    CRAM, VCF and BCF files. (Note for SAM and VCF this only works when
    bgzipped.) (#718)
  - HTSlib now supports the @SQ-AN header field, which lists alternative names
    for reference sequences. This means given @SQ SN:1 AN:chr1, tools like
    samtools can accept requests for 1 or chr1 equivalently. (#931)
  - Zero-length files are no longer considered to be valid SAM files (with no
    header and no alignments). This has been changed so that pipelines such as
    somecmd | samtools ... with somecmd aborting before outputting anything will
    now propagate the error to the second command. (#721, thanks to John
    Marshall; #261 reported by Adrian Tan)
  - Added support for use of non-standard index names by pasting the data
    filename and index filename with ##idx##. For example
    /path1/my_data.bam##idx##/path2/my_index.csi will open bam file
    /path1/my_data.bam and index file /path2/my_index.csi. (#884) This affects
    hts_idx_load() and hts_open() functions.
  - Improved the region parsing code to handle colons in reference names.
    Strings can be disambiguated by the use of braces, so for example when
    reference sequences called chr1 and chr1:100-200 are both present, the
    regions {chr1}:100-200 and {chr1:100-200} unambiguously indicate which
    reference is being used. (#708) A new function hts_parse_region() has been
    added along with specialisations for sam_parse_region() and
    fai_parse_region().
  - CRAM encoding now has additional checks for MD/NM validity. If they are
    incorrect, it stores the (incorrect copy) verbatim so round-trips "work".
    (#792)
  - Sped up decoding of CRAM by around 10% when the MD tag is being generated.
    (#874)
  - CRAM REF_PATH now supports %Ns (where N is a single digit) expansion in
    http URLs, similar to how it already supported this for directories. (#791)
  - BGZF now permits indexing and seeking using virtual offsets in completely
    uncompressed streams. (#904, thanks to Adam Novak)
  - bgzip now asks for extra confirmation before decompressing files that don't
    have a known compression extension (e.g. .gz). This avoids bgzip -d
    foo.bam.bai producing a foo.bam file that is very much not a BAM-formatted
    file. (#927, thanks to John Marshall)
  - The htsfile utility can now copy files (including to/from URLs using
    HTSlib's remote access facilities) with the --copy option, in addition to
    its existing uses of identifying file formats and displaying sequence or
    variant data. (#756, thanks to John Marshall)
  - Added tabix --min-shift option. (#752, thanks to Garrett Stevens)
  - Tabix now has an -D option to disable storing a local copy of a remote
    index. (#870)
  - Improved support for MSYS Windows compiler environment. (#966)
  - External htslib plugins are now supported on Windows. (#966)
- API additions and improvements
  - New API functions bam_set_mempolicy() and bam_get_mempolicy() have been
    added. These allow more control over the ownership of bam1_t alignment
    record data; see documentation in htslib/sam.h for more information. (#922)
  - Added more HTS_RESULT_USED checks, this time for VCF I/O. (#805)
  - khash can now hash kstrings. This makes it easier to hash
    non-NUL-terminated strings. (#713)
  - New haddextension() filename extension API function. (#788, thanks to John
    Marshall)
  - New hts_resize() macro, designed to replace uses of hts_expand() and
    hts_expand0(). (#805)
  - Added way of cleaning up unused jobs in the thread pool via the new
    hts_tpool_dispatch3() function. (#830)
  - New API functions hts_reglist_create() and sam_itr_regarray() are added to
    create hts_reglist_t region lists from chr:<from>-<to> type region
    specifiers. (#836)
  - Ksort has been improved to facilitate library use. See KSORT_INIT2 (adds
    scope / namespace capabilities) and KSORT_INIT_STATIC interfaces. (#851,
    thanks to John Marshall)
  - New kstring functions (#879)
  - New API functions hts_idx_load3(), sam_index_load3(), tbx_index_load3() and
    bcf_index_load3() have been added. These allow control of whether remote
    indexes should be cached locally, and allow the error message printed when
    the index does not exist to be suppressed. (#870)
  - Improved hts_detect_format() so it no longer assumes all text is SAM unless
    positively identified otherwise. It also makes a stab at detecting bzip2
    format and identifying BED, FASTA and FASTQ files. (#721, thanks to John
    Marshall; #200, #719 both reported by Torsten Seemann)
  - File format errors now set errno to EFTYPE (BSD, MacOS) when available
    instead of ENOEXEC. (#721)
  - New API function bam_set_qname() (#942)
  - In addition to the existing hts_version() function, which reflects the
    HTSlib version being used at runtime, htslib/hts.h now also provides
    HTS_VERSION, a preprocessor macro reflecting the HTSlib version that a
    program is being compiled against. (#951, thanks to John Marshall; #794)
- ABI changes
  - This release contains a number of things which change the Application
    Binary Interface (ABI). This means code compiled against an earlier library
    will require recompiling. The shared library so version has been bumped.
  - On systems that support it, the default symbol visibility has been changed
    to hidden and the only exported symbols are ones that form part of the
    officially supported ABI. This is to make clear exactly which symbols are
    considered parts of the library interface. It also helps packagers who want
    to check compatibility between HTSlib versions. (#946; see for example
    issues #311, #616, and #695)
  - HTSlib now supports 64 bit reference positions. This means several
    structures, function parameters, and return values have been made bigger to
    allow larger values to be stored. While most code that uses HTSlib
    interfaces should still build after this change, some alterations may be
    needed - notably to printf() formats where the values of structure members
    are being printed.  (#709)
  - Due to file format limitations, large positions are only supported when
    reading and writing SAM and VCF files.
  - See README.large_positions.md for more information.
  - An extra field has been added to the kbitset_t struct so bitsets can be
    made smaller (and later enlarged) without involving memory allocation.
    (#710, thanks to John Marshall)
  - A new field has been added to the bam_pileup1_t structure to keep track of
    which CIGAR operator is being processed. This is used by a new
    bam_plp_insertion() function which can be used to return the sequence of any
    inserted bases at a given pileup location. If the alignment includes CIGAR P
    operators, the returned sequence will include pads. (#699)
  - The hts_itr_t and hts_itr_multi_t structures have been merged and can be
    used interchangeably. Extra fields have been added to hts_itr_t to support
    this. hts_itr_multi_t is now a typedef for hts_itr_t; sam_itr_multi_next()
    is now an alias for sam_itr_next() and hts_itr_multi_destroy() is an alias
    for hts_itr_destroy(). (#836)
  - An improved regidx interface has been added. To allow this, struct reg_t
    has been removed, regitr_t has been modified and various new API functions
    have been added to htslib/regidx.h. While parts of the old regidx API have
    been retained for backwards compatibility, it is recommended that all code
    using regidx should be changed to use the new interface. (#761)
  - Elements in the hts_reglist_t structure have been reordered slightly so
    that they pack together better. (#761)
  - bgzf_utell() and bgzf_useek() now use type off_t instead of long for the
    offset. This allows them to work correctly on files longer than 2G bytes on
    Windows and 32-bit Linux. (#868)
  - A number of functions that used to return void now return int so that they
    can report problems like memory allocation failures. Callers should take
    care to check the return values from these functions. (#834)
  - bcf_set_variant_type() now outputs VCF_OVERLAP for spanning deletions
    (ALT=*). (#726)
  - A new field (hrecs) has been added to the bam_hdr_t structure for use by
    the new header API. The l_text field has been changed from uint32_t to
    size_t, to allow for very large headers in SAM files. The text and l_text
    fields have been left for backwards compatibility, but should not be
    accessed directly in code that uses the new header API. To access the
    header text, the new functions sam_hdr_length() and sam_hdr_str() should be
    used instead. (#812)
  - The old cigar_tab field is now marked as deprecated; use the new
    bam_cigar_table[] instead. (#891, thanks to John Marshall)
  - The bam1_core_t structure's l_qname and l_extranul fields have been
    rearranged and enlarged; l_qname still includes the extra NULs. (Almost all
    code should use bam_get_qname(), bam_get_cigar(), etc, and has no need to
    use these fields directly.) HTSlib now supports the SAM specification's full
    254 QNAME length again. (#900, thanks to John Marshall; #520)
  - bcf_index_load() no longer tries the '.tbi' suffix when looking for BCF
    index files (.tbi indexes are for text files, not binary BCF). (#870)
  - htsFile has a new state member to support SAM multi-threading. (#916)
  - A new field has been added to the bam1_t structure, and others have been
    rearranged to remove structure holes. (#709; #922)
- Bug fixes
  - Several BGZF format fixes:
    - Support for multi-member gzip files. (#744, thanks to Adam Novak; #742)
    - Fixed error handling code for native gzip formatted files. (64c4927)
    - CRCs checked when threading too (previously only when non-threaded).
      (#745)
    - Made bgzf_useek function work with threads. (#818)
    - Fixed rare threading deadlocks. (#831)
    - Reading of very short files (<28 bytes) that do not contain an EOF block.
      (#910)
  - Fixed some thread pool deadlocks caused by race conditions. (#746, #906)
  - Many additional memory allocation checks in VCF, BCF, SAM and CRAM code.
    This also changes the return type of some functions. See ABI changes above.
    (#920 amongst others)
  - Replace some sam parsing abort() calls with proper errors. (#721, thanks to
    John Marshall; #576)
  - Fixed to permit SAM read names of length 252 to 254 (the maximum specified
    by the SAM specification). (#900, thanks to John Marshall)
  - Fixed mpileup overlap detection heuristic to work with BAMs having long
    CIGARs (more than 65536 operations). (#802)
  - Security fix: CIGAR strings starting with the N operation can no longer
    cause underflow on the bam CIGAR structure. Similarly CIGAR strings that
    are entirely D ops could leak the contents of uninitialised variables.
    (#699)
  - Fixed bug where alignments starting 0M could cause an invalid memory access
    in sam_prob_realn(). (#699)
  - Fixed out of bounds memory access in mpileup when given a reference with
    binary characters (top-bit set). (#808, thanks to John Marshall)
  - Fixed crash in mpileup overlap_push() function. (#882; #852 reported by
    Pierre Lindenbaum)
  - Fixed various potential CRAM memory leaks when recovering from error cases.
  - Fixed CRAM index queries for unmapped reads (#911; samtools/samtools#958
    reported by @acorvelo)
  - Fixed the combination of CRAM embedded references and multiple slices per
    container. This was incorrectly setting the header MD5sum. (No impact on
    default CRAM behaviour.) (b2552fd)
  - Removed unwanted explicit data flushing in CRAM writing, which on some OSes
    caused major slowdowns. (#883)
  - Fixed inefficiencies in CRAM encoding when many small references occur
    within the middle of large chromosomes. Previously it switched into
    multi-ref mode, but not back out of it which caused the read POS field to be
    stored poorly. (#896)
  - Fixed CRAM handling of references when the order of sequences in a supplied
    fasta file differs to the order of the @SQ headers. (#935)
  - Fixed BAM and CRAM multi-threaded decoding when used in conjunction with
    the multi-region iterator. (#830; #577, #822, #926 all reported by Brent
    Pedersen)
  - Removed some unaligned memory accesses in CRAM encoder and undefined
    behaviour in BCF reading (#867, thanks to David Seifert)
  - Repeated calling of bcf_empty() no longer crashes. (#741)
  - Fixed bug where some 8 or 16-bit negative integers were stored using values
    reserved by the BCF specification. These numbers are now promoted to the
    next size up, so -121 to -128 are stored using at least 16 bits, and -32761
    to -32768 are stored using 32 bits. Note that while BCF files affected by
    this bug are technically incorrect, it is still possible to read them. When
    converting to VCF format, HTSlib (and therefore bcftools) will interpret
    the values as intended and write out the correct negative numbers. (#766,
    thanks to John Marshall; samtools/bcftools#874)
  - Allow repeated invocations of bcf_update_info() and bcf_update_format_*()
    functions. (#856, thanks to John Marshall; #813 reported by Steffen Möller)
  - Memory leak removed in knetfile's kftp_parse_url() function. (#759, thanks
    to David Alexander)
  - Fixed various crashes found by libfuzzer (invalid data leading to errors),
    mostly but not exclusively in CRAM, VCF and BCF decoding. (#805)
  - Improved robustness of BAI and CSI index creation and loading. (#870; #967)
  - Prevent (invalid) creation of TBI indices for BCF files. (#837;
    samtools/bcftools#707)
  - Better parsing of handling of remote URLs with ?param=val components and
    their interaction with remote index URLs. (#790; #784 reported by Mark
    Ebbert)
  - hts_idx_load() now checks locally for all possible index names before
    attempting to download a remote index. It also checks that the remote file
    it downloads is actually an index before trying to save and use it. (#870;
    samtools/samtools#1045 reported by Albert Vilella)
  - hts_open_format() now honours the compression field, no longer also
    requiring an explicit z in the mode string. Also fixed a 1 byte buffer
    overrun. (#880)
  - Removed duplicate hts_tpool_process_flush() prototype. (#816, reported by
    James S Blachly)
  - Deleted defunct cram_tell() declaration. (66c41e2; #915 reported by Martin
    Morgan)
  - Fixed overly aggressive filename suffix checking in bgzip. (#927, thanks to
    John Marshall; #129, reported by @hguturu)
  - Tabix and bgzip --help output now goes to standard output. (#754, thanks to
    John Marshall)
  - Fixed bgzip index creation when using multiple threads. (#817)
  - Made bgzip -b option honour -I (index filename). (#817)
  - Bgzip -d no longer attempts to unlink(NULL) when decompressing stdin.
    (#718)
- Miscellaneous other changes
  - Integration with Google OSS fuzzing for automatic detection of more bugs.
    (Thanks to Google for their assistance and the bugs it has found.) (#796,
    thanks to Markus Kusano)
  - aclocal.m4 now has the pkg-config macros. (6ec3b94; #733 reported by Thomas
    Hickman)
  - Improved C++ compatibility of some header files. (#772; #771 reported by
    @cwrussell)
  - Improved strict C99 compatibility. (#860, thanks to John Marshall)
  - Travis and AppVeyor improvements to aid testing. (#747; #773 thanks to
    Lennard Berger; #781; #809; #804; #860; #909)
  - Various minor compiler warnings fixed. (#708; #765; #846, #860, thanks to
    John Marshall; #865; #966; #973)
  - Various new and improved error messages.
  - Documentation updates (mostly in the header files).
  - Even more testing with make check.
  - Corrected many copyright dates. (#979)
  - The default non-configure Makefile now uses libcurl instead of knet, so it
    can support https. (#895)

* Fri Jul 20 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.9-1
- If ./configure fails, make will stop working until either configure is re-run
  successfully, or make distclean is used. This makes configuration failures
  more obvious. (#711, thanks to John Marshall)
- The default SAM version has been changed to 1.6. This is in line with the
  latest version specification and indicates that HTSlib supports the CG tag
  used to store long CIGAR data in BAM format.
- bgzip integrity check option '--test' (#682, thanks to @sd4B75bJ, @jrayner)
- Faidx can now index fastq files as well as fasta. The fastq index adds an
  extra column to the .fai index which gives the offset to the quality values.
  New interfaces have been added to htslib/faidx.h to read the fastq index and
  retrieve the quality values. It is possible to open a fastq index as if fasta
  (only sequences will be returned), but not the other way round. (#701)
- New API interfaces to add or update integer, float and array aux tags. (#694)
- Add level=<number> option to hts_set_opt() to allow the compression level to
  be set. Setting level=0 enables uncompressed output. (#715)
- Improved bgzip error reporting.
- Better error reporting when CRAM reference files can't be opened. (#706)
- Fixes to make tests work properly on Windows/MinGW - mainly to handle line
  ending differences. (#716)
- Efficiency improvements:
  - Small speed-up for CRAM indexing.
  - Reduce the number of unnecessary wake-ups in the thread pool. (#703)
  - Avoid some memory copies when writing data, notably for uncompressed BGZF
    output. (#703)
- Bug fixes:
  - Fix multi-region iterator bugs on CRAM files. (#684)
  - Fixed multi-region iterator bug that caused some reads to be skipped
    incorrectly when reading BAM files. (#687)
  - Fixed synced_bcf_reader() bug when reading contigs multiple times. (#691,
    reported by @freeseek)
  - Fixed bug where bcf_hdr_set_samples() did not update the sample dictionary
    when removing samples. (#692, reported by @freeseek)
  - Fixed bug where the VCF record ref length was calculated incorrectly if an
    INFO END tag was present. (71b00a)
  - Fixed warnings found when compiling with gcc 8.1.0. (#700)
  - sam_hdr_read() and sam_hdr_write() will now return an error code if passed
    a NULL file pointer, instead of crashing.
  - Fixed possible negative array look-up in sam_parse1() that somehow escaped
    previous fuzz testing. (#731, reported by @fCorleone)
  - Fixed bug where cram range queries could incorrectly report an error when
    using multiple threads. (#734, reported by Brent Pedersen)
  - Fixed very rare rANS normalisation bug that could cause an assertion
    failure when writing CRAM files. (#739, reported by @carsonhh)

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

