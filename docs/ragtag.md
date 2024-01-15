# RagTag

[https://github.com/malonge/RagTag](https://github.com/malonge/RagTag)

## Automatic Build

Inside `${HOME}/bioit/apps/ragtag/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/ragtag/SPEC/build 2.1.0

When that completes check that the new version is available using:

    module avail ragtag

If that shows as being there you can test it works with:

    module load ragtag/2.1.0
    which ragtag
    ragtag.py --version
