## Homepage

http://www.htslib.org/

## Build

Download the version to be built into `/opt/bioit/htslib/src` and untar

Inside the source run the following where 1.5 is the current one being built:

    ./configure --prefix=/opt/bioit/htslib/1.5
    make
    make install

## Module setup

Add a module file in `/opt/bioit/modulefiles/htslib/` for this version by copying previous ones and modifying the paths. Note that this file loads `bcftools/1.5` as a dependency since samtools and bcftools should be used together.

    #%Module 1.0
    #
    #  htslib module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/htslib/1.5/bin
    prepend-path  MANPATH      /opt/bioit/htslib/1.5/share/man

## RPM

There's a SPEC file for this package in `~/bioit/apps/htslib/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb htslib

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
