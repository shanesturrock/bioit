## Homepage

http://www.htslib.org/

## Build

Download the version to be built into `/opt/biology/bcftools/src` and untar

## 1.4.1 and earlier

Inside the source run the following where 1.4.1 is the current one being built:

    make prefix=/opt/biology/samtools/1.4.1 install

## 1.5 and later

For 1.5 or later they've switched to a configure based build system the same as samtools so you need to do the following:

    ./configure --prefix=/opt/biology/bcftools/1.5
    make
    make install

## Module setup

Add a module file in `/opt/biology/modulefiles/bcftools/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bcftools module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/biology/bcftools/1.5/bin
    prepend-path  MANPATH      /opt/biology/bcftools/1.5/share/man

## RPM

There's a SPEC file for this package in `/opt/biology/bcftools/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bcftools.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.