# FastQC

[http://www.bioinformatics.babraham.ac.uk/projects/fastqc/](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)

## Automatic Build

Inside `${HOME}/bioit/apps/FastQC/SPEC` there is a script called `build`. This j
ust requires the version number and will download, compile, install and create t
he modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/FastQC/SPEC/build 0.11.9

When that completes check that the new version is available using:

    module avail FastQC

If that shows as being there you can test it works with:

    module load FastQC/0.11.9
    which FastQC

## Manual Build

Download the Linux zip version to be built into `/opt/bioit/FastQC/src` and unzip.

The resulting FastQC directory should be moved to a versioned directory and the `fastqc` command made executable:

    mv FastQC ../0.11.9
    cd ../0.11.9
    chmod 755 fastqc

## Module setup

Add a module file in `/opt/bioit/modulefiles/FastQC/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  FastQC module for use with 'environment-modules' package:
    #
    prepend-path  PATH              /opt/bioit/FastQC/0.11.9

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/FastQC/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb FasqtQC.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
