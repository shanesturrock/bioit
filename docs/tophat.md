# TopHat

[https://ccb.jhu.edu/software/tophat/index.shtml](https://ccb.jhu.edu/software/tophat/index.shtml)

## Automatic Build

Inside `${HOME}/bioit/apps/tophat/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows: 

    ${HOME}/bioit/apps/tophat/SPEC/build 2.1.1

When that completes check that the new version is available using:

    module avail tophat

If that shows as being there you can test it works with:

    module load tophat/2.1.1
    which tophat
    tophat --version

If all is good, you can move to the RPM building step.

## Manual Build

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

There's a SPEC file for this package in `${HOME}/bioit/apps/tophat/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb tophat.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
