## Homepage

[https://vcftools.github.io](https://vcftools.github.io)

## Build

Download the version to be built into `/opt/bioit/vcftools/src` and untar

    ./configure --prefix=/opt/bioit/vcftools/0.1.15
    make
    make install

All perl scripts need to have the following change so that they'll find the perl modules they need to load:

    cd /opt/bioit/vcftools/0.1.15/bin
    sed "s+use strict;+use lib '/opt/bioit/vcftools/0.1.15/share/perl5'; use strict;+" \
    --in-place *

## Module setup

Add a module file in `/opt/bioit/modulefiles/vcftools/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  vcftools module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/vcftools/0.1.15/bin
    prepend-path  MANPATH      /opt/bioit/vcftools/0.1.15/share/man

## RPM

There's a SPEC file for this package in `~/bioit/apps/vcftools/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb vcftools.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
