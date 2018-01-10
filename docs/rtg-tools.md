# RTG-TOOLS

[https://github.com/RealTimeGenomics/rtg-tools](https://github.com/RealTimeGenomics/rtg-tools)

## Automatic Build

Inside `${HOME}/bioit/apps/rtg-tools/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/rtg-tools/SPEC/build 3.8.4

When that completes check that the new version is available using:

    module avail rtg-tools

If that shows as being there you can test it works with:

    module load rtg-tools/3.8.4
    which rtg-tools
    rtg-tools version

If all is good, you can move to the RPM building step.

## Manual Build

Download the `linux-x64.zip` file into `/opt/bioit/rtg-tools/src` and unzip it.

Move the unpackaged directory as follows:

    mv rtg-tools-3.8.4 /opt/bioit/rtg-tools/3.8.4

Make sure you run /opt/bioit/rtg-tools/3.8.4/rtg once as build to set up the initial configuration file.

That should do it.

## Module setup

Add a module file in `/opt/bioit/modulefiles/rtg-tools/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  rtg-tools module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/rtg-tools/3.8.4

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/rtg-tools/SPEC` so modify that with the new version details found in the ReleaseNotes.txt file inside the install directory.

    rpmbuild -bb rtg-tools.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
