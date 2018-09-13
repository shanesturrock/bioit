# Cutadapt

[https://github.com/marcelm/cutadapt](https://github.com/marcelm/cutadapt)

## Automatic Build

Inside `${HOME}/bioit/apps/cutadapt/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/cutadapt/SPEC/cutadapt 1.18

When that completes check that the new version is available using:

    module avail cutadapt

If that shows as being there you can test it works with:

    module load cutadapt/1.18
    which cutadapt
    cutadapt --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the source tarball from [here](https://github.com/marcelm/cutadapt/archive/v1.18.tar.gz) into `/opt/bioit/cutadapt/src`, untar it and cd into the resulting directory then run the following:

    cd cutadapt-1.18

You will need to download cython to do the build:

    wget https://github.com/cython/cython/archive/0.26.tar.gz
    tar xvf 0.26.tar.gz

To use cython you need to modify the PYTHONPATH and PATH variables:

    export PYTHONPATH=/opt/bioit/cutadapt/src/cutadapt-1.18/cython-0.26
    export PATH=/opt/bioit/cutadapt/src/cutadapt-1.18/cython-0.26/bin:$PATH

Now build it:

    python setup.py build_ext -i
    python setup.py build
    # This next bit is needed to allow for a check that it exists
    mkdir -p /opt/bioit/cutadapt/1.18/lib64/python2.7/site-packages/
    export PYTHONPATH=/opt/bioit/cutadapt/1.18/lib64/python2.7/site-packages/:
    $PYTHONPATH
    python setup.py install --prefix=/opt/bioit/cutadapt/1.18

Copy script that sets PYTHONPATH for users and then runs cutadapt:

    cp ${HOME}/bioit/apps/cutadapt/SPEC/cutadapt /opt/bioit/cutadapt/1.18/cutadapt

That should be it.

## Module setup

Add a module file in `/opt/bioit/modulefiles/cutadapt/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  cutadapt module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/cutadapt/1.18

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/cutadapt/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb cutadapt.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
