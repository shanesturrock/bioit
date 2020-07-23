%define priority 22303
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		picard
Version:	2.23.3
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
* Fri Jul 24 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.23.3-1
- 2.22.7
  - Change default in RevertSam for restoring hard-clips to true (#1509)
  - NP-remove_r_from_argument (#1508)
  - Fix for corrupted CO tag issue (#1461)
- 2.22.8
  - Fixes edge case where soft-cliped portion of a read ends up at a nega…
    (#1513)
  - GatherVcfs and MergeVcfs: add COMMENT= + GatherVcfs SORT (#1480)
- 2.22.9
  - gl-916 add pipeline version to metrics (#1515)
  - Update htsjdk to 2.22.0 (#1518)
- 2.23.0
  - Added GtcCallRate to GtcToVcf, parse it out and report it in
    CollectArraysVariantCallingMetrics. (#1525)
  - Bugfix for IdentifyContamiant + small improvements to Fingerprinting
    (#1496)
  - GtcFile now uses bpm rather than bpm.csv (#1517)
- 2.23.1
  - cleanup and better error messaging (#1529)
- 2.23.2
  - Update to htsjdk 2.23.0 (#1537)
  - Upgrade to Barclay 3.0.0. (#1526)
- 2.23.3
  - Add haplotype map liftover (#1457)
  - Determine arg parser to use. (#1265)
  - Update CREATE_INDEX arg javadoc. (#1547)
  - Update README.md (#1543)
  - Use a mutable list when initializing MergeBamAlignment
    MATCHING_DICTIONARY_TAGS arg. (#1545)
  - New CheckDuplicateMarking CLP (#1507)

* Fri May 15 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.22.6-1
- Hardclip adapter option in MergeBamAlignments (#1484)
- fix CollectSequencingArtifactMetrics so that it doesn't die when encountering
  IUPAC bases (#1506)

* Fri May 01 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.22.4-1
- Have CompareMetrics consider two NaN metrics equal. Added absolute
  difference.

* Fri Apr 24 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.22.3-1
- 2.22.3
  - Fixes CheckIlluminaDirectory problem with cbcl files and skips in the
    READ_STRUCTURE (#1489)
  - Add arguments for inputs and output to the ConvertSequencingArtifactToOxoG
    command (#1492)
  - Fixes LiftoverVCF for indels (again) (#1469)
  - Only requiring that the input VCF be indexed if an INTERVAL is provided
    (#1487)
  - Allow more SD inputs to LiftoverIntervals and BedToIntervalList (#1446)
  - Improvements to CompareMetrics - Now gives fuller description of
    differences in metrics. - Added feature to ignore differences in certain
    metrics. - Added 'fuzzy' metric comparison. - Added ability to output a
    differences file.
- 2.22.2
  - Fixed two problems in CompareGtcFiles (#1486)

* Fri Mar 27 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.22.1-1
- Ported CompareGtcFiles from Picard private repo (#1468)
- Update htsjdk (#1482)

* Fri Mar 06 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.22.0-1
- Modify VcfToAdpc to handle multiple samples. (#1470)
- Update htsjdk to 2.21.2 (#1471)
- Fix non-symmetry bug in FingerprintChecker (#1455)
- Cleaned up javadoc... (#1434)
- Removed plain asserts and replaced them with ValidationUtil function (#1465)
- Fixed a bug where the merging of fingerprints changes the original list of
  fingerprints leading to incorrect results in the self-lod case when using
  Crosscheck without SECOND_INPUT. (#1458)
- Port CombineVcfs from picard private to picard (#1463)

* Fri Feb 21 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.21.9-1
- Port CombineVcfs from picard private to picard (#1463)

* Thu Feb 06 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.21.8-1
- Remove pullapprove configuration and replace it with github branch
  protections. 

* Fri Jan 24 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.21.7-1
- Corrected LiftOverIntervalList documentation

* Fri Jan 17 2020 Shane Sturrock <shane.sturrock@gmail.com> - 2.21.6-1
- 2.21.5
  - CreateVerifyIDIntensityContaminationMetricsFile handle negative LLK
  - Parse Floats from GtcToVcf in VcfToAdpc
  - Compile and test on 11
- 2.21.6
  - Re-add DecimalFormat, but get rid of comma

* Fri Nov 29 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.21.4-1
- CollectRnaSeqMetrics: Made IGNORE_SEQUENCE optional (#1423)
- replaced int with long to avoid integer overflow in large files. (#1427)
- only adding a period if there's not already a period is pathological (#1430)
- Yf collect duplicate metrics (#1424)
- update htsjdk to 2.21.0 (#1422)

* Fri Nov 15 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.21.3-1
- Yf optimize query for independent replicate metrics (#1420)
- Make CheckIlluminaDirectory log if faking files (#1417)
- Modified CollectAlignmentSummaryMetric to collect more metrics (#1374)

* Fri Nov 01 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.21.2-1
- Fix bug in VcfToAdpc Some poor performing sites in VCFs have null normalized
  X or Y intensity. This fixes the code to handle these.
- Speeds up MarkDuplicates on queryname input by using the in memory read-ends
  map. (#1411)
- Document two CLPs
- Update plugin versions for github-pages documentation (#1405)
- Removing a spurious newline from the logging output of ReorderSam (#1403)

* Fri Oct 18 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.21.1-1
- Fixing up tests in MarkDuplicates so that tests with duplex UMIs are handled
  properly. (#1404)
- Make crosscheck take a file->sample map input so that we can crosscheck to a
  un-duplicated vcf. (#1303)
- Improvements to the locus iteration. (#1376)
- Added in a progress meter to CollectSamErrorMetrics.
- Added a flag to enable jumping to loci rather than iterating through all
  variants / loci in order each run.
- Added a test to CollectHsMetrics to harden against future code changes
  (#1386)
- Added a test to CollectHsMetrics to harden against future code changes.
- removed non-working (and unneeded) code in reflectiveCopy
- added some protection against NPE
- cleaned-up some code formatting issues.
- sanitized some sam files.

* Fri Sep 20 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.20.8-1
- Throw exception in MergeBamAlignments if UNMAPPED_BAM has mapped reads
  (#1394)
- Order the MarkDuplicatesMetric file (#1398)
- Remove unnecessary import of com.sun.xml.internal class (#1401)
- Propagate errors from threads and add error logging (#1393)
- Fixes a bug in the determination of the distance to the second nearest
  barcode. (#1395)
- typo (#1392)
- Revert UpdateVcfSequenceDictionary handles stdout logic and repair test

* Fri Sep 13 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.20.7-1
- Initial Move Calculate the detail metric correctly (on a per-genotype basis).
  Add more tests Add test to handle multi-sample VCF Refactor detail->summary
  metrics accumulation. Fix CreateVerifyIDIntensityContaminationMetricsFile to
  handle LLK and LLK0 as doubles. Added new metric, refined naming of others.
  Enhanced multiple sample tests.
- Updating gradle to 5.6 (#1380)
- Updating NIO dependency and fixing a dependency issue (#1391)
- Update to htsjdk 2.20.3 (#1381)
- Extend travis build matrix to separate Barclay tests from legacy tests.
  (#952)
- PO-18867 Catch NaN Percent_Duplication edge case (#1389)

* Fri Aug 23 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.20.6-1
- adding logging to help debug a JVM core-dump (#1387)
- Update instructions for running single tests (#1382)
- ReorderSam was having trouble when new dictionary is larger than old one
  (#1074)
- relaxing requirements for VCFIndex in tools that don't need one (#1295)
- Add levenshtein distance to eibc (#1331)
- Added a MIN_HISTOGRAM_WIDTH to CollectInsertSizeMetrics. (#1368)
- Adds a buffer to the index stream (#1348)
- revert base image change due to issues building on dockerhub (#1371)
- Upgrades to CompareSAMs (for functional equivalence) (#1305)

* Fri Aug 09 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.20.5-1
- Trigger travis with a small commit.
- CreateVerifyIDIntensityContaminationMetricsFile A little program to create a
  standard picard metrics file from the output of VerifyIDIntensity.
- updating htsjdk to 2.20.0 (#1367)
- Remove docker_helper usage in docker script Remove docker-helper.sh itself
  Switch base base image to google managed image
- Yf debug sam collector error (#1362)

* Fri Jul 26 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.20.4-1
- GL-422 Move MergePedIntoVCF into picard (#1356)
- MergeSamFiles from cloud (#1346)
- Change default to not throw exception for a call on a zeroed out assay
  Reverted InfiniumDataFile byteArray <-> Int/Float back to bitwise operations
  for performance reasons (using ByteBuffer was very slow) Added tests
- Fixes several small issues that needed some help (#1316)
- refactored IntervalListTools to use a "map-reduce" paradigm (#1319)
- Add MIN_TARGET_COVERAGE to HsMetrics (#1345)
- Fix travis build badge (#1357)
- VcfToAdpc a tool to generate an adpc.bin file (Illumina genotyping intensity
  data) from a Genotyping Arrays VCF.

* Fri Jul 05 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.20.3-1
- Bugfix: Update default platform for IlluminaBasecallsToSam (#1351)
- Recover from side effects introduced in CollectIndependentReplicatesMetric
  tests. (#1341)
- Adding in some enum constants that are used in existing/old extended manifest
  files. (#1347)
- Yf provide arbtrary inputs to cmm (#1337)
- GtcToVcf a tool to convert Illumina GTC files to VCF format Responded to a
  lot (but not all) comments dont recompute tan Refactored some math Enable
  support for zeroed-out SNPs Generalize AA/AB/BB related fields in VCF Headers
  Reove zcall from GtcToVcf Added test for GtcToVcf.getGenotypes Use BidiMap
  Error out / inform user if reference is not HG19 Use IlluminaStrand for
  Illumina-strand specific fields. Update test to cover all chromosomes used.
- Added whitepaper describing fingerprinting Math (#1247)
- Fixes bug that prevented liftover of spanning deletions. (#1339)
- Removed boilerplate "main" function from picard CLPs. (#1311)
- Trim descriptions to shorten --list display width. (#1259)
- Handle edge cases with no evidence in CrosscheckFingerprints consistently
  (#1323)

* Fri May 31 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.20.2-1
- Improving missing tools.jar error message.

* Fri May 17 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.20.1-1
- Enabled CRAM input into MarkDuplicates. (#1275)
- Make CollectSamErrorMetrics show up in docs (#1326)
- Sort CRAM test that are used with tests that create an index. (#1317)

* Fri May 03 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.20.0-1
- 2.20.0
  - Add fingerprint Metric (not FingerprintingMetric) (#1312)
  - liftovervcf: remove '##reference=...' and set the new one. (#1321)
- 2.19.2
  - GL-143 Move the probe metrics into TargetMetrics and add a test for
    HsMetrics (#1318)
  - liftovervcf without sorting the variants (#1306)
- 2.19.1
  - Fix CollectInsertSizeMetrics temporary file creation. (#1313)
  - update google cloud NIO provider (#1300)
  - GL-143 remove fields defined in base class (#1307)
  - Add ability to crosscheck (and check) fingerprints on CRAMS directly.
    (#1302)
  - Fixes assert statement in UmiAwareMDWMC tester (#1271)
  - Update README.md (#1293)
  - Factor out a SamComparison class from CompareSAMs for reuse. (#913)
  - Update CreateSequenceDictionary.java (#1286)
  - fix a typo (#1296)

* Fri Mar 29 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.19.0-1
- Updating htsjdk to 2.19.0 (#1297)
- Add COUNT_OUTPUT input parameter to IntervalListTools to output count of
  bases/intervals to file

* Fri Mar 22 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.29-1
- Simplify BedToIntervalList by not reimplementing coordinate conversion
  (#1292)
- Removing strange import in gradle.settings (#1291)
- Updated the documentation for SortSam to be clearer in detailing
  Queryname-sort tie-breaking
- Include aligned adapter reads in metrics (#1282)
- Fix "end" tag in inverted variants in liftover VCF. (#1268)
- Yf stratify chimeric (#1269)
- added comment about versioning of the tiebreaking
- catching the tool help output as well
- responding to review comment
- updated the documentation for SortSam where it was somewhat misleading

* Fri Feb 15 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.27-1
- Demultiplex only when read structure has barcodes

* Fri Feb 08 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.26-1
- Added handling for indels within CollectHsMetrics and
  CollectTargetedPcrMetrics.

* Fri Jan 25 2019 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.25-1
- update to htsjdk 2.18.2 (#1267)
- changing ADD_PG_TAG_TO_READ to boolean (#1262)
- Liftover all indels in flipped strand (#1266)
- fixing a subtle bug with keeperOrNull
- Histogram of duplicate set sizes to be reported in the MarkDuplicates metrics
  file (#569)
- Tool to add OA sam tag to reads (#1202)
- optimization A
- Changed the OpticalDuplicateFinder to no longer be order dependant in its
  output.

* Fri Dec 21 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.21-1
- Increment of RIBOSOMAL_BASES logic changed, new test checking PCT_RIB… (#1143)
- Fixes bug so that isTopStrand now deals properly with unmapped reads (#1256)

* Fri Dec 07 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.20-1
- Fixed a NullPointerException in the OpticalDuplicateFinder (#1254)
- Reverts the changes in as_DSDEGP-2574_PF_percent_misreported

* Fri Nov 23 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.17-1
- Fixes off by one error in trimDistribution that causes CollectHsMetrics to
  crash on edge case (#1248)

* Fri Nov 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.16-1
- Adds DUPLEX_UMI argument to UmiAwareMarkDuplicatesWithMateCigar (#1235)
- Fixed bug in MarkDuplicates where it was mismarking which reads were optical
  duplicates when TAGGING_POLICY is set. (#1244)
- Fixed order dependance bug in graphUtils.cluster() algorithm. (#1245)
- Protection against using the wrong sample alias which produces zero L…
  (#1242)
- Use provided sequence dictionary with MergeVcfs. (#1234)
- As dsdegp 2574 pf percent misreported (#1231)
- Add Scatter by IntervalCount (IntervalListTools) (#1208)
- fixing mistake in documentation of RevertSam (#1232)
- Revert "Changed the OpticalDuplicateFinding code to rely on a proper
  clustering algorithm"
- Changed the OpticalDuplicateFinding code to rely on a proper clustering
  algorithm
- Made OpticalDuplicateFinder Serializable (#1230)

* Fri Oct 26 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.15-1
- Add Scatter by IntervalCount (IntervalListTools) (#1208)
- fixing mistake in documentation of RevertSam (#1232)
- Revert "Changed the OpticalDuplicateFinding code to rely on a proper
  clustering algorithm"
- Changed the OpticalDuplicateFinding code to rely on a proper clustering
  algorithm
- Made OpticalDuplicateFinder Serializable (#1230)

* Fri Sep 14 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.14-1
- 2.18.13
  - upgrade to htsjdk 2.16.1 (#1224)
  - now starting from the origin commit
  - Fix output file naming
  - Fix to ValidateSamFile to warn when NM validation occurs without reference
    (#258) (#1220)
  - improves MarkDuplcates documentation, fixes #1087 (#1088)
  - Installation of r-base in Docker Image allows RExecutor to work (#1198)
  - Warning message about upcoming command line syntax transition. (#1204)
  - CreateSequenceDictionary support for alternative names (@SQ-AN) (#1127)
  - Fix GenotypeConcordance bug writing spanning deletion (#1210)
  - The method createTemporaryIndexedVcfFromInput(File, String) was changed
    (#1213)
- 2.18.14
  - DSDEGP-2749: too many tokens exception in download genotypes (#1226)

* Fri Aug 31 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.12-1
- Diagnose missing barcodes in ExtractIlluminaBarcodes instead of throwing NPE.
  (#1212)
- FixVcfHeader can now add missing FILTER header lines. (#1205)
- Yf fix scatter with overflow mode (#1206)
- Added options to IlluminaBasecallsToSam (#1162)

* Fri Jul 27 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.11-1
- 2.18.10
  - Tidy up TileMetricsOutReader a bit. (#1200)
  - MarkDuplicates to accept Query-Grouped (not Sorted) input and a slight
    change in tiebreak order
  - Adding a LIBRARY field to the umi metrics file in
    UmiAwareMarkDuplicatesWithMateCigar (#1193)
  - Adding error in LiftoverVcf if reference dictionary does not exist (Issue
    #1157) (#1189)
  - new CLP: CollectSamErrorMetric (#1180)
  - Merge branch 'epam-ls_bug_collectmultiplemetrics_no_refflat' of
    https://github.com/EpamLifeSciencesTeam/picard into
    epam-ls_bug_collectmultiplemetrics_no_refflat
  - Bug when no refflat file input in CollectMultipleMetrics fixed. New test
    for CollectMultipleMetrics.
- 2.18.11
  - Fix an issue where the google NIO code would try to load even when the NIO
    library wasn't present. (#1201)

* Fri Jul 06 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.9-1
- 2.18.8
  - upgrading htsjdk 2.15.1 -> 2.16.0 (#1184)
- 2.18.9
  - DSDEGP-2516 Make RevertSam resilient to read groups with no reads. (#1191)

* Fri Jun 08 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.7-1
- 2.18.6
  - Bump to Intel GKL version 0.8.5. (#1182)
  - upgrade htsjdk to 2.15.1 (#1181)
  - Fixes intermittent failures in TheoreticalHetSensitivityTests. (#1178)
  - remove non-ascii character
  - Added forgotten (test) class that tests MarkDuplicates on queryname sorted
    input. (#1174)
- 2.18.7
  - pass all tile metrics files to parser and id correct one there

* Fri May 25 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.5-1
- Generalization of Theoretical Het Sensitivity to handle arbitrary all… (#1144)
- Allowing static fields in MergableMetrics to be not annotated (#1173)
- Update htsjdk (#1171)
- Use the awaitThreadPool from new util class (#1169)
- Avoid overflow when computing barcode metrics. (#1167)

* Fri May 04 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.4-1
- DSDEGP-2199 Add new MakeVcfSampleNameMap tool. (#1160)
- Move setting of TMP_DIR prior to inflater/deflater check. This ensures that
  java.io.tmpdir is set (which is used when checking if we have space for using
  the intel deflater/inflater). Currently it will always check system temp dir.
  (#1165)
- Jc fix executor exception handling (#1163)

* Fri Apr 27 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.3-1
- Add arguments and reporting around recovering REF/ALT swapped alleles (#1151)
- Added reverse cycle and base dir lookup for tile metrics. (#1158)
- Allow processing of a single tile. Append tile integer to output filename to
  avoid overwrites by multiple tiles. (#1154)
- Add to gradle build pre-requisites check (#1156)
- Integrate @experimentalfeature and @betafeature tags (#1094)
- Yf fix infinite loop md (#1147)
- Make picardcloud accessible in docker image (#1153)
- Remove sbt & Eclipse files from gradle project (#1137)

* Fri Apr 06 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.2-1
- DSDEGP-2199 Switch to shaded NIO jar used by GATK. (#1152)
- Add test for reading bam data from stdin (#1131)

* Fri Mar 23 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.18.0-1
- Made unpaired reads not fall through to paired read checks (#1133)
- illumina directory return code conforms to posix standards
- CrosscheckFingerprint speedup, extra functionality and NIO enabling (#1086)
- Refactor SamToFastq and add SamToFastqWithTags (#1110)
- Change order of iteration in pickTranscripts for speed. (#1126)
- Add IdentifyContaminant CLP (#1107)

* Fri Mar 02 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.17.11-1
- Fix regex for barcode files in basecalling metrics for novaseq. (#1125)
- Replace individual developer names with dsde-pipelines-developers
- Add .pullapprove.yml file to picard public

* Thu Feb 22 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.17.10-1
- Update htsjdk version to 2.14.3

* Tue Feb 13 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.17.9-1
- 2.17.5
  - Jc base dir fix (#1095)
  - LiftoverVcf was failing on variants that have swapped alleles when the…
    (#1080)
- 2.17.6
  - Fix tile checking to ensure we are checking against a tile based format.
    (#1097)
- 2.17.7
  - Add filter by tag option/functionality to FilterSamReads (#1079)
  - minor formatting requests
  - PR comments!
  - add tests to debug argument change
  - Simple tracking/logging of liftover success by contig
  - set debugging value of FilterSamReads to false so its not on by default
- 2.17.8
  - Update htsjdk version to 2.14.2
- 2.17.9
  - Increase test coverage (#972)

* Tue Jan 23 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.17.4-1
- Update GKL to 0.8.2 (#1077)
- Better error message when dictionaries differ in GatherVcfs. (#862)
- DSDEGP-1936 Fix the DataProvider for HiSeqX so that we no longer have to
  create symlinks for the .locs file. (#1066)
- added a more informative error when having problem reading a file from
  IntervalListTools (#1078)
- Add reject output to liftover intervals (#1068)
- Allow command line option to suppress LiftOver logging of every failed
  interval (#1067)
- FilterSamReads has a bug and can't filter read by read name. (#1055)

* Wed Jan 10 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.17.3-1
- update htsjdk version to 2.14.0
- Added missing validation for SECOND_INPUT that was causing errors.

* Tue Jan 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 2.17.2-1
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
