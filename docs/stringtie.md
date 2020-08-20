# stringtie

[https://ccb.jhu.edu/software/stringtie/](https://ccb.jhu.edu/software/stringtie/)

## Automatic Build

Inside `${HOME}/bioit/apps/stringtie/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/stringtie/SPEC/build 2.1.4

When that completes check that the new version is available using:

    module avail stringtie

If that shows as being there you can test it works with:

    module load stringtie/2.1.4
    which stringtie
    stringtie --version

## Manual Build

Download the `stringtie-2.1.4.tar.gz` file into `/opt/bioit/stringtie/src` and untar it. Then run the following:

    cd stringtie-2.1.4
    make release
    mkdir /opt/bioit/stringtie/2.1.4
    mv stringtie /opt/bioit/stringtie/2.1.4

## Module setup

Add a module file in `/opt/bioit/modulefiles/stringtie/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  stringtie module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/stringtie/2.1.4

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/stringtie/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb stringtie.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
