# IGV

[https://github.com/igvteam/igv](https://github.com/igvteam/igv)

## Automatic Build

Inside `${HOME}/bioit/apps/igv/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/igv/SPEC/build 2.4.7

When that completes check that the new version is available using:

    module avail igv

If that shows as being there you can test it works with:

    module load igv/2.4.7
    which igv

If all is good, you can move to the RPM building step.

## Manual Build

Get the zip file and unzip it in the src directory. Before building this will need to be patched to make the version number show up for users.

Edit the `~/bioit/apps/igv/SPEC/about.properties.patch` file and change the version number and date to suit, then do the following:

    cd igv-2.4.7
    patch -p0 < ~/bioit/apps/igv/SPEC/about.properties.patch 

Set the JAVA variables so the build will use the OracleJDK instead of OpenJDK:

    export JAVA_HOME=/usr/java/latest
    export JRE_HOME=/usr/java/latest/jre
    export PATH=$JAVA_HOME/bin:$PATH

Now you can build the package:

    ant -Dinclude.libs=true

Make an install directory for it and move the built files and libraries in, as well as the launcher script users will execute:

    mkdir /opt/bioit/igv/2.4.7
    mv igv.jar /opt/bioit/igv/2.4.7
    mv lib /opt/bioit/igv/2.4.7
    cp ~/bioit/apps/igv/SPEC/igv /opt/bioit/igv/2.4.7

That should be enough for users to launch this version.

## Module setup

Add a module file in `/opt/bioit/modulefiles/igv/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  igv module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/igv/2.4.7/

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/igv/SPEC` so modify that with the new version details. Once changed, build it with the following commands:

    cp ${HOME}/bioit/apps/igv/SPEC/igv.desktop ${HOME}/rpmbuild/SOURCES
    cp ${HOME}/bioit/apps/igv/SPEC/igv-icons.tar.gz ${HOME}/rpmbuild/SOURCES
    cp ${HOME}/bioit/apps/igv/SPEC/bioinformatics* ${HOME}/rpmbuild/SOURCES
    rpmbuild -bb igv.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
