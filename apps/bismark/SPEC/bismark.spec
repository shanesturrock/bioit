%define priority 223
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bismark
Version:	0.22.3
Release:	1%{?dist}
Summary:	A bisulfite read mapper and methylation caller
Group:		Applications/Engineering
License:	GNU GPL v3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description

Bismark is a program to map bisulfite treated sequencing reads to a genome of
interest and perform methylation calls in a single step. The output can be
easily imported into a genome viewer, such as SeqMonk, and enables a researcher
to analyse the methylation levels of their samples straight away.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/bismark bismark /opt/bioit/%{name}/%{version}/bismark %{priority} \
   --slave %{_bindir}/bam2nuc bam2nuc /opt/bioit/%{name}/%{version}/bam2nuc \
   --slave %{_bindir}/bismark2bedGraph bismark2bedGraph /opt/bioit/%{name}/%{version}/bismark2bedGraph \
   --slave %{_bindir}/bismark2report bismark2report /opt/bioit/%{name}/%{version}/bismark2report \
   --slave %{_bindir}/bismark2summary bismark2summary /opt/bioit/%{name}/%{version}/bismark2summary \
   --slave %{_bindir}/bismark_genome_preparation bismark_genome_preparation /opt/bioit/%{name}/%{version}/bismark_genome_preparation \
   --slave %{_bindir}/bismark_methylation_extractor bismark_methylation_extractor /opt/bioit/%{name}/%{version}/bismark_methylation_extractor \
   --slave %{_bindir}/coverage2cytosine coverage2cytosine /opt/bioit/%{name}/%{version}/coverage2cytosine \
   --slave %{_bindir}/deduplicate_bismark deduplicate_bismark /opt/bioit/%{name}/%{version}/deduplicate_bismark \
   --slave %{_bindir}/filter_non_conversion filter_non_conversion /opt/bioit/%{name}/%{version}/filter_non_conversion \
   --slave %{_bindir}/methylation_consistency methylation_consistency /opt/bioit/%{name}/%{version}/methylation_consistency \
   --slave %{_bindir}/NOMe_filtering NOMe_filtering /opt/bioit/%{name}/%{version}/NOMe_filtering

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bismark /opt/bioit/%{name}/%{version}/bismark
fi

%files

%changelog
* Fri Jan 24 2020 Shane Sturrock <shane.sturrock@gmail.com> - 0.22.3-1
- 0.22.3
  - Bismark
    - Accepted pull request to fix the MAPQ score calculation in local mode.
  - Methylation_consistency
    - Added a new script to assess the concordance of methylation calls.
- 0.22.2
  - Added FAQ document for questions that keep coming up. Will be populated
    over time.
  - Bismark
    - the option --non_bs_mm is now only allowed in end-to-end mode
    - Fixed the calculation of non bisulfite mismatches for paired-end data
      which happened correctly only when R2 had an InDel
    - When the option -u was used in conjunction with --parallel, only -u
      sequences will be written to the temporary subset files for each spawn of
      Bismark (previously, the entire file was split for --parallel, but then
      only a small subset of those files was used for -u, which resulted in
      very long runs even for a small number of analysed sequences)
  - Deduplicate_bismark
    - the command deduplicate_bismark *bam now works again. Previously the
      output file names were accidentally all derived from the first supplied
      file.
  - Coverage2cytosine
    - Added new option --coverage_threshold INT. Positions have to be covered
      by at least INT calls (irrespective of their methylation state) before
      they get reported. For NOMe-seq, the minimum threshold is automatically
      set to 1 unless specified explicitly. Setting a coverage threshold does
      not work in conjunction with --merge_CpGs (as all genomix CpGs are
      required for this).  Default: 0 (i.e. all genomic positions get reported)
  - Bismark2report
    - added seconds to the timestamp report statement (which caused a warning
      on certain, but not all, platforms)
  - Bismark2summary
    - Now reads splitting reports even for non-deduplicated files (such as
      RRBS).

