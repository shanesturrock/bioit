# Augustus

[http://bioinf.uni-greifswald.de/augustus/](http://bioinf.uni-greifswald.de/augustus/)

## Automatic Build

Inside `${HOME}/bioit/apps/augustus/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/augustus/SPEC/build 3.4.0

When that completes check that the new version is available using:

    module avail augustus

If that shows as being there you can test it works with:

    module load augustus/3.4.0
    which augustus
    augusutus

If all is good, you can move to the RPM building step.

## Manual Build

Work through errors in the automatic build script to figure out what went wrong and fix them.

## Module setup

Add a module file in `/opt/bioit/modulefiles/augustus/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  augustus module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/augustus/3.4.0/bin:/opt/bioit/augustus/3.4.0/scripts

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/augustus/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb augustus.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
