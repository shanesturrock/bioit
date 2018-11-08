# Abyss

[https://github.com/bcgsc/abyss](https://github.com/bcgsc/abyss)

## Automatic Build

Inside `${HOME}/bioit/apps/abyss/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/abyss/SPEC/build 2.1.3

When that completes check that the new version is available using:

    module avail abyss

If that shows as being there you can test it works with:

    module load abyss/2.1.3
    which ABYSS
    ABYSS --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the source tarball from [here](https://github.com/bcgsc/abyss/releases/download/2.1.3/abyss-2.1.3.tar.gz) into `/opt/bioit/abyss/src`, untar it and cd into the resulting directory then run the following:

    cd abyss-2.1.3

You will need to download a specific version of boost using the following:

    wget http://sourceforge.net/projects/boost/files/boost/1.56.0/boost_1_56_0.tar.bz2
    tar xvf boost_1_56_0.tar.bz2

Now configure and build:

    ./configure --prefix=/opt/bioit/abyss/2.1.3
    make clean
    make
    make install

There is also an issue using multi-processor support if the `ABYSS-P` executable is missing but this can be fixed with a simple symlink:

    cd /opt/bioit/abyss/2.1.3/bin
    ln -sf ABYSS ABYSS-P

That should be it.

## Module setup

Add a module file in `/opt/bioit/modulefiles/abyss/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  abyss module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/abyss/2.1.3/bin
    prepend-path  MANPATH      /opt/bioit/abyss/2.1.3/share/man/man1

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/abyss/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb abyss.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
