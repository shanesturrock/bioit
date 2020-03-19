%define priority 1100
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		samtools
Version:	1.10
Release:	1%{?dist}
Summary:	Tools for nucleotide sequence alignments in the SAM format

Group:		Applications/Engineering
License:	MIT
URL:		http://samtools.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	bcftools
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
SAM (Sequence Alignment/Map) is a flexible generic format for storing
nucleotide sequence alignment.
SAM Tools provide various utilities for manipulating alignments in the
SAM format, including sorting, merging, indexing and generating
alignments in a per-position format.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/samtools samtools /opt/bioit/%{name}/%{version}/bin/samtools %{priority} \
   --slave %{_bindir}/ace2sam ace2sam /opt/bioit/%{name}/%{version}/bin/ace2sam \
   --slave %{_bindir}/blast2sam.pl blast2sam.pl /opt/bioit/%{name}/%{version}/bin/blast2sam.pl \
   --slave %{_bindir}/bowtie2sam.pl bowtie2sam.pl /opt/bioit/%{name}/%{version}/bin/bowtie2sam.pl \
   --slave %{_bindir}/export2sam.pl export2sam.pl /opt/bioit/%{name}/%{version}/bin/export2sam.pl \
   --slave %{_bindir}/interpolate_sam.pl interpolate_sam.pl /opt/bioit/%{name}/%{version}/bin/interpolate_sam.pl \
   --slave %{_bindir}/maq2sam-long maq2sam-long /opt/bioit/%{name}/%{version}/bin/maq2sam-long \
   --slave %{_bindir}/maq2sam-short maq2sam-short /opt/bioit/%{name}/%{version}/bin/maq2sam-short \
   --slave %{_bindir}/md5fa md5fa /opt/bioit/%{name}/%{version}/bin/md5fa \
   --slave %{_bindir}/md5sum-lite md5sum-lite /opt/bioit/%{name}/%{version}/bin/md5sum-lite \
   --slave %{_bindir}/novo2sam.pl novo2sam.pl /opt/bioit/%{name}/%{version}/bin/novo2sam.pl \
   --slave %{_bindir}/plot-bamstats plot-bamstats /opt/bioit/%{name}/%{version}/bin/plot-bamstats \
   --slave %{_bindir}/psl2sam.pl psl2sam.pl /opt/bioit/%{name}/%{version}/bin/psl2sam.pl \
   --slave %{_bindir}/sam2vcf.pl sam2vcf.pl /opt/bioit/%{name}/%{version}/bin/sam2vcf.pl \
   --slave %{_bindir}/samtools.pl samtools.pl /opt/bioit/%{name}/%{version}/bin/samtools.pl \
   --slave %{_bindir}/seq_cache_populate.pl seq_cache_populate.pl /opt/bioit/%{name}/%{version}/bin/seq_cache_populate.pl \
   --slave %{_bindir}/soap2sam.pl soap2sam.pl /opt/bioit/%{name}/%{version}/bin/soap2sam.pl \
   --slave %{_bindir}/wgsim wgsim /opt/bioit/%{name}/%{version}/bin/wgsim \
   --slave %{_bindir}/wgsim_eval.pl wgsim_eval.pl /opt/bioit/%{name}/%{version}/bin/wgsim_eval.pl \
   --slave %{_bindir}/zoom2sam.pl zoom2sam.pl /opt/bioit/%{name}/%{version}/bin/zoom2sam.pl \
   --slave %{_mandir}/man1/samtools.1 samtools.1 /opt/bioit/%{name}/%{version}/share/man/man1/samtools.1 \
   --slave %{_mandir}/man1/wgsim.1 wgsim.1 /opt/bioit/%{name}/%{version}/share/man/man1/wgsim.1

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove samtools /opt/bioit/%{name}/%{version}/bin/samtools
fi

%files

