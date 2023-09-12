# Seqkit

[https://github.com/shenwei356/seqkit/releases](https://github.com/shenwei356/seqkit/releases)

## Automatic Build

Inside `${HOME}/bioit/apps/seqkit/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/seqkit/SPEC/build 2.5.1

When that completes check that the new version is available using:

    module avail seqkit

If that shows as being there you can test it works with:

    module load seqkit/2.5.1
    which seqkit
    seqkit --help
