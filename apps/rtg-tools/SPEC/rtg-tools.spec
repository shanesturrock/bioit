%define priority 3110
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		rtg-tools
Version:	3.11
Release:	1%{?dist}
Summary:	Utilities for accurate VCF comparison and manipulation
Group:		Applications/Engineering
License:	Simplified BSD
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
RTG Tools includes several useful utilities for dealing with VCF files and
sequence data, but probably the most interesting is the vcfeval command which
performs sophisticated comparison of VCF files.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/rtg-tools %{name} /opt/bioit/%{name}/%{version}/rtg %{priority}

%postun
if [ $1 -eq 0 ]
then
  alternatives \
   --remove %{name} /opt/bioit/%{name}/%{version}/rtg-tools
fi

%files

%changelog
* Fri Feb 28 2020 Shane Sturrock <shane.sturrock@gmail.com> - 3.11-1
- This release includes several new features and commands, along with the usual
  assortment of minor features and bug fixes. Several of these result in
  command line arguments or changes to program outputs, so check existing
  scripts for compatibility before upgrading. 
- Larger features of note:
  - A new command, mapp, for mapping protein query sequences against a protein
    database. This command is complementary to the existing translated protein
    search of the mapx command, and usage is very similar.
  - A new command for variant calling tumor samples when no matched normal is
    available. This command, tumoronly, uses a similar bayesian model as the
    existing somatic command (and several of the improvements made during
    development of the tumor-only calling scenario have also been applied to
    the somatic caller). See the user manual for more information.
  - Several improvements to simulation tools, particularly oriented toward the
    simulation of variants within members of a pedigree. Quite substantial
    improvements to speed and memory use have been made, as well as adding the
    ability to utilize genetic map files to choose recombination sites when
    simulating children.
- Detailed changes are listed below by area.  For more information on new
  features, see the RTG Operations Manual which is included within the
  distribution as HTML and PDF.
- Basic Formatting and Mapping
  - mapp: This new command is like mapx but for protein query sequences.
  - map/mapf: Supports --format fastq-interleaved to allow mapping
    directly from paired end interleaved FASTQ files.
  - mapx: The flag --min-dna-read-length has been renamed to
    --min-read-length (the old flag name will still work).
- Variant Calling and Evaluation
  - tumoronly: New command for detection of somatic variants without a
    matched normal sample.
  - all callers: The --Xformat-annotation flag can be used to enable
    output of additional FORMAT annotations ADF, ADR, ADF1, ADF2, ADR1,
    ADR2 containing allelic counts per arm and orientation that can be
    used for strand and arm-specific filtering.
  - vcfeval: Fixed a rare race-condition crash that could occur when using
    --decompose.
  - vcfeval: Added support for the summary metrics to report at
    user-selectable threshold criteria as an alternative to maximized
    F-measure, via the new flags --at-precision and --at-sensitivity.
  - vcfeval/bndeval/cnveval: New flag --no-roc option to skip the creation
    of ROC data output files.
- Variant Processing and Analysis
  - vcfsplit: This new command allows efficient splitting of a large
    multi-sample VCF into individual sample VCFs, as the input VCF is only
    read a single time. See the user manual for more information including
    supported command line options.
  - vcfsubset: The values provided to --keep-sample and --remove-sample
    argument can now be a file, listing one sample name per line.
  - vcfsubset: Significantly faster when subsetting samples from a VCF
    containing many input samples.
  - vcfdecompose/vcfmerge: Smarter handling of Number=R INFO and FORMAT
    attributes during variant alteration.
  - vcfsubset/vcfannotate/vcfmerge: These commands now accept the
    --bed-regions and --region flags to restrict processing to the regions
    of interest.
  - vcfmerge: Fixed missed cases of allele set changes when warning about
    Number=R/A/G incompatibility.
  - vcfmerge: Now has new flags for controlling the merging of multiple
    records at the same position. --no-merge-records disables all merging
    of multiple records at the same position, and --no-merge-alts disables
    merging of multiple records at the same position when the set of ALTs
    changes.
  - vcfmerge: Now supports --no-header to suppress output of the VCF
    header.
  - vcffilter: When filtering structural variant records, now takes the
    end position into account (if present) when applying region-based
    filtering via --include-bed, --include-vcf, --exclude-bed, and
    --exclude-vcf. (Note that --region and --bed-regions should not be
    used, as tabix indices are not aware of SV variant spans)
  - vcffilter: Fixed JavaScript incorrectly interpreting the setting an
    ID, FILTER, or INFO field to the value '0' as clearing the field.
  - vcffilter: JavaScript extensions can now write to stderr via the new
    error() function.
  - vcffilter: JavaScript extensions can set new values for CHROM and POS.
  - vcfdecompose: Improved the handling of AD and related fields when the
    set of ALT alleles changes.
