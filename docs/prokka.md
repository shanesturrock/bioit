# Prokka

[https://github.com/tseemann/prokka](https://github.com/tseemann/prokka)

## Automatic Build

Inside `${HOME}/bioit/apps/prokka/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/prokka/SPEC/build 1.15.6

When that completes check that the new version is available using:

    module avail prokka

If that shows as being there you can test it works with:

    module load prokka/1.15.6
    which prokka
    prokka --version
