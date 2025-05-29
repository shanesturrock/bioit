# Cutadapt

[https://github.com/marcelm/cutadapt](https://github.com/marcelm/cutadapt)

## Automatic Build

Inside `${HOME}/bioit/apps/cutadapt/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/cutadapt/SPEC/cutadapt 5.1

When that completes check that the new version is available using:

    module avail cutadapt

If that shows as being there you can test it works with:

    module load cutadapt/5.1
    which cutadapt
    cutadapt --version

If all is good, you can move to the RPM building step.

## Manual Build

Make the directory for the install

    mkdir /opt/bioit/cutadapt/5.1

Create a virtual environment for Python3.9

    python3.9 -m venv /opt/bioit/cutadapt/5.1/venv

Install cutadapt using pip3

    /opt/bioit/cutadapt/5.1/venv/bin/pip3 install --install-option="--install-scripts=/opt/bioit/cutadapt/5.1" cutadapt==5.1

That should be it.

## Module setup

Add a module file in `/opt/bioit/modulefiles/cutadapt/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  cutadapt module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/cutadapt/5.1

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/cutadapt/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb cutadapt.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
