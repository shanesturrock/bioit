# SolexaQA++

[http://solexaqa.sourceforge.net](http://solexaqa.sourceforge.net)

## Build

Download the `src.zip` file into `/opt/bioit/bowtie/src` and unzip it.

cd into the unzipped directory and then into `Linux_x64` and type the following to move the prebuilt binary into position and correct the ownerships:

    mkdir /opt/bioit/SolexaQA++/3.1.7.1/
    mv Linux_x64/SolexaQA++ /opt/bioit/SolexaQA++/3.1.7.1/
    cd /opt/bioit/SolexaQA++/3.1.7.1/
    chmod 755 SolexaQA++

## Module setup

Add a module file in `/opt/bioit/modulefiles/SolexaQA++/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  SolexaQA++ module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/SolexaQA++/3.1.7.1

## RPM

There's a SPEC file for this package in `~/bioit/apps/SolexaQA++/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb SolexaQA++.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
