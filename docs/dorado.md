# Dorado

[https://github.com/nanoporetech/dorado](https://github.com/nanoporetech/dorado)

## Automatic Build

Inside `${HOME}/bioit/apps/dorado/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/dorado/SPEC/build 1.0.2

When that completes check that the new version is available using:

    module avail dorado

If that shows as being there you can test it works with:

    module load dorado/1.0.2
    which dorado
    dorado --version
