# Hmmer

[http://hmmer.org/](http://hmmer.org/)

## Automatic Build

Inside `${HOME}/bioit/apps/hmmer/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/hmmer/SPEC/build 3.1b2

When that completes check that the new version is available using:

    module avail hmmer

If that shows as being there you can test it works with:

    module load hmmer/3.1b2
    which hmmalign
    hmmalign -h 

If all is good, you can move to the RPM building step.

## Manual Build

Download the binary tarball from [here](http://eddylab.org/software/hmmer3/3.1b2/hmmer-3.1b2-linux-intel-x86_64.tar.gz) into `/opt/bioit/hmmer/src`, untar it and cd into the resulting directory then run the following:

    mv binaries /opt/bioit/hmmer/3.1b2

## Module setup

Add a module file in `/opt/bioit/modulefiles/hmmer/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  hmmer module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/hmmer/3.1b2/

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/hmmer/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb hmmer.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.