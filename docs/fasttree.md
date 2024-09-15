# FastTree

[http://www.microbesonline.org/fasttree/](http://www.microbesonline.org/fasttree/)

## Automatic Build

Inside `${HOME}/bioit/apps/fasttree/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/fasttree/SPEC/build 2.1.11

When that completes check that the new version is available using:

    module avail fasttree

If that shows as being there you can test it works with:

    module load fasttree/2.1.11
    which fasttree
    fasttree --version
