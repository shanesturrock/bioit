# vsearch

[https://github.com/torognes/vsearch](https://github.com/torognes/vsearch)

## Automatic Build

Inside `${HOME}/bioit/apps/vsearch/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows: 

    ${HOME}/bioit/apps/vsearch/SPEC/build 2.8.4

When that completes check that the new version is available using:

    module avail vsearch

If that shows as being there you can test it works with:

    module load vsearch/2.8.4
    which vsearch
    vsearch --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the version to be built into `/opt/bioit/vsearch/src` and untar

    ./autogen.sh
    ./configure --prefix=/opt/bioit/vsearch/2.8.4
    sed -i -e 's/native/x86-64/g' Makefile src/Makefile
    make
    make install

The `sed` line prevents it building binaries that won't run on all 64 bit pricessors.

## Module setup

Add a module file in `/opt/bioit/modulefiles/vsearch/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  vsearch module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/vsearch/2.8.4/bin
    prepend-path  MANPATH      /opt/bioit/vsearch/2.8.4/share/man

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/vsearch/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb vsearch.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
