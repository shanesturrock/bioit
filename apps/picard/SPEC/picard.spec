%define priority 2110
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		picard
Version:	2.10.10
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
   --install %{_bindir}/picard picard /opt/bioit/%{name}/%{version}/picard %{priority}

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove picard /opt/bioit/%{name}/%{version}/picard
fi


%files

%changelog
* Mon Aug 21 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.10-1
- Add documentation creation and update (pushed to gh-pages) (#909)
- Fixed docker build for gradle (#908)
- Remove class (CommandLineProgramGroup) replaced by Barclay parser.
- Add set UQ only option to SetNmMdAndUqTags (#887)

* Wed Aug 09 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.9-1
- Change log4j logging to send all logging to stderr. Added test to assert
  empty stdout.
- Adding the ability to set a maximum size of duplicate sets for checking
  optical dups
- Add regression test for #883. (#894)

* Fri Aug 04 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.7-1
- added config file to supress error message
- Bump GKL version to avoid hanging in AVX support check. (#888)
- Updated the documentation for the reference argument in ScatterIntervalsByNs.
  Also, we now expilictly check for an index and a dict for the reference file.

* Tue Aug 01 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.6-1
- Add a doc note to change VALIDATION_STRINGENCY if validation error
- Add comment per code review suggestion.
- Allow RG tag fields to be unpopulated.
- Made METRICS_FILE optional, which was fairly clearly the original intent.
  (#884)
- Sort availableTiles consistently in all ctors (#878)

* Thu Jul 27 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.5-1
- Revert default compression level to 5.

* Wed Jul 26 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.4-1
- This Picard version contains MAJOR CHANGES TO DEFAULT SETTINGS that impact
  throughput of pipelines.
- New features
  - MAJOR CHANGE: The default compression level is now 1 instead of 5 for
    faster reading (#843). The tradeoff in increased size is paid for by the
    ~3x faster reading.
  - MAJOR CHANGE: Picard now uses the Intel Deflator and Inflator instead of
    JDK for writing and reading compressed data (#843, DSDEGP-454). The Intel
    library is faster in tests than the older JDK library. To disable the Intel
    library and revert to using the JDK library, specify USE_JDK_DEFLATER and
    USE_JDK_INFLATER Boolean arguments.
- Bug fixes
  - Htsjdk versioning is now fixed and cannot be transitive (#843). Previously,
    a dependency could pull in a different version of htsjdk and overwrite the
    build's htsjdk version. Now, the version shown in the build.gradle file is 
    the htsjdk version used by all tools. Currently, Picard uses htsjdk v2.10.1.

* Wed Jul 19 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.3-1
- Add warning to CheckIlluminaDir if we detect cycles without data. (#874)

* Fri Jul 14 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.10.2-1
- yet another reverse-compatibility issue in CrosscheckReadgroupFingerprints
  (#868) 
- fixed bug in Liftover pertaining to indels that straddle two "links…
  (#864)

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
