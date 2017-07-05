%define priority 15
%define dir_exists() (if [ ! -d /opt/biology/%{name}/%{version} ]; then \
  echo "/opt/biology/%{name}/%{version} not found!"; exit 1 \
fi )
%define dist .el7.bioit

Name:		bcftools
Version:	1.5
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
   --install %{_bindir}/bcftools bcftools /opt/biology/%{name}/%{version}/bin/bcftools %{priority} \
   --slave %{_bindir}/plot-vcfstats plot-vcfstats /opt/biology/%{name}/%{version}/bin/plot-vcfstats \
   --slave %{_bindir}/vcfutils.pl vcfutils.pl /opt/biology/%{name}/%{version}/bin/vcfutils.pl \
   --slave %{_mandir}/man1/bcftools.1 bcftools.1 /opt/biology/%{name}/%{version}/share/man/man1/bcftools.1

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove bcftools /opt/biology/%{name}/%{version}/bin/bcftools
fi

%files

%changelog
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
