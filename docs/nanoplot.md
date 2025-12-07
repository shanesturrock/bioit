# NanoPlot

[https://github.com/wdecoster/NanoPlot](https://github.com/wdecoster/NanoPlot)

## Automatic Build

Inside `${HOME}/bioit/apps/nanoplot/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/nanoplot/SPEC/build 1.46.2

When that completes check that the new version is available using:

    module avail nanoplot

If that shows as being there you can test it works with:

    module load nanoplot/1.46.2
    which NanoPlot
    NanoPlot --version
