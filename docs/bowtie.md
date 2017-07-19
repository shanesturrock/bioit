## Homepage

https://github.com/BenLangmead/bowtie

## Build

Download the `src.zip` file into `/opt/bioit/bowtie/src` and unzip it.

Edit the `Makefile` to change the value of prefix as follows (change the version as required):

    prefix = /opt/bioit/bowtie/1.2.1.1

Compile it with the following commands:

    make NO_TBB=1
    make install

## Module setup

Add a module file in `/opt/bioit/modulefiles/bowtie/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bowtie module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/bowtie/1.2.1.1/bin

## RPM

There's a SPEC file for this package in `~/bioit/apps/bowtie/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bowtie.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
