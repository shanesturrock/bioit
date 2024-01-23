# Samtools

[http://www.htslib.org/](http://www.htslib.org/)

## Automatic Build

Inside `${HOME}/bioit/apps/samtools/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/samtools/SPEC/build 1.19.1

When that completes check that the new version is available using:

    module avail samtools

If that shows as being there you can test it works with:

    module load samtools/1.19.1
    which samtools
    samtools --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the version to be built into `/opt/bioit/samtools/src` and untar

Inside the source run the following where 1.19.1 is the current one being built:

    ./configure --prefix=/opt/bioit/samtools/1.19.1
    make
    make install

## Module setup

Add a module file in `/opt/bioit/modulefiles/samtools/` for this version by copying previous ones and modifying the paths. Note that this file loads `bcftools/1.19` as a dependency since `samtools` and `bcftools` should be used together.

    #%Module 1.0
    #
    #  samtools module for use with 'environment-modules' package:
    #
    module load bcftools/1.19
    prepend-path  PATH         /opt/bioit/samtools/1.19.1/bin
    prepend-path  MANPATH      /opt/bioit/samtools/1.19.1/share/man

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/samtools/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb samtools.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
