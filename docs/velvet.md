# Velvet

VELVET has been deleted so the URL doesn't work any more.

[https://www.ebi.ac.uk/~zerbino/velvet/](https://www.ebi.ac.uk/~zerbino/velvet/)

## Automatic Build

Inside `${HOME}/bioit/apps/velvet/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows: 

    ${HOME}/bioit/apps/velvet/SPEC/build 1.2.10

When that completes check that the new version is available using:

    module avail velvet

If that shows as being there you can test it works with:

    module load velvet/1.2.10
    which velvetg
    velvetg

If all is good, you can move to the RPM building step.

## Manual Build

Download the version to be built into `/opt/bioit/velvet/src` and untar and cd into the resulting directory. Then run the following:

    # Tweak makefile
    sed 's+CATEGORIES=2+CATEGORIES=99+g' --in-place Makefile
    sed 's+MAXKMERLENGTH=31+MAXKMERLENGTH=255+g' --in-place Makefile
    # Compile
    make 'OPENMP=8'
    # Fix perl shebangs
    find . -type f -name '*.pl' | xargs sed 's=/usr/local/bin/perl=/usr/bin/perl=g' --in-place
    mkdir /opt/bioit/velvet/1.2.10
    mv velveth /opt/bioit/velvet/1.2.10
    mv velvetg /opt/bioit/velvet/1.2.10
    mv contrib /opt/bioit/velvet/1.2.10

## Module setup

Add a module file in `/opt/bioit/modulefiles/velvet/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  velvet module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/velvet/1.2.10

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/velvet/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb velvet.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