- Other
  - pedsamplesim: Simulation for many samples is now significantly faster
    and much more memory efficient.
  - samplesim/denovosim/childsim: Reduced memory use.
  - childsim: Initial support for employing genetic maps for LD-aware
    crossover point selection. This is enabled by the --genetic-map-dir
    flag, which specifies a directory containing genetic maps. See the
    user manual for more information on the genetic maps feature.
  - simulators: Fixed a bug where a reference sequence name that looked
    like a region specification (e.g. "name:start-end") was inadvertently
    being interpreted as a genomic region, giving unexpected results.
  - many: Updated the version of htsjdk that we use for SAM/BAM/CRAM
    processing, for improved support with newer Java versions.  Note that
    this new htsjdk is more restrictive in the names that can be used for
    reference sequences, so there is a chance that this will produce
    errors when processing old data that does not comply with the new
    naming constraints.
  - sdfsubseq: When outputting a sub-sequence in FASTA/FASTQ format, the
    output sequence name has been changed from "source[start,end]" to
    "source:start-end", to comply with the new htsjdk sequence naming
    restrictions.
  - many: Updated the JRE used in bundled builds to Zulu Community OpenJDK
    8u242.
  - many: VCF header parsing is more lenient in the case where fields are
    declared multiple times.
  - many: Fixed off-by-one error during single region based tabix VCF
    record retrieval where sometimes extra records abutting the requested
    region would be returned.
  - many: VCF output is now VCFv4.2, and along with this several
    commands now use the new Number=R type.

* Fri Jan 25 2019 Shane Sturrock <shane.sturrock@gmail.com> - 3.10.1-1
- This release primarily includes bugfixes and minor improvements:
  - vcfdecompose: Fix a case where extremely long indels could cause an
    exception during call decomposition. This also affected vcfeval when using
    --decompose.
  - demo scripts: Fix the demo script not pausing for the user under newer
    versions of bash.
  - map: Fix an exception that could be triggered during report generation when
    using --all-hits.
  - rocplot: (gui) Fix the status bar metrics not showing when the curve hugs
    an axis.
  - rocplot: Fix a rare exception that would occur during precision/sensitivity
    plotting if the input data file contained redundant initial points.
  - vcveval: Initial support for "partial spanning deletion" notation that
    octopus uses in some calls.
  - vcfmerge: Now allows -f to be a comma-separated list.
  - vcfstats: The percent phased genotypes statistic was incorrectly calculated
    for call sets using partial genotypes (e.g. ".|1")
  - many: VCF header parsing of the INFO/FORMAT Description component was
    incorrectly de-escaping additional backslash sequences, which could result
    in invalid VCF output.
  - readsim: Warn if the user supplied taxonomic distribution make reference to
    unusable taxon ids.

* Fri Nov 09 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.10-1
- Basic Formatting and Mapping
  - petrim: Now outputs read length distribution statistics.
  - petrim: Fixed an incorrect filename extension being used for fragment and
    overlap length distribution output files.
  - map: Now allows the use of both --repeat-freq and --blacklist-threshold at
    the same time.
  - map: Unmapped but placed reads have had minor adjustments made to their
    expected mapping position.  As well as causing changes to BAM annotations,
    this can cause subsequent changes to variant calling annotations (such as
    AVR scores).
  - map: Fix a rare crash that could occur when mapping a male sample. The fix
    for this can similarly have some changes to subsequent variant calling.
  - sammerge: New flag --min-read-length to permit filtering out alignments
    where the read length is below the specified threshold.
  - sammerge: New flag --select-read-group to include only alignments from the
    specified read groups.
  - sammerge: New flag --remove-duplicates to detect and remove duplicate reads
    based on mapping position. This is like the duplicate detection that the
    analysis tools such as variant callers normally perform on the fly.
  - sammerge: Supports --Xforce to allow overwriting existing output files.
  - sdfsubset/sdfsplit: These commands now pass SAM read group information from
    the input SDF to the output SDF.
