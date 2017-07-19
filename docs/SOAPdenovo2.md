## Homepage

http://soap.genomics.org.cn/soapdenovo.html

## Build

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

There's a SPEC file for this package in `~/bioit/apps/SOAPdenovo2/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb SOAPdenovo2.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
