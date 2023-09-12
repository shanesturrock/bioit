# Minimap2

[https://github.com/lh3/minimap2](https://github.com/lh3/minimap2)

## Automatic Build

Inside `${HOME}/bioit/apps/minimap2/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/minimap2/SPEC/build 2.26

When that completes check that the new version is available using:

    module avail minimap2

If that shows as being there you can test it works with:

    module load minimap2/2.26
    which minimap2
    minimap2 --version
