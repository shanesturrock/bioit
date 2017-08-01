# SOAPdenovo2

[http://soap.genomics.org.cn/soapdenovo.html](http://soap.genomics.org.cn/soapdenovo.html)

## Automatic Build

Inside `${HOME}/bioit/apps/SOAPdenovo2/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/SOAPdenovo2/SPEC/build 241

When that completes check that the new version is available using:

    module avail SOAPdenovo2

If that shows as being there you can test it works with:

    module load SOAPdenovo2/241
    which SOAPdenovo-63mer
    SOAPdenovo-63mer --version

Note this reports a different version (2.04 in this case) but that's expected.

If all is good, you can move to the RPM building step.

## Manual Build

Download the `tar.gz` file into `/opt/bioit/SOAPdenovo2/src` and untar it.

Build is simple, just `make` and then `mv` the resulting `SOAPdenovo-*` binaries into place:

    make
    mkdir /opt/bioit/SOAPdenovo2/241/
    mv SOAPdenovo-* /opt/bioit/SOAPdenovo2/241/

## Module setup

Add a module file in `/opt/bioit/modulefiles/SOAPdenovo2/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  SOAPdenovo2 module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/SOAPdenovo2/241

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/SOAPdenovo2/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb SOAPdenovo2.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
