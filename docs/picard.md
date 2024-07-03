# Picard

[https://github.com/broadinstitute/picard](https://github.com/broadinstitute/picard)

## Automatic Build

Inside `${HOME}/bioit/apps/picard/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/picard/SPEC/build 3.2.0

When that completes check that the new version is available using:

    module avail picard

If that shows as being there you can test it works with:

    module load picard/3.2.0
    which picard
    picard SortVcf --version

If all is good, you can move to the RPM building step.

## Manual Build

From version 3.2.0, picard requires Java 17 so do the following before trying to build picard itself:

    cd /opt/bioit
    wget https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138 ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz
    tar xvf openjdk-17.0.2_linux-x64_bin.tar.gz
    rm openjdk-17.0.2_linux-x64_bin.tar.gz

Once you've got Java you need to set these two variables before doing the clone:

    export JAVA_HOME=/opt/bioit/jdk-17.0.2
    export PATH=$PATH:$JAVA_HOME/bin

Now you have to clone the git repo into `/opt/bioit/picard/src` using the following:

    cd /opt/bioit/picard/src
    git clone -b 3.2.0 https://github.com/broadinstitute/picard.git
    mv picard picard-3.2.0

Build the `picard.jar` file by running the following:

    cd picard-3.2.0
    ./gradlew shadowJar

Now make a directory for the jar to go into and move it into there:

    mkdir /opt/bioit/picard/3.2.0
    mv build/libs/picard.jar /opt/bioit/picard/3.2.0

Finally, copy the picard wrapper from inside the SPEC directory of the git repository:

    cp ~/bioit/apps/picard/SPEC/picard /opt/bioit/picard/3.2.0

This wrapper figures out what directory it is in and sets `picard_dir` to that so there's no need to edit it.

Now users will just be able to run `picard` from the command line without all that messing around with calling java -jar.

## Module setup

Add a module file in `/opt/bioit/modulefiles/picard/` for this version by copying previous ones and modifying the paths.

    #%Module 1.0
    #
    #  picard module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/picard/3.2.0/

## RPM

There's a SPEC file for this package in `${HOME}/bioit/apps/picard/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb picard.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.
