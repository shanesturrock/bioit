# BBMap

[https://sourceforge.net/projects/bbmap/](https://sourceforge.net/projects/bbmap/)

## Automatic Build

Inside `${HOME}/bioit/apps/bbmap/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the module file for you. Execute it as follows:

    ${HOME}/bioit/apps/bbmap/SPEC/build 37.66

When that completes check that the new version is available using:

    module avail bbmap

If that shows as being there you can test it works with:

    module load bbmap/37.66
    which bbduk.sh
    bbduk.sh --version

If all is good, you can move to the RPM building step.

## Manual Build

The `version_check` script will show there's a new version available but it can't download it so you'll need to go to the homepage and get it directly.

Download the version to be built into `/opt/bioit/bbmap/src` and untar

There's nothing to actually build so just run the following to move the files and correct the permissions:

    mv bbmap ../37.66
    chmod 755 ../37.66
    cd ../37.66
    chmod -R 755 *

## Module setup

Add a module file in `/opt/bioit/modulefiles/bbmap/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  bbmap module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/bbmap/37.66

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/bbmap/SPEC` so modify that with the new version details. The `/opt/bioit/bbmap/37.66/doc/changelog.txt` will give you the details for the `%changelog` section of the SPEC file.

Once changed, build it with the following command:

    rpmbuild -bb bbmap.spec

This will create an RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_66
`. It checks that the installation directory exists and will fail if it isn't th
ere.

Before you install this, you need to sign it using:

    rpm --addsign \
    ${HOME}/rpmbuild/RPMS/x86_64/bbmap-37.66-1.el7.bioit.x86_64.rpm

Now you can move it to `/opt/bioit/repo/RPMS`

    mv ${HOME}/rpmbuild/RPMS/x86_64/bbmap-37.66-1.el7.bioit.x86_64.rpm \
    /opt/bioit/repo/RPMS

Lastly, run the `buildrepo` command:

    buildrepo

When this finishes, as root you can do the following:

    yum clean all
    yum update bbmap

That should install the new RPM. If that has worked you can now run the followin
g without loading the module:

    bbduk.sh --version

and it should report the correct version. You're done.
