# LongStitch

[https://github.com/bcgsc/LongStitch](https://github.com/bcgsc/LongStitch)

## Automatic Build

Inside `${HOME}/bioit/apps/longstitch/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/longstitch/SPEC/build 1.0.5

When that completes check that the new version is available using:

    module avail longstitch

If that shows as being there you can test it works with:

    module load longstitch/1.0.5
    which longstitch
    longstitch --version
