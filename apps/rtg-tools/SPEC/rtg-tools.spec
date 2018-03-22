%define priority 390
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		rtg-tools
Version:	3.9
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
