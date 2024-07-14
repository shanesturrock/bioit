# PICRUSt2

[https://github.com/picrust/picrust2](https://github.com/picrust/picrust2)

## Automatic Build

Inside `${HOME}/bioit/apps/picrust2/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows:

    ${HOME}/bioit/apps/picrust2/SPEC/build 2.5.2

When that completes check that the new version is available using:

    module avail picrust2

If that shows as being there you can test it works with:

    module load picrust2/2.5.2
    which picrust2_pipeline.py
    picrust2_pipeline.py --version