%changelog
* Fri Mar 20 2020 Shane Sturrock <shane.sturrock@gmail.com> - 1.10-1
- Changes affecting the whole of samtools, or multiple sub-commands:
  - Samtools now uses the new HTSlib header API. As this adds more checks for
    invalid headers, it is possible that some illegal files will now be
    rejected when they would have been allowed by earlier versions. (#998)
  - Examples of problems that will now be rejected include @SQ lines with no
    SN: tag, and @RG or @PG lines with no ID: tag.
  - samtools sub-commands will now add @PG header lines to output sam/bam/cram
    files. To disable this, use the --no-PG option. (#1087; #1097)
  - samtools now supports alignment records with reference positions greater
    than 2 gigabases. This allows samtools to process alignments for species
    which have large chromosomes, like axolotl and lungfish. Note that due to
    file format limitations, data with large reference positions must use the
    SAM format. (#1107; #1117)
  - Improved the efficiency of reading and writing SAM format data by 2 fold
    (single thread). This is further improved by the ability to use multiple
    threads, as previously done with BAM and CRAM.
  - samtools can now write BGZF-compressed SAM format. To enable this, either
    save files with a .sam.gz suffix, or use --output-fmt sam.gz.
  - samtools can now index BGZF-compressed SAM files.
  - The region parsing code has been improved to handle colons in reference
    names. Strings can be disambiguated by the use of braces, so for example
    when reference sequences called chr1 and chr1:100-200 are both present, the
    regions {chr1}:100-200 and {chr1:100-200} unambiguously indicate which
    reference is being used. (#864)
  - samtools flags, flagstats, idxstats and stats now have aliases flag,
    flagstat, idxstat and stat. (#934)
  - A new global --write-index option has been added. This allows output
    sam.gz/bam/cram files to be indexed while they are being written out. This
    should work with addreplacerg, depad, markdup, merge, sort, split, and view.
    (#1062)
  - A global --verbosity option has been added to enable/disable debugging
    output. (#1124, thanks to John Marshall)
  - It is now possible to have data and index files stored in different
    locations. There are two ways to tell samtools where to find the index:
  - Samtools bedcov, depth, merge, mpileup, stats, tview, and view accept a new
    option (-X). When this is used, each input sam/bam/cram listed on the
    command line should have a corresponding index file. Note that all the data
    files should be listed first, followed by all the index files. (#978,
    thanks to Mingfei Shao) A delimiter ##idx## can be appended to the data file
    name followed by the index file name. This can be used both for input files
    and outputs when indexing on-the-fly.
  - HTSlib (and therefore SAMtools) now uses version 4 signatures by default
    for its s3:// plug-in. It can also write to S3 buckets, as long as version
    4 signatures are in use. See HTSlib's NEWS file and htslib-s3-plugin manual
    page for more information.
  - HTSlib (and therefore SAMtools) no longer considers a zero-length file to
    be a valid SAM file. This has been changed so that pipelines such as
    somecmd | samtools ... with somecmd aborting before outputting anything will
    now propagate the error to the second command.
  - The samtools manual page has been split up into one for each sub-command.
    The main samtools.1 manual page now lists the sub-commands and describes
    the common global options. (#894)
  - The meaning of decode_md, store_md and store_nm in the fmt-option section
    of the samtools.1 man page has been clarified. (#898, thanks to Evan Benn)
  - Fixed numerous memory leaks. (#892)
  - Fixed incorrect macro definition on Windows. (#950)
  - bedcov, phase, misc/ace2sam and misc/wgsim now check for failure to open
    files. (#1013, thanks to Julie Blommaert and John Marshall)
- Changes affecting specific sub-commands:
  - A new "coverage" sub-command has been added. This prints a tabular format
    of the average coverage and percent coverage for each reference sequence,
    as well as number of aligned reads, average mapping quality and base
    quality.  It can also (with the -m option) plot a histogram of coverage
    across the genome. (#992, thanks to Florian Breitwieser)
  - samtools calmd:
    - Reference bases in MD: tags are now converted to upper case. (#981, #988)
      samtools depth:
    - Add new options to write a header to the output (-H) and to direct the
      output to a file (-o). (#937, thanks to Pierre Lindenbaum)
    - New options -g and -G can be used to filter reads. (#953)
    - Fix memory leak when failing to set CRAM options. (#985, thanks to
      Florian Breitwieser)
    - Fix bug when using region filters where the -a option did not work for
      regions with no coverage. (#1113; #1112 reported by Paweł Sztromwasser)
  - samtools fasta and fastq:
    - -1 FILE -2 FILE with the same filename now works properly. (#1042)
    - -o FILE is added as a synonym for -1 FILE -2 FILE. (#1042)
    - The -F option now defaults to 0x900 (SECONDARY,SUPPLEMENTARY). Previously
      secondary and supplementary records were filtered internally in a way
      that could not be turned off. (#1042; #939 reported by @finswimmer)
    - Allow reading from a pipe without an explicit - on the command line.
      (#1042; #874 reported by John Marshall)
    - Turn on multi-threading for bgzf compressed output files. (#908)
    - Fixed bug where the samtools fastq -i would output incorrect information
      in the Casava tags for dual-index reads. It also now prints the tags for
      dual indices in the same way as bcl2fastq, using a + sign between the two
      parts of the index. (#1059; #1047 reported by Denis Loginov)
  - samtools flagstat:
    - Samtools flagstat can now optionally write its output in JSON format or
      as a tab-separated values file. (#1106, thanks to Vivek Rai).
  - samtools markdup:
    - It can optionally tag optical duplicates (reads following Illumina naming
      conventions only). The is enabled with the -d option, which sets the
      distance for duplicates to be considered as optical. (#1091; #1103; #1121;
      #1128; #1134)
    - The report stats (-s) option now outputs counts for optical and
      non-primary (supplementary / secondary) duplicates. It also reports the
      Picard "estimate library size" statistic. A new -f option can be used to
      save the statistics in a given file. (#1091)
    - The rules for calling duplicates can be changed using the new --mode
      option. This mainly changes the position associated with each read in a
      pair. --mode t (the default) is the existing behaviour where the position
      used is that of the outermost template base associated with the read.
      Alternatively --mode s always uses the first unclipped sequence base. In
      practice, this only makes a difference for read pairs where the two reads
      are aligned in the same direction. (#1091)
    - A new -c option can be used to clear any existing duplicate tags. (#1091)
    - A new --include-fails option makes markdup include QC-failed reads.
      (#1091)
    - Fixed buffer overflow in temporary file writer when writing a mixture of
      long and short alignment records. (#911; #909)
  - samtools mpileup:
    - mpileup can now process alignments including CIGAR P (pad) operators
      correctly. They will now also produce the correct output for alignments
      where insertions are immediately followed by deletions, or deletions by
      insertions. Note that due to limitations in HTSlib, they are still unable
      to output sequences that have been inserted before the first aligned base
      of a read. (#847; #842 reported by Tiffany Delhomme. See also htslib
      issue #59 and pull request #699).
    - In samtools mpileup, a deletion or pad on the reverse strand is now
      marked with a different character (#) than the one used on a forward
      strand (*), if the --reverse-del option is used. (#1070)
    - New option --output-extra can be used to add columns for user selected
      alignment fields or aux tags. (#1073)
    - Fixed double-counting of overlapping bases in alignment records with
      deletions or reference skips longer than twice the insert size. (#989;
      #987 reported by @dariomel)
    - Improved manual page with documentation about what each output column
      means. (#1055, thanks to John Marshall)
  - samtools quickcheck:
    - Add unmapped (-u) option, which disables the check for @SQ lines in the
      header. (#920, thanks to Shane McCarthy) samtools reheader:
    - A new option -c allows the input header to be passed to a given command.
      Samtools then takes the output of this command and uses it as the
      replacement header. (#1007)
    - Make it clear in help message that reheader --in-place only works on CRAM
      files. (#921, thanks to Julian Gehring)
    - Refuse to in-place reheader BAM files, instead of unexpectedly writing a
      BAM file to stdout. (#935)
  - samtools split:
    - In samtools split, the -u option no longer accepts an extra file name
      from which a replacement header was read. The two file names were
      separated using a colon, which caused problems on Windows and prevented
      the use of URLs. A new -h option has been added to allow the replacement
      header file to be specified in its own option. (#961)
    - Fixed bug where samtools split would crash if it read a SAM header that
      contained an @RG line with no ID tag. (#954, reported by @blue-bird1)
  - samtools stats:
    - stats will now compute base compositions for BC, CR, OX and RX tags, and
      quality histograms for QT, CY, BZ and QX tags. (#904)
    - New stats FTC and LTC showing total number of nucleotides for first and
      last fragments. (#946)
    - The rules for classifying reads as "first" or "last" fragment have been
      tightened up. (#949)
    - Fixed bug where stats could over-estimate coverage when using the
      target-regions option or when a region was specified on the command-line.
      (#1027; #1025, reported by Miguel Machado; #1029, reported by Jody
      Phelan).
    - Fixed error in stats GCD percentile depth calculation when the depth to
      be reported fell between two bins. It would report the depth entirely
      from the lower bin instead of taking a weighted average of the two.
      (#1048)
    - Better catching and reporting of out of memory conditions. (#984; #982,
      reported by Jukka Matilainen)
    - Improved manual page. (#927)
  - samtools tview:
    - tview can now display alignments including CIGAR P operators, D followed
      by I and I followed by D correctly. See mpileup above for more
      information. (#847; #734, reported by Ryan Lorig-Roach)
    - The "go to position" text entry box has been made wider. (#968, thanks to
      John Marshall)
    - Fixed samtools tview -s option which was not filtering reads correctly.
      It now only shows reads from the requested sample or read group. (#1089)
  - samtools view:
    - New options -d and -D to only output alignments which have a tag with a
      given type and value. (#1001, thanks to Gert Hulselmans)
      misc/plot-bamstats script:
    - Fixed merge (-m) option. (#923, #924 both thanks to Marcus D Sherman)
    - Made the quality heatmap work with gnuplot version 5.2.7 and later.
      (#1068; #1065 reported by Martin Mokrejš)
    - Fixed --do-ref-stats bug where fasta header lines would be counted as
      part of the sequence when the --targets option was used. (#1120, thanks
      to Neil Goodgame)
    - Removed the misc/varfilter.py Python script, as it takes consensus-pileup
      as input, which was removed from samtools in release 0.1.17 in 2011.
      (#1125)

* Fri Jul 20 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.9-1
- Samtools mpileup VCF and BCF output is now deprecated. It is still
  functional, but will warn. Please use bcftools mpileup instead. (#884)
- Samtools mpileup now handles the '-d' max_depth option differently. There is
  no longer an enforced minimum, and '-d 0' is interpreted as limitless (no
  maximum - warning this may be slow). The default per-file depth is now 8000,
  which matches the value mpileup used to use when processing a single sample.
  To get the previous default behaviour use the higher of 8000 divided by the
  number of samples across all input files, or 250. (#859)
- Samtools stats new features:
  - The '--remove-overlaps' option discounts overlapping portions of templates
    when computing coverage and mapped base counting. (#855)
  - When a target file is in use, the number of bases inside the target is
    printed and the percentage of target bases with coverage above a given
    threshold specified by the '--cov-threshold' option. (#855)
  - Split base composition and length statistics by first and last reads.
    (#814, #816)
- Samtools faidx new features:
  - Now takes long options. (#509, thanks to Pierre Lindenbaum)
  - Now warns about zero-length and truncated sequences due to the requested
    range being beyond the end of the sequence. (#834)
  - Gets a new option (--continue) that allows it to carry on when a requested
    sequence was not in the index. (#834)
  - It is now possible to supply the list of regions to output in a text file
    using the new '--region-file' option. (#840)
  - New '-i' option to make faidx return the reverse complement of the regions
    requested. (#878)
  - faidx now works on FASTQ (returning FASTA) and added a new fqidx command to
    index and return FASTQ. (#852)
- Samtools collate now has a fast option '-f' that only operates on primary
  pairs, dropping secondary and supplementary. It tries to write pairs to the
  final output file as soon as both reads have been found. (#818)
- Samtools bedcov gets a new '-j' option to make it ignore deletions (D) and
  reference skips (N) when computing coverage. (#843)
- Small speed up to samtools coordinate sort, by converting it to use radix
  sort. (#835, thanks to Zhuravleva Aleksandra)
- Samtools idxstats now works on SAM and CRAM files, however this isn't fast
  due to some information lacking from indices. (#832)
- Compression levels may now be specified with the level=N output-fmt-option.
  E.g. with -O bam,level=3.
- Various documentation improvements.
- Bug-fixes:
  - Improved error reporting in several places. (#827, #834, #877, cd7197)
  - Various test improvements.
  - Fixed failures in the multi-region iterator (view -M) when regions provided
    via BED files include overlaps (#819, reported by Dave Larson).
  - Samtools stats now counts '=' and 'X' CIGAR operators when counting mapped
    bases. (#855)
  - Samtools stats has fixes for insert size filtering (-m, -i). (#845; #697
    reported by Soumitra Pal)
  - Samtools stats -F now longer negates an earlier -d option. (#830)
  - Fix samtools stats crash when using a target region. (#875, reported by
    John Marshall)
  - Samtools sort now keeps to a single thread when the -@ option is absent.
    Previously it would spawn a writer thread, which could cause the CPU usage
    to go slightly over 100%. (#833, reported by Matthias Bernt)
  - Fixed samtools phase '-A' option which was incorrectly defined to take a
    parameter. (#850; #846 reported by Dianne Velasco)
  - Fixed compilation problems when using C_INCLUDE_PATH. (#870; #817 reported
    by Robert Boissy)
  - Fixed --version when built from a Git repository. (#844, thanks to John
    Marshall)
  - Use noenhanced mode for title in plot-bamstats. Prevents unwanted
    interpretation of characters like underscore in gnuplot version 5. (#829,
    thanks to M. Zapukhlyak)
  - blast2sam.pl now reports perfect match hits (no indels or mismatches).
    (#873, thanks to Nils Homer)
  - Fixed bug in fasta and fastq subcommands where stdout would not be flushed
    correctly if the -0 option was used.
  - Fixed invalid memory access in mpileup and depth on alignment records where
    the sequence is absent.

* Fri Apr 06 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.8-1
- samtools calmd now has a quiet mode. This can be enabled by passing -Q to
  calmd. (Thanks to Colin Davenport)
- In samtools depth -d 0 will effectively remove the depth limit. (#764)
- Improvements made to samtools collate's interface and documentation. It is
  now possible to specify an output file name using -o, instead of deriving it
  from the prefix used for temporary files. The prefix itself is now optional if
  -o or -O (to stdout) is used. (#780)
- Bug-fixes:
  - Make samtools addreplacerg choose output format by file extension. (#767;
    reported by Argy Megalios)
  - Merge tests now work on ungzipped data, allowing tests to be run against
    different deflate libraries.
  - samtools markdup error messages about missing tags have been updated with
    the suggestion that samtools fixmate is run beforehand. (#765; reported by
    Yudong Cai)
  - Enables the --reference option for samtools fastq. Now works like other
    programs when a reference sequence is needed for CRAM files. (#791,
    reported by Milana Kaljevic)

* Tue Feb 13 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.7-1
- HTSlib, and so samtools, now support BAMs which include CIGARs with more than
  65535 operations as per HTS-Specs 18th November (dab57f4 and 2f915a8).
- samtools quickcheck will now write a warning to stderr if it finds any
  problems. These messages can be suppressed with a new -q option.
- samtools markdup can now mark supplementary alignments of reads where the
  primary alignment is found to be a duplicate. Supplementary marking can be
  turned on by passing the -S option to markdup. When this option is enabled, 
  all the alignment data will be written to a temporary file so that 
  supplementary alignments that occur before a duplicated primary can be 
  correctly marked in the final output. The location of this temporary file 
  can be influenced using the new -T option.
- samtools view now supports HTSlib's new multi-region iterator. This can be
  enabled by passing the -M option to view. When using this option:
  - The BED filter (-L option) will use the index to skip through the file
  - Reads from overlapping regions will only be output once
- samtools bedcov will now ignore BED comment and header lines (#571; thanks to
  Daniel Baker).
- samtools collate now updates the @HD SO: and GO: tags, and sort will remove a
  GO: tag if present. (#757; reported by Imran Haque).
- Bug-fixes:
  - maq2sam now checks for input files that end early. (#751; patch supplied by
    Alexandre Rebert of the Mayhem team, via Andreas Tille from Debian.)
  - Fixed incorrect check when looking up header tags that could lead to a
    crash in samtools stats. (#208; thanks to Dave Larson.)
  - Fixed bug in samtools fastq -O option where it would fail if the OQ tag in
    the input file had an unexpected type. (#758; reported by Taejeong Bae)
  - The MD5 calculations in samtools dict and md5fa did not handle
    non-alphabetic characters in the same way as the CRAM MD5 function. They
    have now been updated to match. (#704; reported by Chris Norman).
  - Fix possible infinite loop in samtools targetcut.
  - Building bam_tview_curses should no longer fail if a curses header file
    cannot be found.

* Tue Oct 03 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.6-1
- Added new markdup sub-command and -m option for fixmate. Used together,they
  allow duplicates to be marked and optionally removed. This fixes a number of
  problems with the old rmdup sub-command, for example issue #497. rmdup is kept
  for backwards compatibility but markdup should be used in preference.
- Sort is now much better at keeping within the requested memory limit. It
  should also be slightly faster and need fewer temporary files when the file
  to be sorted does not fit in memory. (#593; thanks to Nathan Weeks.)
- Sort no longer rewrites the header when merging from files. It can also now
  merge from memory, so fewer temporary files need to be written and it is
  better at sorting in parallel when everything fits in memory.
- Both sort and merge now resolve ties when merging based on the position in
  the input file(s). This makes them fully stable for all ordering options.
  (Previously position sort was stable, but name and by tag sorts were not).
- New --output-qname option for mpileup.
- Support for building on Windows using msys2/mingw64 or cygwin has been
  improved.

* Tue Jun 27 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.5-1
- Samtools fastq now has a -i option to create a fastq file from an index tag,
  and a -T option (similar to -t) to add user specified aux tags to the fastq
  header line.
- Samtools fastq can now create compressed fastq files, by giving the output
  filenames an extention of .gq, .bgz, or .bgzf
- Samtools sort has a -t TAG option, that allows records to be sorted by the
  value of the specified aux tag, then by position or name. Merge gets a
  similar option, allowing files sorted this way to be merged. (#675; thanks to
  Patrick Marks of 10xgenomics).

* Thu May 25 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.4.1-1
- This is primarily a security bug fix update.
- Added options to fastq to create fastq files from BC (or other) tags.
- Samtools view has gained a -G option to exclude on all bits set. For example
  to discard reads where neither end has been mapped use "-G 12".
- Samtools cat has a -b option to ease concatenation of many files.
- Added misc/samtools_tab_completion for bash auto-completion of samtools
  sub-commands. (#560)
- Samtools tview now has J and K keys for verticale movement by 20 lines.
  (#257)
- Various compilation / portability improvements.
- Fixed issue with more than 65536 CIGAR operations and SAM/CRAM files.  (#667)
