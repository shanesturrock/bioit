# TopHat

[https://ccb.jhu.edu/software/tophat/index.shtml](https://ccb.jhu.edu/software/tophat/index.shtml)

## Build

Download the `tar.gz` file into `/opt/bioit/tophat/src` and untar it.

Configure and make with the following:

    ./configure --prefix=/opt/bioit/tophat/2.1.1
    make
    make install

## Module setup

Add a module file in `/opt/bioit/modulefiles/tophat/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  tophat module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/tophat/2.1.1/bin

## RPM

There's a SPEC file for this package in `~/bioit/apps/tophat/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb tophat.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
