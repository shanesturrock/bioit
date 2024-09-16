# MAFFT

[https://mafft.cbrc.jp/alignment/software/](https://mafft.cbrc.jp/alignment/software/)

## Automatic Build

Inside `${HOME}/bioit/apps/mafft/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/mafft/SPEC/build 7.525

When that completes check that the new version is available using:

    module avail mafft

If that shows as being there you can test it works with:

    module load mafft/7.525
    which mafft
    mafft --version
