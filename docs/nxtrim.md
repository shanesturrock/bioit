# nxtrim

[https://github.com/sequencing/NxTrim](https://github.com/sequencing/NxTrim)

## Automatic Build

Inside `${HOME}/bioit/apps/nxtrim/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/nxtrim/SPEC/build 0.4.3

When that completes check that the new version is available using:

    module avail nxtrim

If that shows as being there you can test it works with:

    module load nxtrim/0.4.3
    which nxtrim
    nxtrim

If all is good, you can move to the RPM building step.

## Manual Build

Download the `tar.gz` version to be built into `/opt/bioit/nxtrim/src` and untar.

Inside the resulting directory run the following:

    make 
    mkdir /opt/bioit/nxtrim/0.4.3
    mv nxtrim /opt/bioit/nxtrim/0.4.3

## Module setup

Add a module file in `/opt/bioit/modulefiles/nxtrim/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  nxtrim module for use with 'environment-modules' package:
    #
    prepend-path  PATH              /opt/bioit/nxtrim/0.4.3

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/nxtrim/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb nxtrim.spec

This will create an RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64`. It checks that the installation directory exists and will fail if it isn't there.

Before you install this, you need to sign it using:

    rpm --addsign \
    ${HOME}/rpmbuild/RPMS/x86_64/nxtrim-0.4.3-1.el7.bioit.x86_64.rpm

Now you can move it to /opt/bioit/repo/RPMS

    mv ${HOME}/rpmbuild/RPMS/x86_64/nxtrim-0.4.3-1.el7.bioit.x86_64.rpm \
    /opt/bioit/repo/RPMS

Lastly, run the `buildrepo` command:

    buildrepo

When this finishes, as root you can do the following:

    yum clean all
    yum update nxtrim

That should install the new RPM. If that has worked you can now run the following without loading the module:

    nxtrim

and it should report the correct version. You're done.
