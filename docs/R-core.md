# R-core

[http://www.r-project.org/](http://www.r-project.org/)

## Automatic Build

Before starting to build R you must be sure you've used `ssh -Y` to get in because it will fail without X11 support. Alternatively, run the build in X2Go.

Also, you need to have the following installed from source if you haven't already:

    gdal-2.4.3
    geos-3.6.5

Download them, untar, run `./configure` and `make` and `sudo install` in `/usr/local` (the default location) plus you'll also need to run this as root:

    echo "/usr/local/lib" >> /etc/ld.so.conf.d/local.conf
    ldconfig

That should be all that is required to get tools like `sf` to compile.

Inside `${HOME}/bioit/apps/R-core/SPEC` there is a script called `build`. This just requires the version number and will download, compile, install and create the modulefile for you. Execute it as follows: 

    ${HOME}/bioit/apps/R-core/SPEC/build 4.3.2

This will take a long time because it also installs the BioConductor packages into the new R installation. When that completes check that the new version is available using:

    module avail R-core

If that shows as being there you can test it works with:

    module load R/4.3.2
    which R

If all is good, you can move to the RPM building step.

## Manual Build

Download the version to be built into `/opt/bioit/R-core/src` and untar

    ./configure --prefix=/opt/bioit/R-core/4.3.2 --enable-R-shlib --with-x \ 
    --with-libpng --with-jpeglib --with-cairo --with-libtiff \
    --with-blas --with-lapack --enable-memory-profiling --with-pcre1

There will be an warning message about `inconsolata.sty` not being found but this just isn't available on CentOS 7 so can't be helped.

    make clean
    make
    make check
    make install

## Install BioConductor etc

Now you have an installation of this build, you need to install the bioconductor and related packages for the users so they don't have to install all that themselves. A script called `bioC_install.R` is in `/opt/bioit/R-core/src` so do the following to start your new R build so you can run this script:

    cd /opt/bioit/R-core/4.3.2/bin
    ./R

Once R starts type the following:

    source("/root/bioit/apps/R-core/SPEC/bioC_install.R") 

It will automatically go through and install all the packages the team requires. Some of the packages require X support to install so you must use -Y to the build machine.

Lastly, run `biocValid()` and it will probably complain about a bunch of newer packages and how to downgrade them to the current stable versions. Do that. When it completes just type `q()` to quit and don't save the workspace image.

## Module setup

Add a module file in `/opt/bioit/modulefiles/R/` for this version by copying previous ones and modifying the paths. Note this isn't called `R-core`, just `R`.

    #%Module 1.0
    #
    #  R-core module for use with 'environment-modules' package:
    #
    prepend-path  PATH             /opt/bioit/R-core/4.3.2/bin
    prepend-path  MANPATH          /opt/bioit/R-core/4.3.2/share/man
    prepend-path  LD_LIBRARY_PATH  /opt/bioit/R-core/4.3.2/lib64/R/lib

There's a SPEC file for this package in `${HOME}/bioit/apps/R-core/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb R-core.spec

This will create an installable RPM file which you can find in `${HOME}/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.

## Updates

Check weekly for updates for the R packages already installed by starting the correct version of R as root and running the following which list updates (using BioConductor rather than just `update.packages()` because often new packages come out which are not compatible with BioConductor):

    BiocManager::valid()$out_of_date

To update, just run:

    BiocManager::install()

Sometimes you'll get a failure like this:

    installation of package ‘RJDBC’ had non-zero exit status

The solution is to exit R, and run this:

    R CMD javareconf

Then start R again and redo the update.

Sometimes package updates fail because of a lock file such as:

    /opt/bioit/R-core/4.3.2/lib64/R/library/00LOCK-RMySQL/

Deleting that should allow you to complete an update.
