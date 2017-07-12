## Homepage

https://github.com/lh3/bwa

## Build

Download the `tar.bz2` file into `/opt/biology/bwa/src` and untar it and go into it.

The `Makefile` is pretty basic so just type `make`

When that completes you need to do the following:

    mkdir ../../0.7.15/bin
    mkdir -p ../../0.7.15/man/man1
    mv bwa ../../0.7.15/bin/
    mv *.pl ../../0.7.15/bin
    mv bwa.1 ../../0.7.15/man/man1/

## Module setup

Add a module file in `/opt/biology/modulefiles/bwa/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bwa module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/biology/bwa/0.7.15/bin
    prepend-path  MANPATH      /opt/biology/bwa/0.7.15/man

## RPM

There's a SPEC file for this package in `/opt/biology/bwa/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bwa.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