- Variant Calling
  - variant callers: The GT fields for unphased calls are now in a normalized
    (numerically increasing) format. Previously the choice of allele ordering
    for alleles within a GT field was somewhat arbitrary, giving the impression
    of some significance where there was none.
  - variant callers: Population variants loaded via --population-priors are
    only used to refine complex call regions when the non-reference allele
    fractions for the variant are higher than 1%. Previously the use of a
    population priors source such as gnomAD that includes many rare variants
    could lead to reduced sensitivity.
  - variant callers: Improved the ability to identify candidate local
    haplotypes when jointly calling a large number of samples or where there is
    wide variation in coverage between samples. The effect of this is greater
    sensitivity to rare variants such as singletons and de novo variants.
  - variant callers: Ignore SAM records where the reads have zero length.
  - many: Region based SAM/BAM record retrieval could sometimes skip records in
    the case of a small inter-region gap.
  - segment: The --min-panel-coverage option has been renamed to
    --min-norm-control-coverage (with extended functionality).
  - avrbuild: New flag --annotated that allows supplying positive/negative
    labels via annotations on each VCF record, as an alternative to supplying
    separate positive and negative VCFs. The supported annotation is the same as
    produced by vcfeval --output-mode=annotate format.
  - avrbuild: New flag --bed-regions to only read those training instances that
    overlap the specified regions. This is a convenience method that can be
    used to train on a specific subset of the data.
- Variant Processing and Analysis
  - svdecompose: Fixed a crash caused by records where SVTYPE=INS but where the
    record did not also contain an SVLEN annotation. These records are now
    ignored.
  - vcfdecompose: Fixed a crash on records that did not contain a GT format
    field. This also affected vcfeval when using --decompose. In addition, the
    error reporting for records with invalid GT fields has been improved.
  - many: Clearer error handling for VCF records that are invalid due to extra
    TABs
  - rocplot: Move the legend for precision/sensitivity graphs to the left hand
    side, where it is less likely to obstruct the curves themselves.
  - vcfannotate: Change in matching semantics when annotating with IDs. Now
    uses the span of the record rather than just the start position.
  - many: New derived annotation VAF1 that contains the VAF of the most
    frequent alt allele. Being a single value annotation, it can be easily used
    during AVR model building.
  - vcfmerge: Fix a crash that could occur when trying to merge a record
    containing duplicated alleles.
- Other
  - samplesim: Changed the behaviour when simulating from VCF records without
    an AF annotation. Now these variants are ignored (i.e. never selected for
    use by the sample), previously samplesim would treat all alleles as equally
    likely. The old behaviour is available via new flag --allow-missing-af.
  - childsim: The misleadingly named flag --num-crossovers has been renamed to
    --extra-crossovers.
  - denovosim: Now allows the original and derived sample names to be the same,
    in which case the sample in the output VCF is updated rather than creating
    a new sample column.
  - denovosim: No longer sets the DN flag to "N" for samples not receiving the
    de novo mutation, as in multi-sample simulation scenarios this is not a
    reliable indicator.
  - denovosim: Fix bug when determining if a putative de novo site would
    overlap with pre-existing variants.
  - pedsamplesim: New command that allows simulating several samples in one run
    according to a pedigree. This uses the methods of samplesim, denovosim, and
    childsim to greatly ease the simulation of multiple samples.
  - pedstats: New flag --delimiter that can be used to output sample
    identifiers with an alternative delimiter. For example, use comma as a
    delimiter when directly supplying a sample list to vcfsubset --keep-samples.
  - simulation tools: Most commands now support --Xforce to overwrite existing
    files.
  - simulation tools: Improvements have been made to parameter validation.
  - misc: Updates for compatibility with Java 11. However, for performance
    reasons we recommend using Java 8 for computationally intensive analysis
    such as mapping and variant calling.
  - misc: Update bundled JRE to 1.8.0_181.
  - misc: Improved percentage memory allocation behaviour when total system
    memory can not be determined. Will now fall back to Java default memory
    allocation.

* Fri Jun 01 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.9.1-1
- map: Fix a rare circumstance where mapping using a reference based
  hash blacklist would use significantly more memory than required.
- vcffilter: JavaScript functions can test for the version of RTG they
  are running under (for checking minimum required version for feature
  compatibility) via a call of the form: "checkMinVersion('3.9.2')"
- vcffilter: JavaScript now supports writing of ID, QUAL, and FILTER
  fields. Added function "ensureFilterHeader" that works the same way as
  ensureInfoHeader and ensureFormatHeader for defining new FILTERs.
- coverage: Improve binning when reporting coverage levels for very deep
  (e.g. >10000X) sequencing datasets.
- vcfeval: More graceful handling of a malformed GT in an input VCF.
- many: Fix escaping of description fields when writing VCF header
  lines.

