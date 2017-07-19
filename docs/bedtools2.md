## Homepage

https://github.com/arq5x/bedtools2

## Build

Download the version to be built into `/opt/bioit/bedtools2/src` and untar

Edit the `Makefile` to change the prefix:

    prefix ?= /opt/bioit/bedtools2/2.26.0

Then type the following commands:

    make
    make install

## Module setup

Add a module file in `/opt/bioit/modulefiles/bedtools2/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bedtools2 module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/bedtools2/2.26.0/bin

## RPM

There's a SPEC file for this package in `~/bioit/apps/bedtools2/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bedtools2.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
