## Homepage

https://github.com/pezmaster31/bamtools

## Build

Download the `tar.gz` version to be built into `/opt/biology/bamtools/src` and untar.

Inside the resulting directory run the following:

    mkdir build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/opt/biology/bamtools/2.4.1 ..
    make all
    make install

Go into the installation directory (`/opt/biology/bamtools/2.4.1/bin`) and remove the bamtools symlink. You need to create a launcher script which sets the library path.

    #!/bin/bash
    export LD_LIBRARY_PATH=/opt/biology/bamtools/2.4.1/lib/bamtools
    exec /opt/biology/bamtools/2.4.1/bin/bamtools-2.4.1 "$@"

Call this `bamtools` and then when the user calls bamtools, this script will set the library path and then call the bamtools versioned binary with the command line options passed through.

## Module setup

Add a module file in `/opt/biology/modulefiles/bamtools/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bamtools module for use with 'environment-modules' package:
    #
    prepend-path  PATH              /opt/biology/bamtools/2.4.1/bin

## RPM

There's a SPEC file for this package in `/opt/biology/bamtools/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb bamtools.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.