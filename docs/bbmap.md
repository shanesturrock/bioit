# BBMap

[https://sourceforge.net/projects/bbmap/](https://sourceforge.net/projects/bbmap/)

## Build

The `version_check` script will show there's a new version available but it can't download it so you'll need to go to the homepage and get it directly.

Download the version to be built into `/opt/bioit/bedtools2/src` and untar

There's nothing to actually build so just run the following to move the files and correct the permissions:

    mv bbmap ../37.36
    chmod 755 ../37.36
    cd ../37.36
    chmod -R 755 *

## Module setup

Add a module file in `/opt/bioit/modulefiles/bbmap/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bbmap module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/bbmap/37.36

## RPM

There's a SPEC file for this package in `~/bioit/apps/bbmap/SPEC` so modify that with the new version details. The `/opt/bioit/bbmap/37.36/changelog.txt` will give you the details for the `%changelog` section of the SPEC file.

Once changed, build it with the following command:

    rpmbuild -bb bbmap.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
