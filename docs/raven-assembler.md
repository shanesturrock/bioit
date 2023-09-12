# Raven Assembler

[https://github.com/lbcb-sci/raven](https://github.com/lbcb-sci/raven)

## Automatic Build

Inside `${HOME}/bioit/apps/raven-assembler/SPEC` there is a script called `build`. This just requires the version number and will download, compile, in stall and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/raven-assembler/SPEC/build 1.8.3

When that completes check that the new version is available using:

    module avail raven-assembler

If that shows as being there you can test it works with:

    module load raven-assembler/1.8.3
    which raven
    raven --version
