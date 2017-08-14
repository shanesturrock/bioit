# Augustus

[http://bioinf.uni-greifswald.de/augustus/](http://bioinf.uni-greifswald.de/augustus/)

## Automatic Build

Inside `${HOME}/bioit/apps/augustus/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/augustus/SPEC/build 3.3

When that completes check that the new version is available using:

    module avail augustus

If that shows as being there you can test it works with:

    module load augustus/3.3
    which augustus
    augusutus

If all is good, you can move to the RPM building step.

## Manual Build

Download the binary tarball from [here](http://bioinf.uni-greifswald.de/augustus/binaries/augustus-3.3.tar.gz) into `/opt/bioit/augustus/src`, untar it and cd into the resulting directory then run the following:

    mv augustus augustus-3.3
    cd augustus-3.3
    make clean

The binaries supplied with this won't run so you need to recompile from source. This requires bamtools as a dependency and rather than run the version already installed it is better to include the dependency inside this package separately.

    wget https://github.com/pezmaster31/bamtools/archive/v2.4.1.tar.gz
    tar xvf v2.4.1.tar.gz
    cd bamtools-2.4.1
    mkdir build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/opt/bioit/augustus/src/augustus-3.3/bamtools ..
    make all
    make install

To use this internal version of bamtools a few files need to be patched as follows:
    cd /opt/bioit/augustus/src/augustus-3.3
    # patch bam2hints Makefile
    sed "s+INCLUDES = /usr/include/bamtools+INCLUDES = /opt/bioit/augustus/src/augustus-3.3/bamtools/include/bamtools+" --in-place auxprogs/bam2hints/Makefile
    sed "s+LIBS = -lbamtools -lz+LIBS = /opt/bioit/augustus/src/augustus-3.3/bamtools/lib/bamtools/libbamtools.a -lz+" --in-place auxprogs/bam2hints/Makefile
    # patch filterBam Makefile
    sed "s+BAMTOOLS = /usr/include/bamtools+BAMTOOLS = /opt/bioit/augustus/src/augustus-3.3/bamtools+" --in-place auxprogs/filterBam/src/Makefile
    sed "s+INCLUDES = -I\$(BAMTOOLS) -Iheaders -I./bamtools+INCLUDES = -I\$(BAMTOOLS)/include/bamtools -Iheaders -I./bamtools+" --in-place auxprogs/filterBam/src/Makefile
    sed "s+LIBS = -lbamtools -lz+LIBS = \$(BAMTOOLS)/lib/bamtools/libbamtools.a -lz+" --in-place auxprogs/filterBam/src/Makefile
    # patch Makefile to set install directory
    sed "s+INSTALLDIR = /opt/augustus-\$(AUGVERSION)+INSTALLDIR = /opt/bioit/augustus/${VERSION}+" --in-place Makefile
    # Remove symlinks lines to avoid permission denied error
    sed '/ln /d' --in-place Makefile

Now build augustus

    make
    make install

Lastly, the permissions on the install need to be fixed otherwise users will get a permission denied error when trying to use it:

find /opt/bioit/augustus/3.3 -type d -exec chmod a+rx {} +
find /opt/bioit/augustus/3.3 -type f -exec chmod a+r {} +

## Module setup

Add a module file in `/opt/bioit/modulefiles/augustus/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  augustus module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/augustus/3.3/

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/augustus/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb augustus.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
