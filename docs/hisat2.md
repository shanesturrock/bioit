## Homepage

[https://ccb.jhu.edu/software/hisat2/index.shtml](https://ccb.jhu.edu/software/hisat2/index.shtml)

## Build

Download the version to be built into `/opt/bioit/hisat2/src` and unzip. Here we'll use version 2.1.0.

Inside the source run the following:

    make

This just builds in the current location. Since it isn't good to have the binaries in the same location as the source, you first need to move docs, examples and scripts:

    mv scripts /opt/bioit/hisat2/2.1.0/
    mv doc /opt/bioit/hisat2/2.1.0/
    mv example /opt/bioit/hisat2/2.1.0/
    mv hisatgenotype_scripts /opt/bioit/hisat2/2.1.0/
    mv hisatgenotype_modules /opt/bioit/hisat2/2.1.0/

Now you need to move all the binaries and python packages into `/opt/bioit/hisat2/2.1.0/bin` as follows:

    mkdir /opt/bioit/hisat2/2.1.0/bin
    mv hisat2 /opt/bioit/hisat2/2.1.0/bin/
    mv hisat2-* /opt/bioit/hisat2/2.1.0/bin/
    mv *.py /opt/bioit/hisat2/2.1.0/bin/

You also the need to modify the `*genotype*.py` packages to make it look in the location of the libraries it needs. This can be done with the following command:

    cd /opt/bioit/hisat2/2.1.0/bin ; find . -type f -name '*genotype*.py' | \
    xargs sed "/ sys,/a \ 
    sys.path.append('/opt/bioit/hisat2/2.1.0/hisatgenotype_modules')" --in-place

Note that you need to change the version number to match what you're building.

## Module setup

Add a module file in `/opt/bioit/modulefiles/hisat2/` for this version by copying previous ones and modifying the path.

    #%Module 1.0
    #
    #  hisat2 module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/hisat2/2.1.0/bin

## RPM

There's a SPEC file for this package in `~/bioit/apps/hisat2/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb hisat2.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
