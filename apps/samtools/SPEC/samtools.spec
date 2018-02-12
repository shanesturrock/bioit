%define priority 17
%define dir_exists() (if [ ! -d /opt/bioit/%{name}/%{version} ]; then \
  echo "/opt/bioit/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		samtools
Version:	1.7
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
   --slave %{_bindir}/varfilter.py varfilter.py /opt/bioit/%{name}/%{version}/bin/varfilter.py \
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
