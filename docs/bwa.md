# Bwa

[https://github.com/lh3/bwa](https://github.com/lh3/bwa)

## Automatic Build

Inside `${HOME}/bioit/apps/bwa/SPEC` there is a script called `build`. This j
ust requires the version number and will download, compile, install and create t
he modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/bwa/SPEC/build 0.7.16a

When that completes check that the new version is available using:

    module avail bwa

If that shows as being there you can test it works with:

    module load bwa/0.7.16a
    which bwa
    bwa

## Manual Build

Download the `tar.bz2` file into `/opt/bioit/bwa/src` and untar it and go into it.

The `Makefile` is pretty basic so just type `make`

When that completes you need to do the following:

    mkdir -p ../../0.7.16a/bin
    mkdir -p ../../0.7.16a/man/man1
    mv bwa ../../0.7.16a/bin/
    mv *.pl ../../0.7.16a/bin
    mv bwa.1 ../../0.7.16a/man/man1/

## Module setup

Add a module file in `/opt/bioit/modulefiles/bwa/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bwa module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/bwa/0.7.16a/bin
    prepend-path  MANPATH      /opt/bioit/bwa/0.7.16a/man

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/bwa/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bwa.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
