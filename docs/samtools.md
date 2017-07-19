## Homepage

[http://www.htslib.org/](http://www.htslib.org/)

## Build

Download the version to be built into `/opt/bioit/samtools/src` and untar

Inside the source run the following where 1.5 is the current one being built:

    ./configure --prefix=/opt/bioit/samtools/1.5
    make
    make install

## Module setup

Add a module file in `/opt/bioit/modulefiles/samtools/` for this version by copying previous ones and modifying the paths. Note that this file loads `bcftools/1.5` as a dependency since `samtools` and `bcftools` should be used together.

    #%Module 1.0
    #
    #  samtools module for use with 'environment-modules' package:
    #
    module load bcftools/1.5
    prepend-path  PATH         /opt/bioit/samtools/1.5/bin
    prepend-path  MANPATH      /opt/bioit/samtools/1.5/share/man

## RPM

There's a SPEC file for this package in `~/bioit/apps/samtools/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb samtools.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
