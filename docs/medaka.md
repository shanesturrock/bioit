# Medaka

[https://github.com/nanoporetech/medaka](https://github.com/nanoporetech/medaka)

## Automatic Build

Inside `${HOME}/bioit/apps/medaka/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/medaka/SPEC/build 1.12.1

When that completes check that the new version is available using:

    module avail medaka

If that shows as being there you can test it works with:

    module load medaka/1.12.1
    which medaka
    medaka --version
