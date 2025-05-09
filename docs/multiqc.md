# multiqc

[https://github.com/MultiQC/MultiQC](https://github.com/MultiQC/MultiQC)

## Automatic Build

Inside `${HOME}/bioit/apps/multiqc/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/multiqc/SPEC/build 1.28

When that completes check that the new version is available using:

    module avail multiqc

If that shows as being there you can test it works with:

    module load multiqc/1.28
    which multiqc
    multiqc --version
