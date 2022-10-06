# Bismark

[https://github.com/FelixKrueger/Bismark](https://github.com/FelixKrueger/Bismark)

## Automatic Build

Inside `${HOME}/bioit/apps/bismark/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/bismark/SPEC/build 0.24.0

When that completes check that the new version is available using:

    module avail bismark

If that shows as being there you can test it works with:

    module load bismark/0.24.0
    which bismark
    bismark --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the source tarball from [here](https://github.com/FelixKrueger/Bismark/archive/0.24.0.tar.gz) into `/opt/bioit/bismark/src`, untar it and move it into place as there's nothing to compile:

    mv Bismark-0.24.0 /opt/bioit/bismark/0.24.0

That should be it.

## Module setup

Add a module file in `/opt/bioit/modulefiles/bismark/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bismark module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/bismark/0.24.0/

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/bismark/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bismark.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
