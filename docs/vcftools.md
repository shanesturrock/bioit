# Vcftools

[https://vcftools.github.io](https://vcftools.github.io)

## Automatic Build

Inside `${HOME}/bioit/apps/vcftools/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows: 

    ${HOME}/bioit/apps/vcftools/SPEC/build 0.1.16

When that completes check that the new version is available using:

    module avail vcftools

If that shows as being there you can test it works with:

    module load vcftools/0.1.16
    which vcftools
    vcftools --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the version to be built into `/opt/bioit/vcftools/src` and untar

    ./configure --prefix=/opt/bioit/vcftools/0.1.16
    make
    make install

All perl scripts need to have the following change so that they'll find the perl modules they need to load:

    cd /opt/bioit/vcftools/0.1.16/bin
    sed "s+use strict;+use lib '/opt/bioit/vcftools/0.1.16/share/perl5'; use strict;+" \
    --in-place *

## Module setup

Add a module file in `/opt/bioit/modulefiles/vcftools/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  vcftools module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/vcftools/0.1.16/bin
    prepend-path  MANPATH      /opt/bioit/vcftools/0.1.16/share/man

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/vcftools/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb vcftools.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
