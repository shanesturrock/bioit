# Abyss

[https://github.com/bcgsc/abyss](https://github.com/bcgsc/abyss)

## Automatic Build

Inside `${HOME}/bioit/apps/abyss/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/abyss/SPEC/build 2.3.10

When that completes check that the new version is available using:

    module avail abyss

If that shows as being there you can test it works with:

    module load abyss/2.3.10
    which ABYSS
    ABYSS --version
