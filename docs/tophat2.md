## Homepage

https://ccb.jhu.edu/software/tophat/index.shtml

## Build

Download the `tar.gz` file into `/opt/biology/tophat2/src` and untar it.

Configure and make with the following:

    ./configure --PREFIX=/opt/biology/tophat2/2.1.1
    make
    make install

## Module setup

Add a module file in `/opt/biology/modulefiles/tophat2/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  tophat2 module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/biology/tophat2/2.1.1/bin

## RPM

There's a SPEC file for this package in `/opt/biology/tophat2/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb tophat2.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.