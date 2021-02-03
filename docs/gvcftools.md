# Gvcftools

[https://github.com/sequencing/gvcftools](https://github.com/sequencing/gvcftools)

## Automatic Build

Inside `${HOME}/bioit/apps/gvcftools/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows: 

    ${HOME}/bioit/apps/gvcftools/SPEC/build 0.17.0

When that completes check that the new version is available using:

    module avail gvcftools

If that shows as being there you can test it works with:

    module load gvcftools/0.17.0
    which twins
    twins --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the version to be built into `/opt/bioit/gvcftools/src` and untar

    make
    mkdir /opt/bioit/gvcftools/0.17.0
    mv bin /opt/bioit/gvcftools/0.17.0/

## Module setup

Add a module file in `/opt/bioit/modulefiles/gvcftools/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  vcftools module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/gvcftools/0.17.0/bin

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/gvcftools/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb gvcftools.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
