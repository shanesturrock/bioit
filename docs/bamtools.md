# Bamtools

[https://github.com/pezmaster31/bamtools](https://github.com/pezmaster31/bamtools)

## Automatic Build

Download the `v2.4.1.tar.gz` file to be built into `/opt/bioit/bamtools/src`.

Inside `bioit/apps/bamtools/SPEC` there is a script called `build`. This just requires the version number and will do the compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/bamtools/SPEC/build 2.4.1

When that completes check that the new version is available using:

    module avail bamtools

If that shows as being there you can test it works with:

    module load bamtools/2.4.1
    which bamtools
    bamtools --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the `tar.gz` version to be built into `/opt/bioit/bamtools/src` and untar.

Inside the resulting directory run the following:

    mkdir build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/opt/bioit/bamtools/2.4.1 ..
    make all
    make install

Go into the installation directory (`/opt/bioit/bamtools/2.4.1`) and copy the launcher from `~/bioit/apps/bamtools/SPEC/bamtools` into it (not into the `bin` directory. This will sort out the location and execute bamtools with the usual options.

    cp ${HOME}/bioit/apps/bamtools/SPEC/bamtools /opt/bioit/bamtools/2.4.1/

## Module setup

Add a module file in `/opt/bioit/modulefiles/bamtools/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bamtools module for use with 'environment-modules' package:
    #
    prepend-path  PATH              /opt/bioit/bamtools/2.4.1

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/bamtools/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bamtools.spec

This will create an RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64`. It checks that the installation directory exists and will fail if it isn't there.

Before you install this, you need to sign it using:

    rpm --addsign \
    ${HOME}/rpmbuild/RPMS/x86_64/bamtools-2.4.1-1.el7.bioit.x86_64.rpm

Now you can move it to /opt/bioit/repo/RPMS

    mv ${HOME}/rpmbuild/RPMS/x86_64/bamtools-2.4.1-1.el7.bioit.x86_64.rpm \
    /opt/bioit/repo/RPMS

lastly, run the buildrepo command:

    buildrepo

When this finish, as root you can do the following:

    yum clean all
    yum update bamtools

That should install the new RPM. If that has worked you can now run the following without loading the module:

    bamtools --version

and it should report the correct version. You're done.
