%define priority 1130
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bcftools
Version:	1.14
Release:	1%{?dist}
Summary:	Tools for nucleotide sequence alignments in the SAM format

Group:		Applications/Engineering
License:	MIT
URL:		http://samtools.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	samtools
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

%description
BCFtools implements utilities for variant calling (in conjunction with
SAMtools) and manipulating VCF and BCF files.  The program is intended
to replace the Perl-based tools from vcftools.

%pre
%dir_exists

%post
alternatives \
   --install %{_bindir}/bcftools bcftools /opt/bioit/%{name}/%{version}/bin/bcftools %{priority} \
   --slave %{_bindir}/guess-ploidy.py guess-ploidy.py /opt/bioit/%{name}/%{version}/bin/guess-ploidy.py \
   --slave %{_bindir}/plot-vcfstats plot-vcfstats /opt/bioit/%{name}/%{version}/bin/plot-vcfstats \
   --slave %{_bindir}/vcfutils.pl vcfutils.pl /opt/bioit/%{name}/%{version}/bin/vcfutils.pl \
   --slave %{_bindir}/color-chrs.pl color-chrs.pl /opt/bioit/%{name}/%{version}/bin/color-chrs.pl \
   --slave %{_bindir}/plot-roh.py plot-roh.py /opt/bioit/%{name}/%{version}/bin/plot-roh.py \
   --slave %{_bindir}/run-roh.pl run-roh.pl /opt/bioit/%{name}/%{version}/bin/run-roh.pl \
   --slave %{_mandir}/man1/bcftools.1 bcftools.1 /opt/bioit/%{name}/%{version}/share/man/man1/bcftools.1

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bcftools /opt/bioit/%{name}/%{version}/bin/bcftools
fi

%files

%changelog
* Mon Nov 08 2021 Shane Sturrock <shane.sturrock@gmail.com> - 1.14-1
- https://github.com/samtools/bcftools/releases/tag/1.14

* Tue Jul 20 2021 Shane Sturrock <shane.sturrock@gmail.com> - 1.13-1
- 1.12 https://github.com/samtools/bcftools/releases/tag/1.12
- 1.13 https://github.com/samtools/bcftools/releases/tag/1.13

