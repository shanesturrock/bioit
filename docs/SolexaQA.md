# SolexaQA++

[http://solexaqa.sourceforge.net](http://solexaqa.sourceforge.net)

## Automatic Build

Inside `${HOME}/bioit/apps/SolexaQA++/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/SolexaQA++/SPEC/build 3.1.7.2

When that completes check that the new version is available using:

    module avail SolexaQA++

If that shows as being there you can test it works with:

    module load SolexaQA++/3.1.7.2
    which SolexaQA++
    SolexaQA++ --version

If all is good, you can move to the RPM building step.

## Manual Build

Download the `src.zip` file into `/opt/bioit/bowtie/src` and unzip it.

cd into the unzipped directory and then into `Linux_x64` and type the following to move the prebuilt binary into position and correct the ownerships:

    mkdir /opt/bioit/SolexaQA++/3.1.7.2/
    mv Linux_x64/SolexaQA++ /opt/bioit/SolexaQA++/3.1.7.2/
    cd /opt/bioit/SolexaQA++/3.1.7.2/
    chmod 755 SolexaQA++

## Module setup

Add a module file in `/opt/bioit/modulefiles/SolexaQA++/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  SolexaQA++ module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/SolexaQA++/3.1.7.2

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/SolexaQA++/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb SolexaQA++.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