* Fri May 03 2019 Shane Sturrock <shane.sturrock@gmail.com> - 0.22.1-1
- 0.22.1 Essential Easter Performance Release [EEPR]
  - Bismark
    - Hot-fixed (read: removed) the cause of delay during the MD:Z: field
      computation for reads containing a deletion (which was roughly equal to 1
      second per read). Apologies, I did it again…
    - Changed the default --score_min function for HISAT2 in --local mode back
      to a linear function (instead of using the logarithmic model that is
      employed by Bowtie 2). The default is now --score_min L,0,-0.2 for both
      end-to-end (default) and --local mode. It should be mentioned that we
      currently don't understand how exactly the scoring mode in HISAT2 works
      (even though the scores appear to be all negative with a maximum value 
      of 0), so this might change somewhat in the future.
- 0.22.0 Easter Release - local alignments for single-cell and scNMT-seq
  - Expanding on our observation that single-cell BS-seq, or PBAT libraries in
    general, can generate chimeric read pairs, a recent publication by Wu et
    al. described in further detail that intra-fragment chimeras can hinder the
    efficient alignment of single-cell BS-seq libraries. In there, the authors
    described a pipeline that uses paired-end alignments first, followed by a
    second, single-end alignment step that uses local alignments in a bid to
    improve the mapping of intra-molecular chimeras. To allow this type of
    improvement for single-cell or PBAT libraries, we have been experimenting
    with allowing local alignments.
      Please note that we still do not recommend using local alignments as a
    means to magically increase mapping efficiencies (please see here), but we
    do acknowledge that PBAT/scBSs-seq/scNMT-seq are exceptional applications
    where local alignments might indeed make a difference (there is only so much
    data to be had from a single cell...).
      We didn't have the time yet to set more appropriate or stringent default
    values for local alignments (suggestions welcome), nor did we investigate
    whether the methylation extraction will require an additional --ignore flag
    if a read was found to the be soft-clipped (the so called 'micro-homology
    domains'). This might be added in the near future.
  - Bismark
    - Added support for local alignments by introducing the new option --local.
      This means that the CIGAR operation S (soft-clipping) is now supported
    - fixed typo in option --path_to_bowtie2 (a single missing 2 was preventing
      the specified path to be accepted)
    - fixed typo in option --no-spliced-alignment in HISAT2 mode
    - fixed missing end-of-line character for unmapped or ambiguous FastQ
      sequences in paired-end FastQ mode
    - fixed output file naming in --hisat2 and --parallel mode (_hisat2 was
      missing in --parallel mode). Thanks to @phue for spotting this.
  - Bismark_genome_preparation
    - Added option --large-index to force the generation of LARGE genome
      indexes. This may be required for indexing extremely large genomes (e.g.
      the Axolotl (32 GigaBases)) in --parallel mode. For more information on 
      why the indexing was failing previously see here
  - Bismark_methylation_extractor
    - Now supporting reads containing soft-clipped bases (CIGAR operation S)
  - Bam2nuc
    - Now supporting reads containing soft-clipped bases (CIGAR operation S)
  - Deduplicate_bismark
    - Now supporting reads containing soft-clipped bases (CIGAR operation S)

* Fri Mar 22 2019 Shane Sturrock <shane.sturrock@gmail.com> - 0.21.0-1
- [New]: HISAT2 and SLAM-mode; [Retired]: Bowtie 1
- For the upcoming version Bismark has undergone some substantial changes,
  which sometimes affect more than one module within the Bismark suite. Here is
  a short description of the major changes:
- [Retired]: Bowtie 1 support
  - Bowtie (1) support, and all of its options, has been completely dropped
    from bismark_genome_preparation and bismark. This decision was not made
    lightly, but it seems no one is using the original Bowtie short read aligner
    anymore, even short reads have moved on…
  - Consequently, the option --vanilla and its handling has been removed from a
    number of modules (bismark_genome_preparation, bismark,
    bismark_methylation_extractor and deduplicate_bismark). Too bad, I liked
    that name…
- [Added]: HISAT2 support
  - Instead, the DNA and RNA aligner HISAT2 has been added as a new choice of
    aligner. The reason for this is not necessarily that RNA methylation is now
    a thing, but certain alignment modes (see below) do require splice-aware
    mapping if we don't want to miss out on a whole class of (spliced)
    alignments.  Bowtie 2 is the default mode, HISAT2 alignments can be enabled
    with the option --hisat2
  - Similar to the Bowtie2 mode, alignments with HISAT2 are restricted to
    global (end-to-end) alignments, i.e. soft-clipping is disabled.
    Furthermore, in paired-end mode, the options --no-mixed and --no-discordant
    are permanently enabled, meaning that only properly aligned read pairs are
    put out.
  - As the --hisat2 mode supports spliced alignments, the new CIGAR operation N
    is now supported in all Bismark modules (this includes
    bismark_genome_preparation, bismark, bismark_methylation_extractor,
    deduplicate_bismark and some others).
  - At the time of writing this, the --hisat2 mode appears to be working as
    expected. It should be mentioned however that we have not done a lot of
    testing of these new files, so comments and feedback are welcome.
- SLAM-seq mode
  - We also added a new, experimental and completely different type of
    alignment for SLAM-seq type data (option --slam). This fairly recent method
    to interrogate newly synthesized messenger RNA is akin to bisulfite
    conversion, in that newly synthesized RNA may contain T to C conversions
    following an alkylation reaction (original publication and
    https://www.nature.com/articles/nmeth.4435). The new Bismark alignment mode
    --slam performs T>C conversions of both the genome (in the genome
    preparation step) and the subsequent alignment steps (Bismark alignment
    step).  Currently, the rest of the processing of SLAM-seq data hijacks the
    standard methylation
pipeline:
  - T>C conversions are written out as methylation events in CpG context, while
    T-T matches are scored as unmethylated events in CpG context. Other
    cytosine contexts are not being used.
  - So in a nut-shell: methylation calls in --slam mode are either Ts
    (unmethylated calls = matches at T positions), or T to C mismatches
    (methylated calls = C mismatches at T positions).
  - It should be noted that this is currently an experimental workflow. One
    might argue that T/C conversion aware (or T/C mis-mapping agnostic) mapping
    is currently not necessary for SLAM-seq, NASC-Seq, or scSLAM-seq data as the
    labeling reaction is very inefficient (1 in only 50 to 200 newly
    incorporated Ts is a 4sU, which may get alkylated). This might be true - for
    now. If and when the conversion reaction improves over time, C/T agnostic
    mapping, similar to bisulfite-Seq data, might very well become necessary.
  - Added documentation for NOMe-seq or scNMT-seq processing.
- bismark
  - Dropped support for Bowtie
  - Removed all traces of --vanilla
  - Added support for HISAT2 with option --hisat2.
  - Added HISAT2 option --no-spliced-aligments to disable spliced alignments
    altogether
  - Added HISAT2 option --known-splicesite-infile <path> to provide a list of
    known splice sites.
  - Added option --slam to allow T/C mismatch agnostic mapping (3-letter
    alignment). More here.
  - Added a new option --icpc to truncate read IDs at the first space (or tab)
    it encounters in the (FastQ) read ID, which are sometimes used to add
    comments to a FastQ entry (instead of replacing them with underscores which
    is the default behaviour).
- bismark_genome_preparation
  - Dropped support for Bowtie
  - Added support for HISAT2 with option --hisat2.
  - Added option --slam. Instead of performing an in-silico bisulfite
    conversion, this mode transforms T to C (forward strand), or A to G
    (reverse strand). The folder structure and rest of the indexing process is
    currently exactly the same as for bisulfite sequences, but this might
    change at some point. This means that a genome prepared in --slam mode is
    currently indistinguishable from a true Bisulfite Genome (until the
    alignments are in) so please make sure you name the genome folder
    appropriately to avoid confusion.
- deduplicate_bismark
  - Removed all traces of --vanilla
  - --bam mode is now the default. Uncompressed SAM output may still be
    obtained using the new option --sam
  - Added new option -o/--outfile <basename>. This basename is then modified to
    remove file endings such as .bam, .sam, .txt or .gz, and .deduplicated.bam,
    or .multiple.deduplicated.bam in --multiple mode, is then appended for
    consistency reasons.
  - Added support for new CIGAR operation N
- bismark_methylation_extractor
  - Added support for new CIGAR operation N for all extraction modes
  - Removed all traces of --vanilla
- bismark2summary/bismark2report
  - Adapted to work with Bismark HISAT2 reports instead of Bowtie 1 reports.
- bam2nuc
  - Reads containing spliced reads are now also skipped when determining the
    genomic base composition (as are reads with InDels).

* Fri Feb 08 2019 Shane Sturrock <shane.sturrock@gmail.com> - 0.20.1-1
- This is an early notice that this will be the last release of Bismark that
  supports the use of Bowtie 1. We have added warning statements to both the
  genome preparation and alignment steps to warn users that Bowtie1 is now
  deprecated. All Bowtie 1 functionality and support will disappear in a future
  release. Please shout now if you think this will be a disaster for you...
- bismark
  - Added check to prevent users from inadvertently specifying the very same
    file as both R1 and R2
  - Added a check for file truncation, or more generally the same number of
    reads between R1 and R2 for paired-end FastQ files (directional,
    non-directional and PBAT mode).
  - Added Travis CI testing for most Bismark modules and commands. This should
    help spotting problems a early, e.g. if I release a new version right
    before the Christmas holidays …
  - Changed error message for failed fork command in --parallel mode to [FATAL
    ERROR]: ... to alert users that something isn't working as intended.
- bismark_genome_preparation
  - Added multi-threading to the Bowtie2-based genome preparation (thanks to
    Rahul Karnik)
  - Added test to see whether specified files exist, or die otherwise
- bismark2summary
  - Fixed division by zero errors when a C-context was not covered by any
    reads. This will now use values of 0/0 for the context plots, which looks a
    bit odd, but at least it still works.
  - Detects if (non-deduplicated) RRBS and WGBS samples are mixed together, and
    bails with a meaningful error message.
- bam2nuc
  - Changed samtools to $samtools_path during single-end/paired-end file
    testing.
- bismark_methylation_extractor
  - Changed the order in which --ample_mem and --buffer_size are checked.

* Fri Aug 17 2018 Shane Sturrock <shane.sturrock@gmail.com> - 0.20.0-1
- bismark_methylation_extractor
  - The methylation extractor now creates output directories if they don't
    exist already.
  - The options --ample_mem and --buffer_size <string> are now mutually
    exclusive.
  - Changed the directory being passed on when --cytosine_report is specified
    from parent directory' to 'output directory'.
- bismark2report
  - Major rewrite of bismark2report: HTML file are now rendered using Plotly.js
    [plotly.js v1.39.4] which is completely open source and free to use.
    Highcharts and JQuery were dropped, as was raised here: #177.
  - The files bioinfo.logo, bismark.logo, plot.ly and plotly_template.tpl are
    read in dynamically from a new folder plotly. bismark_sitrep and all its
    contents no longer ship with Bismark. The Bismark HTML reports should be
    completely self-contained, here is an example paired-end Bismark report.
- bismark2summary
  - Major rewrite of bismark2summary: HTML file are now rendered using
    Plotly.js [plotly.js v1.39.4] which is completely open source and free to
    use. Highcharts and JQuery were dropped, as was raised here: #177. The
    files bioinfo.logo, bismark.logo, plot.ly and plotly_template.tpl are read
    in dynamically from a new folder plotly. bismark_sitrep and all its
    contents no longer ship with Bismark. The Bismark HTML Summary reports
    should be completely self-contained.

* Fri Jun 29 2018 Shane Sturrock <shane.sturrock@gmail.com> - 0.19.1-1
- Bismark
  - Child processes are now terminated properly once the mapping and merging
    steps have completed successfully. This means that supplying a
    comma-separated list of input files such as 
      -1 R1.fastq,simulated_1.fastq,ZZZ_R1.fastq \
      -2 R2.fastq,simulated_2.fastq,ZZZ_R2.fastq \
      --multicore 4 
    does no longer spawn a steadily increasing number of Bismark instances.
    issue #138
  - Bismark now also accepts genome FastA files if they are gzip compressed
    (ending in .gz)
- coverage2cytosine
  - Restructured the way output and input file paths are handled. All should be
    working now, including combinations of --gzip, --dir /PATH/, --merge_CpG,
    --disco, --split_by_chromosome etc.
  - The genome folder may now be specified as full or relative path.
  - Now also accepts genome FastA files if they are gzip compressed (ending in
    .gz)
- bam2nuc
  - Now also accepts genome FastA files if they are gzip compressed (ending in
    .gz)
- bismark_genome_preparation
  - Now also accepts genome FastA files if they are gzip compressed (ending in
    .gz)
- deduplicate_bismark
  - Changed the way strands are handled by replacing + and - for a strand
    identity OT,CTOT, CTOB and OB instead. This should avoid conflicts in (the
    extremely rare) occasions where reads with the same starting and end
    positions might have come from both the OT and CTOB strands, or its bottom
    strand equivalent. (see here for more info: issue #161 )
  - Completely removed the code for the --representative mode. People should
    have stopped wanting that anyway.

* Tue Oct 17 2017 Shane Sturrock <shane.sturrock@gmail.com> - 0.19.0-1
- Bismark
  - Changed the methylation call behaviour so that insertions in a read (which
    are filled in with X for the methylation call) are also considered as
    Unknown context for the methylation call. Here is issue #135.
- filter_non_conversion
  - Added new options --percentage_cutoff [int] and --minimum_count [int] to
    allow filtering reads for non-bisulfite conversion using an overall
    methylation percentage and count cutoff. Here is issue #122.
- deduplicate_bismark
  - Added option --multiple to the deduplicator to treat several input SAM/BAM
    files as the same sample. Here is issue #107.
  - Added option --output_dir to deduplicate_bismark so that it can be used in
    the Google cloud. Here is issue #123
- coverage2cytosine
  - Output files are now handled better and more consistently. Default
    processing now produces the following output files (with --gzip):
        CpG_report.txt(.gz) or
        CX_report.txt(.gz)
  - The option --NOMe-Seq now produces four output files (with --gzip):
        NOMe.CpG_report.txt(.gz)
        NOMe.CpG.cov(.gz)
        NOMe.GpC_report.txt(.gz)
        NOMe.GpC.cov(.gz)
  - The option --split_by_chromosome should work in either default, --gc or
    --NOMe-seq mode.
  - NOMe-Seq processing if now ignoring processing that were not covered by any
    reads.
  - Improved handling of the --output_dir, i.e. the folder will be created if
    it doesn't exist already and making the path absolute.
  - Added new option --discordance <int> to allow filtering for discordance pf
    top and bottom strand when in --merge_CpG mode. CpG positions for which
    either the top or bottom strand was not measured at all will not be assessed
    for discordance and hence appear in the regular 'merged_CpG_evidence.cov' 
    file.  More details in issue #91.
  - Fixed context extraction for Gs at positions 1 and 2 of a
    chromosome/contig. Also, last cytosine positions of not covered chromosomes
    are now ignored in the same way as for covered chromosomes issue #127

- copy_files_for_release
  - Is now working from any location.
* Wed Aug 16 2017 Shane Sturrock <shane.sturrock@gmail.com> - 0.18.2-1
- Bismark
  - Changed the timing of when ambiguous within same thread alignments are
    reset. Previously some alignments were incorrectly considered ambiguous
    (see here). This affected Bowtie 2 alignments only.
- bismark2bedGraph
  - The option --ample_mem is now mutually exclusive with specifying memory for
    the UNIX sort command via the option --buffer_size.
