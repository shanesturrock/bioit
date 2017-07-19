# Picard

[https://github.com/lh3/bw://github.com/broadinstitute/picard](https://github.com/lh3/bw://github.com/broadinstitute/picard)

## Build

You can't build from the downloaded zip unfortuantely. You have to clone the git repo into `/opt/bioit/picard/src` using the following:

    git clone -b 2.10.3 https://github.com/broadinstitute/picard.git
    mv picard picard-2.10.3

Build the `picard.jar` file by running the following:

    cd picard-2.10.3
    ./gradlew shadowJar

Now make a directory for this jar to go into and move it into there:

    mkdir /opt/bioit/picard/2.10.3

Finally, copy the picard wrapper from inside the SPEC directory of the git repository:

    cp ~/bioit/apps/picard/SPEC/picard /opt/bioit/picard/2.10.3

This wrapper figures out what directory it is in and sets `picard_dir` to that so there's no need to edit it.

Now users will just be able to run `picard` from the command line without all that messing around with calling java -jar.

## Module setup

Add a module file in `/opt/bioit/modulefiles/picard/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  picard module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/picard/2.10.3/

## RPM

There's a SPEC file for this package in `~/bioit/apps/picard/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb picard.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
