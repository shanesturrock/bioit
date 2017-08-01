# NCBI-BLAST

[https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)

## Automatic Build

Inside `${HOME}/bioit/apps/ncbi-blast/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/ncbi-blast/SPEC/build 2.6.0+

When that completes check that the new version is available using:

    module avail ncbi-blast

If that shows as being there you can test it works with:

    module load ncbi-blast/2.6.0+
    which blastp
    blastp -h

If all is good, you can move to the RPM building step.

## Manual Build

Download the `x64-linux.tar.gz` file into `/opt/bioit/ncbi-blast/src` and untar it. Note you can't build from source without the Intel compiler so just use this which is a binary and also avoid the RPM because this way we can have multiple versions installed.

Move the unpackaged directory as follows:

    mv ncbi-blast-2.6.0+ /opt/bioit/ncbi-blast/2.6.0+

That should do it.

## Module setup

Add a module file in `/opt/bioit/modulefiles/ncbi-blast/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  ncbi-blast module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/ncbi-blast/2.6.0+/bin

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/ncbi-blast/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb ncbi-blast.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