* Fri Mar 23 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.9-1
- Basic Formatting and Mapping
  - format: In addition to minimum and maximum length of input and output
    sequences, now outputs the mean length of the sequences.
  - petrim: This command is now available in RTG Tools.
  - petrim: New flag --mismatch-adjustment allows updating bases within reads
    when non-matching bases are encountered in the overlap.
  - petrim: Output summary and length distribution information.
  - sammerge: New flag --no-header, does what it says on the tin.
  - map/cgmap: Output SAM/BAM records include an XC:A:A attribute for those
    reads unmapped due to no index hits. (The mapping summary.txt output has
    also been altered slightly to account for this)
  - map/cgmap: The HTML output reports include read summary status counts.
  - map: Direct mapping of fastq data containing 0 length sequences could
    result in an exception or incorrect quality data being associated with a
    sequence in the output BAM. This has been fixed.
  - map: Prevent exception when using a SAM/BAM read group without a sample tag
    specified. We now mandate a sample field be present.
- Variant Calling
  - snp: Prevent exception when using a SAM/BAM read group without a sample tag
    specified. We now mandate a sample field be present.
  - family/population: Fix an arithmetic overflow during calculation of  priors
    in Hardy-Weinberg.
  - variant callers: The default representation used for the output of complex
    haplotype calls now breaks these calls into smaller components than
    previously. This behaviour is selectable via an advanced flag:
    --Xtrim-split={none,standard,trim,align}.
  - variant callers: The default AVR model is now illumina-wgs.avr rather than
    illumina-exome.avr.  When processing exome data, we would recommend only
    using the illumina-exome model if you are specifically interested in ranking
    variant calls outside of target regions.
  - somatic: The VAF annotation is produced by default (previously this
    annotation was only produced when using the --min-allelic-fraction /
--min-allelic-count flags)
  - avrbuild: Multi-thread the loading of training VCF files.
  - discord: Various improvements, primarily improving compatibility with third
    party BAM files and to better handle sequencing with smaller average
    fragment lengths.
  - cnvponbuild: A region label column is not required (one can be specified
    with the new flag --label-column-name).
  - cnvponbuild: The name of the input column supplying coverage levels can be
    overridden with the new flag --coverage-column-name.
  - segment: New flag --min-panel-coverage allows specifying a minimum
    normalized coverage threshold applied to the input panel of normals file.
- Variant Processing and Analysis
  - vcffilter: New flags --min-alleles/--max-alleles to filter by number of
    alleles. For example, --min-alleles=2 --max-alleles=2 for biallelic sites
    only.
  - vcffilter: New flag --fail-samples to allow setting the FT FORMAT field of
    samples that fail the filtering criteria.
  - vcffilter: Fix Javascript interpreting the setting an INFO field to the
    value '1' as setting a flag type INFO field.
  - vcffilter/vcfannotate: New flag --add-header to supply extra header lines,
    either as literal lines or read from file.
  - vcfannotate: New flag --annotation to allow adding several computed
    annotations to the VCF records. See the user manual for the list of
    available annotations.
  - vcfsubset: Rather than aborting when trying to process VCFs that do not
    contain header declarations for fields to be manipulated, just warn and
    continue.
  - vcfstats: Improvement in counting of partial calls, and do not issue a
    warning when polyploid calls are encountered. There has been a slight
    change in output format regarding partial calls, so check any scripts that
    may be parsing vcfstats output.
  - vcfmerge: The --preserve-format also applies when two input records contain
    calls for the same sample at the same reference position and span.
  - vcfmerge: The existing flag --add-header now allows lines read from file.
  - vcfmerge: New flag --input-list-file to allow supplying the VCFs to merge
    via a text file.
  - vcfeval: New flag --decompose to allow decomposing VCF files prior to
    evaluation. This permits some degree of partial credit allocation for
    callers that produce longer complex calls rather than breaking calls into 
    small constituents. Warning: When this flag is used, output VCF files will 
    contain decomposed allele representations, but with annotations from the 
    original records, so any annotations that depend on un-decomposed variant
    representations (e.g. allelic depths, GL, etc) may no longer be meaningful.
    Records that have been decomposed contain ORP and ORL locations indicating 
    the position and length of the original variants to allow backtracking 
    through the decomposition.
  - vcfeval: The ROC data files corresponding to variant type subsets (e.g.
    snps and indel specific) now include the additional metrics such as
    sensitivity and precision that were previously present only in the full ROC
    data file. See the user manual for more information about how these metrics 
    are computed for these subsets.
  - vcfeval: Improvements to --ref-overlap in cases where variants can have ref
    bases removed from either side to choose the side that minimizes overlaps
    with other variants.
  - vcfeval: Algorithm adjustment to permit more frequent syncing, helping to
    reduce instances where variants are too complex to evaluate.
  - vcfeval: Support for the '*' ALT allele that indicates a spanning deletion.
  - rocplot: Produce a more informative error message when trying to open the
    GUI when running in a headless environment.
  - rocplot: (GUI) Remember zoom levels independently for ROC and
    Precision/Recall graphs for better behaviour when swapping back and forth.
  - rocplot: (GUI) A secondary crosshair is available by shift-click placement
    which allows displaying the difference in metrics between the two points.
  - rocplot: (GUI) Permit curve interpolation (this can be important for
    precision recall curves with sparse data, since linear interpolation in
    precision/recall space can be misleading).
  - vcfdecompose: New command to decompose complex variants into smaller
    components.
  - svdecompose: New command to break structural variant DUP/INV/DEL events and
    longer sequence-resolved insertions and deletions into constituent break
    ends for evaluation with bndeval.
  - bndeval: New command to compare breakend call sets.  This command provides
    a similar workflow to vcfeval in terms of output files and use of rocplot
    for benchmarking call sets.
