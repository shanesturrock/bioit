# IGV

[https://github.com/igvteam/igv](https://github.com/igvteam/igv)

## Automatic Build

Inside `${HOME}/bioit/apps/igv/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/igv/SPEC/build 2.15.2

When that completes check that the new version is available using:

    module avail igv

If that shows as being there you can test it works with:

    module load igv/2.15.2
    which igv

If all is good, you can move to the RPM building step.

## Manual Install

Get the Linux zip file from [https://software.broadinstitute.org/software/igv/download](https://software.broadinstitute.org/software/igv/download) and unzip it in the src directory. Then you just need to move the unzipped directory into its final location:

    mv IGV_Linux_2.15.2 /opt/bioit/igv/2.15.2

Rename the run script:

    mv /opt/bioit/igv/2.15.2/igv.sh /opt/bioit/igv/2.15.2/igv

That should be enough for users to launch this version.

## Module setup

Add a module file in `/opt/bioit/modulefiles/igv/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  igv module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/igv/2.15.2/

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/igv/SPEC` so modify that with the new version details. Once changed, build it with the following commands:

    cp ${HOME}/bioit/apps/igv/SPEC/igv.desktop ${HOME}/rpmbuild/SOURCES
    cp ${HOME}/bioit/apps/igv/SPEC/igv-icons.tar.gz ${HOME}/rpmbuild/SOURCES
    cp ${HOME}/bioit/apps/igv/SPEC/bioinformatics* ${HOME}/rpmbuild/SOURCES
    rpmbuild -bb igv.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