* Fri Oct 16 2020 Shane Sturrock <shane.sturrock@gmail.com> - 1.11-1
- Changes affecting the whole of bcftools, or multiple commands:
  - Filtering -i/-e expressions
    - Breaking change in -i/-e expressions on the FILTER column. Originally it
      was possible to query only a subset of filters, but not an exact match.
      The new behaviour is: 
      Expression    Result 
      FILTER="A"    Exact match, for example "A;B" does not pass 
      FILTER!="A"   Exact match, for example "A;B" does pass
      FILTER~"A"    Both "A" and "A;B" pass 
      FILTER!~"A"   Neither "A" nor "A;B" pass
    - Fix in commutative comparison operators, in some cases reversing sides
      would produce incorrect results (#1224; #1266)
    - Better support for filtering on sample subsests
    - Add SMPL_*/S* family of functions that evaluate within rather than across
      all samples. (#1180)
  - Improvements in the build system
- Changes affecting specific commands:
  - bcftools annotate:
    - Previously it was not possible to use --columns =TAG with INFO tags and
      the --merge-logic feature was restricted to tab files with BEG,END
      columns, now extended to work also with REF,ALT.
    - Make annotate -TAG/+TAG work also with FORMAT fields. (#1259)
    - ID and FILTER can be transferred to INFO and ID can be populated from
      INFO.  However, the FILTER column still cannot be populated from an INFO
      tag because all possible FILTER values must be known at the time of
      writing the header (#947; #1187)
  - bcftools consensus:
    - Fix in handling symbolic deletions and overlapping variants. (#1149;
      #1155; #1295)
    - Fix --iupac-codes crash on REF-only positions with ALT=".". (#1273)
    - Fix --chain crash. (#1245)
    - Preserve the case of the genome reference. (#1150)
    - Add new -a, --absent option which allows to set positions with no
      supporting evidence to "N" (or any other character). (#848; #940)
  - bcftools convert:
    - The option --vcf-ids now works also with -haplegendsample2vcf. (#1217)
    - New option --keep-duplicates
  - bcftools csq:
    - Add misc/gff2gff.py script for conversion between various flavors of GFF
      files. The initial commit supports only one type and was contributed by
      @flashton2003. (#530)
    - Add missing consequence types. (PR #1203; #1292)
    - Allow overlapping CDS to support ribosomal slippage. (#1208)
  - bcftools +fill-tags:
    - Added new annotations: INFO/END, TYPE, F_MISSING.
  - bcftools filter:
    - Make --SnpGap optionally filter also SNPs close to other variant types.
      (#1126)
  - bcftools gtcheck:
    - Complete revamp of the command. The new version is faster and allows N:M
      sample comparisons, not just 1:N or NxN comparisons. Some functionality
      was lost (plotting and clustering) but may be added back on popular
      demand.
  - bcftools +mendelian:
    - Revamp of user options, output VCFs with mendelian errors annotation, read
      PED files (thanks to Giulio Genovese).
  - bcftools merge:
    - Update headers when appropriate with the '--info-rules *:join' INFO rule.
      (#1282)
    - Local alleles merging that produce LAA and LPL when requested, a draft
      implementation of samtools/hts-specs#434 (#1138)
    - New --no-index which allows to merge unindexed files. Requires the input
      files to have chromosomes in th same order and consistent with the order
      of sequences in the header. (PR #1253; samtools/htslib#1089)
    - Fixes in gVCF merging. (#1127; #1164)
  - bcftools norm:
    - Fixes in --check-ref s reference setting features with non-ACGT bases.
      (#473; #1300)
    - New --keep-sum switch to keep vector sum constant when splitting
      multiallelics. (#360)
  - bcftools +prune:
    - Extend to allow annotating with various LD metrics: r^2, Lewontin's D'
      (PMID:19433632), or Ragsdale's D (PMID:31697386).
  - bcftools query:
    - New %N_PASS() formatting expression to output the number of samples that
      pass the filtering expression.
  - bcftools reheader:
    - Improved error reporting to prevent user mistakes. (#1288)
  - bcftools roh:
   - Several fixes and improvements
   - the --AF-file description incorrectly suggested "REF\tALT" instead of the
     correct "REF,ALT". (#1142)
   - RG lines could have negative length. (#1144)
   - new --include-noalt option to allow also ALT=. records. (#1137)
  - bcftools scatter:
    - New plugin intended as a convenient inverse to concat (thanks to Giulio
      Genovese, PR #1249)
  - bcftools +split:
    - New --groups-file option for more flexibility of defining desired output.
      (#1240)
    - New --hts-opts option to reduce required memory by reusing one output
      header and allow overriding the default hFile's block size with
      --hts-opts block_size=XXX. On some file systems (lustre) the default size
      can be 4M which becomes a problem when splitting files with 10+ samples.
    - Add support for multisample output and sample renaming
  - bcftools +split-vep:
    - Add default types (Integer, Float, String) for VEP subfields and make
      --columns - extract all subfields into INFO tags in one go.

* Fri Mar 20 2020 Shane Sturrock <shane.sturrock@gmail.com> - 1.10.2-1
- Numerous bug fixes, usability improvements and sanity checks were added to
  prevent common user errors.
- The -r, --regions (and -R, --regions-file) option should never create
  unsorted VCFs or duplicates records again. This also fixes rare cases where a
  spanning deletion makes a subsequent record invisible to bcftools isec and
  other commands.
- Additions to filtering and formatting expressions
  - support for the spanning deletion alternate allele (ALT=*)
  - new ILEN filtering expression to be able to filter by indel length
  - new MEAN, MEDIAN, MODE, STDEV, phred filtering functions
  - new formatting expression %PBINOM (phred-scaled binomial probability),
    %INFO (the whole INFO column), %FORMAT (the whole FORMAT column), %END (end
    %position of the REF allele), %END0 (0-based end position of the REF
    %allele), %MASK (with multiple files indicates the presence of the site in
    %other files)
- New plugins
  - +gvcfz: compress gVCF file by resizing gVCF blocks according to specified
    criteria
  - +indel-stats: collect various indel-specific statistics
  - +parental-origin: determine parental origin of a CNV region
  - +remove-overlaps: remove overlapping variants.
  - +split-vep: query structured annotations such INFO/CSQ created by
    bcftools/csq or VEP
  - +trio-dnm: screen variants for possible de-novo mutations in trios
- annotate
  - new -l, --merge-logic option for combining multiple overlapping regions
- call
  - new bcftools call -G, --group-samples option which allows grouping samples
    into populations and applying the HWE assumption within but not across the
    groups.
- csq
  - significant reduction of memory usage in the local -l mode for VCFs with
    thousands of samples and 20% reduction in the non-local haplotype-aware
    mode.
  - fixes a small memory leak and formatting issue in FORMAT/BCSQ at sites with
    many consequences
  - do not print protein sequence of start_lost events
  - support for "start_retained" consequence
  - support for symbolic insertions (ALT="<INS...>"), "feature_elongation"
    consequence
  - new -b, --brief-predictions option to output abbreviated protein
    predictions.
- concat
  - the --naive command now checks header compatibility when concatenating
    multiple files.
- consensus
  - add a new -H, --haplotype 1pIu/2pIu feature to output first/second allele
    for phased genotypes and the IUPAC code for unphased genotypes
  - new -p, --prefix option to add a prefix to sequence names on output
- +contrast
  - added support for Fisher's test probability and other annotations
- +fill-from-fasta
  - new -N, --replace-non-ACGTN option
- +dosage
  - fix some serious bugs in dosage calculation
- +fill-tags
  - extended to perform simple on-the-fly calculations such as calculating
    INFO/DP from FORMAT/DP.
- merge
  - add support for merging FORMAT strings
  - bug fixed in gVCF merging
- mpileup
  - a new optional SCR annotation for the number of soft-clipped reads
- reheader
  - new -f, --fai option for updating contig lines in the VCF header
- +trio-stats
  - extend output to include DNM homs and recurrent DNMs
- VariantKey support

* Fri Jul 20 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.9-1
- annotate
  - REF and ALT columns can be now transferred from the annotation file.
  - fixed bug when setting vector_end values.
- consensus
  - new -M option to control output at missing genotypes
  - variants immediately following insersions should not be skipped. Note
    however, that the current fix requires normalized VCF and may still falsely
    skip variants adjacent to multiallelic indels.
  - bug fixed in -H selection handling
- convert
  - the --tsv2vcf option now makes the missing genotypes diploid, "./." instead
    of "."
  - the behavior of -i/-e with --gvcf2vcf changed. Previously only sites with
    FILTER set to "PASS" or "." were expanded and the -i/-e options dropped
    sites completely. The new behavior is to let the -i/-e options control
    which records will be expanded. In order to drop records completely, one
    can stream through "bcftools view" first.
- csq
  - since the real consequence of start/splice events are not known, the
    aminoacid positions at subsequent variants should stay unchanged
  - add --force option to skip malformatted transcripts in GFFs with
    out-of-phase CDS exons.
- +dosage: output all alleles and all their dosages at multiallelic sites
- +fixref: fix serious bug in -m top conversion
- -i/-e filtering expressions:
  - add two-tailed binomial test
  - add functions N_PASS() and F_PASS()
  - add support for lists of samples in filtering expressions, with many
    samples it was impractical to list them all on the command line. Samples
    can be now in a file as, e.g., GT[@samples.txt]="het"
  - allow multiple perl functions in the expressions and some bug fixes
  - fix a parsing problem, @ was not removed from @filename expressions
- mpileup: fixed bug where, if samples were renamed using the -G
  (--read-groups) option, some samples could be omitted from the output file.
- norm: update INFO/END when normalizing indels
- +split: new -S option to subset samples and to use custom file names instead
  of the defaults
- +smpl-stats: new plugin
- +trio-stats: new plugin
- Fixed build problems with non-functional configure script produced on some
  platforms

* Fri Apr 06 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.8-1
- -i, -e filtering: Support for custom perl scripts
- +contrast: New plugin to annotate genotype differences between groups of
  samples
- +fixploidy: New options for simpler ploidy usage
- +setGT: Target genotypes can be set to phased by giving --new-gt p
- run-roh.pl: Allow to pass options directly to bcftools roh
- Number of bug fixes

* Tue Feb 13 2018 Shane Sturrock <shane.sturrock@gmail.com> - 1.7-1
- -i, -e filtering: Major revamp, improved filtering by FORMAT fields and
  missing values. New GT=ref,alt,mis etc keywords, check the documentation for
  details.
- query: Only matching expression are printed when both the -f and -i/-e
  expressions contain genotype fields. Note that this changes the original
  behaviour. Previously all samples were output when one matching sample was
  found. This functionality can be achieved by pre-filtering with view and then
  streaming to query. Compare 
     bcftools query -f'[%CHROM:%POS %SAMPLE %GT\n]' -i'GT="alt"' file.bcf 
  and 
    bcftools view -i'GT="alt"' file.bcf -Ou | \
    bcftools query -f'[%CHROM:%POS %SAMPLE %GT\n]'
- annotate: New -k, --keep-sites option
- consensus: Fix --iupac-codes output
- csq: Homs always considered phased and other fixes
- norm: Make -c none work and remove query -c
- roh: Fix errors in the RG output
- stats: Allow IUPAC ambiguity codes in the reference file; report the number
  of missing genotypes
- +fill-tags: Add ExcHet annotation
- +setGt: Fix bug in binom.test calculation, previously it worked only for
  nAlt<nRef!
- +split: New plugin to split a multi-sample file into single-sample files in
  one go
- Improve python3 compatibility in plotting scripts

* Tue Oct 03 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.6-1
- New sort command.
- New options added to the consensus command. Note that the -i, --iupac option
  has been renamed to -I, --iupac, in favor of the standard -i, --include.
- Filtering expressions (-i/-e): support for GT=<type> expressions and for
  lists and ranges (#639) - see the man page for details.
- csq: relax some GFF3 parsing restrictions to enable using Ensembl GFF3 files
  for plants (#667)
- stats: add further documentation to output stats files (#316) and include
  haploid counts in per-sample output (#671).
- plot-vcfstats: further fixes for Python3 (@nsoranzo, #645, #666).
- query bugfix (#632)
- +setGT plugin: new option to set genotypes based on a two-tailed binomial
  distribution test. Also, allow combining -i/-e with -t q.
- mpileup: fix typo (#636)
- convert --gvcf2vcf bugfix (#641)
- +mendelian: recognize some mendelian inconsistencies that were being missed
  (@oronnavon, #660), also add support for multiallelic sites and sex
  chromosomes.

* Tue Jun 27 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.5-1
- Added autoconf support to bcftools. See INSTALL for more details.
- norm: Make norm case insensitive (#601). Trim the reference allele (#602).
- mpileup: fix for misreported indel depths for reads containing adjacent
  indels (3c1205c).
- plot-vcfstats: Open stats file in text mode, not binary (#618).
- fixref plugin: Allow multiallelic sites in the -i, --use-id reference. Also
  flip genotypes, not just REF/ALT!
- merge: fix gVCF merge bug when last record on a chromosome opened a gVCF
  block (#616)
- New options added to the ROH plotting script.
- consensus: Properly flush chain info (#606, thanks to @krooijers).
- New +prune plugin for pruning sites by LD (R2) or maximum number of records
  within a window.
- New N_MISSING, F_MISSING (number and fraction missing) filtering expressions.
- Fix HMM initialization in roh when snapshots are used in multiple chromosome
  VCF.
- Fix buffer overflow (#607) in filter.

* Thu May 25 2017 Shane Sturrock <shane.sturrock@gmail.com> - 1.4.1-1
- This is primarily a security bug fix update.
- roh: Fixed malfunctioning options -m, --genetic-map and -M, --rec-rate, and
  newly allowed their combination. Added a convenience wrapper misc/run-roh.pl
  and an interactive script for visualizing the calls misc/plot-roh.py.  
- csq: More control over warning messages (#585).
- Portability improvements (#587). Still work to be done on this front.
- Add support for breakends to view, norm, query and filtering (#592).
- plot-vcfstats: Fix for python 2/3 compatibility (#593).
- New -l, --list option for +af-dist plugin.
- New -i, --use-id option for +fix-ref plugin.
- Add --include/--exclude options to +guess-ploidy plugin.
- New +check-sparsity plugin.
- Miscellaneous bugfixes for #575, #584, #588, #599, #535.