- Other
  - pedfilter: New filtering options to select portions of an input pedigree:
    --keep-family allows retaining particular families; --keep-ids allows
    selecting particular individuals from the larger pedigree.
  - aview: New flags --sort-sample and --print-sample.
  - many: The --no-index flag has been removed. This option was of little use
    since index files are almost always generated on the fly rather than as a
    separate pass. The behaviour is currently still available in this release 
    via --Xno-index, but will removed in the future.
  - many: The use of --Xforce to write into an existing directory will now
    remove any pre-existing log file / done file / progress file.
  - many: Colorized command line help. Whether this is enabled is automatically
    determined, but can be disabled using RTG_JAVA_OPTS (either per-command or
    in rtg.cfg) using -Drtg.default-markup=none. See the user manual for more
    information.
  - many: Single region restrictions can now be specified using the syntax
    <chr>:<pos>~<size> to denote the range surrounding <pos> by <size> on each
    side.
  - many: Miscellaneous bugfixes and improvements to error handling.
  - misc: version and crash talkbacks attempt to indicate to the user if a new
    version is available.
  - misc: Update to htsjdk 2.14.3.
  - misc: Update rtg launcher script to accept Java 9. However, for performance
    reasons we recommend using Java 8 for computationally intensive analysis
    such as mapping and variant calling.
  - misc: Update bundled JRE to 1.8.0_161.

* Thu Jan 11 2018 Shane Sturrock <shane.sturrock@gmail.com> - 3.8.4-1
- RTG Core 3.8.4 (2017-09-08)
- This release primarily includes bugfixes and minor improvements:
  - vcfeval: Explicitly warn when the ROC score field does not exist in
    the VCF header, to help in cases where the user has mixed up INFO vs
    FORMAT field names.
  - vcfeval: Fix an exception that could occur when processing VCFs with
    GT ploidy >= 3.
  - format: When formatting FASTA (both DNA and protein), suppress
    warnings about "unexpected symbols" produced by genuine IUPAC
    ambiguity codes.
  - misc: Detect invalid VCF records containing duplicate INFO or FORMAT
    fields.
  - misc: Improved detection of invalid REF/ALT fields in input VCF files,
    allowing clearer exception messages.
  - misc: Fix incorrect detection of network stats capability during local
    run monitoring.
  - misc: Bash command completion now also works if rtg is symlinked as
    rtg-tools or rtg-core, to improve convenience when both are
    installed. (See the bash completion script if you have alternative
    RTG executable names for which you want to enable the completion)
- RTG Core 3.8.3 (2017-08-02)
- This release primarily includes bugfixes and minor improvements:
  - rocplot: (GUI) Improvements to graph zooming, to allow stepping back
    to previous zoom levels as well as fully un-zooming.
  - rocplot: Improve the automatic curve naming heuristic to ignore
    directory name suffixes like "-eval", ".vcfeval" etc, and similar
    prefixes.
  - rocplot: Enable text antialiasing in GUI and PNG output.
  - vcfeval: More graceful handling of input VCFs containing REF values
    that are not valid according to VCF specifications.
  - vcfmerge/vcfeval: Normalize the casing of nucleotides in REF/ALT,
    which permits merging records where the REF/ALT differ in casing.
  - vcffilter: Graceful error handling of a new category of invalid
    javascript expression.
  - vcfsubset: Don't complain when using --keep-filter/--remove-filter
    flags with "PASS" and the VCF header doesn't contain a declaration for
    that filter.
  - misc: Prevent a unit test failure when running on newer versions of
    Ubuntu.
