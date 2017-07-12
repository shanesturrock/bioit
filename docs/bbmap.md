## Homepage

https://sourceforge.net/projects/bbmap/

## Build

Download the version to be built into `/opt/biology/bedtools2/src` and untar

There's nothing to actually build so just run the following to move the files and correct the permissions:

    mv bbmap ../37.31
    chmod 755 ../37.31
    cd ../37.31
    chmod -R 755 *

## Module setup

Add a module file in `/opt/biology/modulefiles/bbmap/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bbmap module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/biology/bbmap/37.31

## RPM

There's a SPEC file for this package in `/opt/biology/bbmap/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bbmap.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.