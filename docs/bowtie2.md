## Homepage

[https://github.com/BenLangmead/bowtie2](https://github.com/BenLangmead/bowtie2)

## Build

Download the `src.zip` file into `/opt/bioit/bowtie/src` and unzip it.

Edit the `Makefile` to change the value of prefix as follows (change the version as required):

    prefix = /opt/bioit/bowtie2/2.3.2

Compile it with the following commands:

    make NO_TBB=1
    make install

## Module setup

Add a module file in `/opt/bioit/modulefiles/bowtie2/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bowtie2 module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/bowtie2/1.2.1.1/bin

## RPM

There's a SPEC file for this package in `~/bioit/apps/bowtie2/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bowtie2.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
