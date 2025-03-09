# Busco

[https://busco.ezlab.org/](https://busco.ezlab.org/)

## Automatic Build

Inside `${HOME}/bioit/apps/busco/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/busco/SPEC/build 5.8.3

When that completes check that the new version is available using:

    module avail busco

If that shows as being there you can test it works with:

    module load busco/5.8.3
    which busco
    busco --version
