## Homepage

http://www.bioinformatics.babraham.ac.uk/projects/fastqc/

## Build

Download the Linux zip version to be built into `/opt/biology/FastQC/src` and unzip.

The resulting FastQC directory should be moved to a versioned directory and the `fastqc` command made executable:

    mv FastQC ../0.11.5
    cd ../0.11.5
    chmod 755 fastqc

## Module setup

Add a module file in `/opt/biology/modulefiles/FastQC/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  FastQC module for use with 'environment-modules' package:
    #
    prepend-path  PATH              /opt/biology/FastQC/0.11.5

## RPM

There's a SPEC file for this package in `/opt/biology/FastQC/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb FasqtQC.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.