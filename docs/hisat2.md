# HiSat2

[https://ccb.jhu.edu/software/hisat2/index.shtml](https://ccb.jhu.edu/software/hisat2/index.shtml)

## Automatic Build

Inside `${HOME}/bioit/apps/hisat2/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/hisat2/SPEC/build 2.2.1

When that completes check that the new version is available using:

    module avail hisat2

If that shows as being there you can test it works with:

    module load hisat2/2.2.1
    which hisat2
    hisat2 --version

## Manual Build

Download the version to be built into `/opt/bioit/hisat2/src` and unzip. Here we'll use version 2.2.1.

Inside the source run the following:

    make

This just builds in the current location. Since it isn't good to have the binaries in the same location as the source, you first need to move docs, examples and scripts:

    mv scripts /opt/bioit/hisat2/2.2.1/
    mv docs /opt/bioit/hisat2/2.2.1/
    mv example /opt/bioit/hisat2/2.2.1/

Now you need to move all the binaries and python packages into `/opt/bioit/hisat2/2.2.1/bin` as follows:

    mkdir /opt/bioit/hisat2/2.2.1/bin
    mv hisat2 /opt/bioit/hisat2/2.2.1/bin/
    mv hisat2-* /opt/bioit/hisat2/2.2.1/bin/
    mv *.py /opt/bioit/hisat2/2.2.1/bin/

Note that you need to change the version number to match what you're building.

## Module setup

Add a module file in `/opt/bioit/modulefiles/hisat2/` for this version by copying previous ones and modifying the path.

    #%Module 1.0
    #
    #  hisat2 module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/hisat2/2.2.1/bin

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/hisat2/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb hisat2.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
