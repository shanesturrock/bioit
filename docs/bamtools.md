# Bamtools

[https://github.com/pezmaster31/bamtools](https://github.com/pezmaster31/bamtools)

## Build

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

There's a SPEC file for this package in `~/bioit/apps/bamtools/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bamtools.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
