%define priority 21703
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		picard
Version:	2.17.3
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
Obsoletes:	picard-2.14.0
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
* Wed Jan 10 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.17.3-1
- update htsjdk version to 2.14.0
- Added missing validation for SECOND_INPUT that was causing errors.

* Tue Jan 09 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.17.2-1
- 2.17.0
  - Adding mode and 95th percentile to InsertSizeMetrics. (#1001)
  - Bug fix: CollectWgsMetricsWithNonZeroCoverage fails to produce a plot
    (#1031)
  - Changes: (#1006)
  - Add additional LiftoverVcf tests (#1011)
  - Enable FilterVcf to filter "sites only" VCFs (#962)
  - Add KEEP_FIRST_DUPLICATE option to RevertSam. (#1029)
  - Update ExtractIlluminaBarcodes.java (#977)
  - incorporate htsjdk 2.13.1 (#1007)
  - Fix up adapter clipping tags after an adapter is selected (#1020)
- 2.17.1
  - Fixes for LiftoverVcf (#1039)
- 2.17.2
  - Yf documentation update 2 (#1028)
  - Remove extra newline in IntervalListTools summary line. (#1054)
  - Upgrade to Barclay 2.0.0. (#1053)
  - Documentation update for several command-line tools (#1021)
  - Yf documentation update 3 (#1045)
  - Enhances MergeVcfs documentation (#1012)
  - New program group definitions and tool assignments. (#1043)
  - Only check expected output cycles (#1049)
  - MOAR tests for LiftOverVcf (#1050)
  - Documentation Updates (#1051)
  - responding to comments, adding ViewSam
  - Make TargetMetrics public (#1048)
  - Pull out some of the metrics being fixed in HsMetricsCollector into a
    separate method (#1046)
  - Updating documentation on ValidateSamFile
  - Improving SamToFastq documentation
  - Updating UmiAwareMarkDuplicates
  - Adding comments for UmiAwareMarkDuplicates
  - Adds FastqToSam javadoc documentation
  - Adds javadoc documentation to GatherBamFiles
  - Added Javadoc to BamToBfq, updating Picards's command line help to have the
    same content.
  - Documentation fixes for MergeSamFiles
  - Adds documentation for CollectRawWgsMetrics and CollectTargetedPcrMetrics
  - Adding javadoc to CollectHsMetrics

* Thu Dec 07 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.16.0-1
- Tool to split unmapped SAM/BAM (#964)
- Enable LiftOverVcf to emit a variant when the reference base has changed
  (#971)
- tag for documentation (6) and beta and experimental categorization (3)

* Tue Nov 14 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.15.0-1
- Adds option to validator to skip mate validation (#973)

* Tue Nov 07 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.14.1-1
- LiftoverVcf performance improvements (#947)
- Misc MarkDuplicates refactoring (#965)
- Allele subsetting code was broken when PL was missing. Got bad NPE. (#963)
- Bugfix for UmiAwareMDWMC
- fixes #935 so that RANDOM_SEED=null is a working option.
- Make Transition enum public (#958)

* Tue Oct 31 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.14.0-1
- Add unit test for FIRST_TILE and TILE_LIMIT features. (#914)
- ExtractIlluminaBarcodes throws a NullPointerException in the case of an empty
  lane directory (#948)
- Adds usage statement to UmiAwareMarkDuplicatesWithMateCigar that it shouldn't
  be used with RNAseq or other technologies with long gaps. (#959)
- Converted the tests of @dataproviders to using....a @dataProvider! (#941)
- Make column names in ExtractIlluminaBarcodes public, and use them in the help
  description (#957)
- Fixed H4 tags in README (#954)
- Extending CrossCheckFingerprint to do a serial check. (#949)
- Backport VcfToIntervalList INCLUDE_FILTERED argument from GATK. (#875)

* Wed Oct 04 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.13.2-1
- Prk samtofastq compressed (#942)
- Fixed tests that were removed from CrosscheckReadgroupFingerprints (#870)
- Fixing lift-over (again) WRT genotypes (#930)
- Adds argument to include filtered sites in genotypeconcordance (#898)

* Tue Oct 03 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.13.1-1
- Updated htsjdk version to integrate updates to Snappy
- Add support for KS and FO in AddOrReplaceReadGroups (#925)

* Tue Sep 12 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.12.1-1
- Replaced hard-coded uses of .vcf, .bcf, and .vcf.gz with static variables.
  (Didn't touch the tests or comments though)
- This fixes [this] (#742) bug, where genotype concordance does not properly
  handle the star allele which represents a spanning deletion. (#904)
- update to htsjdk 2.11.0 and fix tests (#918)

* Wed Aug 30 2017 Shane Sturrock <shane.sturrock@gmail.com> - 2.11.0-1
- Extract CommandLineProgram finding/processing code for reuse. (#899)
- This makes CollectSequencingArtifactMetrics faster by reducing the number of
  HashMap.get() functions we call at every base of the traversal. (#912)
- Adding the option to not write out PG tags for MarkDuplicates and
  MergeBamAlignment. Default behavior is kept the same as it was before but you
  can get speed increases if you set them appropriately. (#907)

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
