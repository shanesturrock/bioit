# IGV

[https://github.com/igvteam/igv](https://github.com/igvteam/igv)

## Build

Get the zip file and unzip it in the src directory. Before building this will need to be patched to make the version number show up for users.

Edit the `~/bioit/apps/igv/SPEC/about.properties.patch` file and change the version number and date to suit, then do the following:

    cd igv-2.3.98
    patch -p0 < ~/bioit/apps/igv/SPEC/about.properties.patch 

Now you can build the package:

    ant -Dinclude.libs=true

Make an install directory for it and move the built files and libraries in, as well as the launcher script users will execute:

    mkdir /opt/bioit/igv/2.3.98
    mv igv.jar /opt/bioit/igv/2.3.98
    mv lib /opt/bioit/igv/2.3.98
    cp ~/bioit/apps/igv/SPEC/igv /opt/bioit/igv/2.3.98

That should be enough for users to launch this version.

## Module setup

Add a module file in `/opt/bioit/modulefiles/igv/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  igv module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/igv/2.3.98/

## RPM

There's a SPEC file for this package in `~/bioit/apps/igv/SPEC` so modify that with the new version details. Once changed, build it with the following commands:

    cp ~/bioit/apps/igv/SPEC/igv.desktop ~/rpmbuild/SOURCES
    cp ~/bioit/apps/igv/SPEC/igv.icons.tar.gz ~/rpmbuild/SOURCES
    cp ~/bioit/apps/igv/SPEC/bioinformatics* ~/rpmbuild/SOURCES
    rpmbuild -bb igv.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
