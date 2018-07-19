%define priority 19
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bcftools
Version:	1.9
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
   --slave %{_bindir}/plot-vcfstats plot-vcfstats /opt/bioit/%{name}/%{version}/bin/plot-vcfstats \
   --slave %{_bindir}/vcfutils.pl vcfutils.pl /opt/bioit/%{name}/%{version}/bin/vcfutils.pl \
   --slave %{_mandir}/man1/bcftools.1 bcftools.1 /opt/bioit/%{name}/%{version}/share/man/man1/bcftools.1

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bcftools /opt/bioit/%{name}/%{version}/bin/bcftools
fi

%files

%changelog
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
