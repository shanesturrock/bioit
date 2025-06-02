# Bcftools

[http://www.htslib.org/](http://www.htslib.org/)

## Automatic Build

Inside `${HOME}/bioit/apps/bcftools/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/bcftools/SPEC/build 1.22

When that completes check that the new version is available using:

    module avail bcftools

If that shows as being there you can test it works with:

    module load bcftools/1.22
    which bcftools
    bcftools --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the version to be built into `/opt/bioit/bcftools/src` and untar

## 1.4.1 and earlier

Inside the source run the following where 1.4.1 is the current one being built:

    make prefix=/opt/bioit/bcftools/1.4.1 install

## 1.5 and later

For 1.5 or later they've switched to a configure based build system the same as samtools so you need to do the following:

    ./configure --prefix=/opt/bioit/bcftools/1.22
    make
    make install

## Module setup

Add a module file in `/opt/bioit/modulefiles/bcftools/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bcftools module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/bcftools/1.22/bin
    prepend-path  MANPATH      /opt/bioit/bcftools/1.22/share/man

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/bcftools/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bcftools.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
