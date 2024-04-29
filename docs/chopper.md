# Chopper

[https://github.com/wdecoster/chopper](https://github.com/wdecoster/chopper)

## Automatic Build

Inside `${HOME}/bioit/apps/chopper/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/chopper/SPEC/build 0.8.0

When that completes check that the new version is available using:

    module avail chopper

If that shows as being there you can test it works with:

    module load chopper/0.8.0
    which chopper
    chopper --version
