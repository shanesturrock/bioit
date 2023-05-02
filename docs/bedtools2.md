# Bedtools2

[https://github.com/arq5x/bedtools2](https://github.com/arq5x/bedtools2)

## Automatic Build

Inside `${HOME}/bioit/apps/bedtools2/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/bedtools2/SPEC/build 2.31.0

When that completes check that the new version is available using:

    module avail bedtools2

If that shows as being there you can test it works with:

    module load bedtools2/2.31.0
    which bedtools
    bedtools --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the version to be built into `/opt/bioit/bedtools2/src` and untar

Edit the `Makefile` to change the prefix:

    prefix ?= /opt/bioit/bedtools2/2.31.0

Then type the following commands:

    make
    make install

## Module setup

Add a module file in `/opt/bioit/modulefiles/bedtools2/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bedtools2 module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/bedtools2/2.31.0/bin

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/bedtools2/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bedtools2.spec

This will create an RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64`. It checks that the installation directory exists and will fail if it isn't there.

Before you install this, you need to sign it using:

    rpm --addsign \
    ${HOME}/rpmbuild/RPMS/x86_64/bedtools2-2.31.0-1.el7.bioit.x86_64.rpm

Now you can move it to /opt/bioit/repo/RPMS

    mv ${HOME}/rpmbuild/RPMS/x86_64/bedtools2-2.31.0-1.el7.bioit.x86_64.rpm \
    /opt/bioit/repo/RPMS

Lastly, run the `buildrepo` command:

    buildrepo

When this finishes, as root you can do the following:

    yum clean all
    yum update bedtools2

That should install the new RPM. If that has worked you can now run the following without loading the module:

    bedtools --version

and it should report the correct version. You're done.
