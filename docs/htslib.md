# Htslib

[http://www.htslib.org/](http://www.htslib.org/)

## Automatic Build

Inside `${HOME}/bioit/apps/htslib/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/htslib/SPEC/build 1.22.1

When that completes check that the new version is available using:

    module avail htslib

If that shows as being there you can test it works with:

    module load htslib/1.22.1
    which tabix
    tabix --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the version to be built into `/opt/bioit/htslib/src` and untar

Inside the source run the following where 1.22.1 s the current one being built:

    ./configure --prefix=/opt/bioit/htslib/1.22.1
    make
    make install

## Module setup

Add a module file in `/opt/bioit/modulefiles/htslib/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  htslib module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/htslib/1.22.1/bin
    prepend-path  MANPATH      /opt/bioit/htslib/1.22.1/share/man

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/htslib/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb htslib

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
