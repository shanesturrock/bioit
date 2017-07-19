## Homepage

[http://www.r-project.org/](http://www.r-project.org/)

## Before installation

You should not install EPEL `R-core` on this system so do the following to remove it if it is already installed:

    yum remove R-core

To prevent `R-core` being installed from EPEL edit `/etc/yum.repos.d/epel.repo` and add the following line after the `gpgcheck=1` for the `[epel]` section:

    exclude=R-core

If you try the following you should now get an error that there's no package available:

    yum install R-core

This will mean the `R-core` package from the BioIT repo will be installed once that is added.

## Build

Download the version to be built into `/opt/bioit/R-core/src` and untar

    ./configure --prefix=/opt/bioit/R-core/3.4.1 --enable-R-shlib --with-x \ 
    --with-libpng --with-jpeglib --with-cairo

There will be an warning message about `inconsolata.sty` not being found but this just isn't available on CentOS 7 so can't be helped.

    make clean
    make
    make check
    make install

## Install BioConductor etc

Now you have an installation of this build, you need to install the bioconductor and related packages for the users so they don't have to install all that themselves. A script called `bioC_install.R` is in `/opt/bioit/R-core/src` so do the following to start your new R build so you can run this script:

    cd /opt/bioit/R-core/3.4.1/bin
    ./R

Once R starts type the following:

    source("/root/bioit/apps/R-core/SPEC/bioC_install.R") 

It will then ask for a mirror and then should automatically go through and install all the packages the team requires.

Lastly, run `biocValid()` and it will probably complain about a bunch of newer packages and how to downgrade them to the current stable versions. Do that. When it completes just type `q()` to quit and don't save the workspace image.

## Module setup

Add a module file in `/opt/bioit/modulefiles/R/` for this version by copying previous ones and modifying the paths. Note this isn't called `R-core`, just `R`.

    #%Module 1.0
    #
    #  R-core module for use with 'environment-modules' package:
    #
    prepend-path  PATH         /opt/bioit/R-core/3.4.1/bin

## RPM

There's a SPEC file for this package in `~/bioit/apps/R-core/SPEC` so modify that with the new version details. Once changed, build it with the following command:

    rpmbuild -bb R-core.spec

This will create an installable RPM file which you can find in `~/rpmbuild/RPMS/x86_64` and just install that. It checks that the installation directory exists and will fail if it isn't there.

## Rstudio

With R installed you can now install Rstudio:

    wget https://download1.rstudio.org/rstudio-1.0.143-x86_64.rpm
    yum -y install ./rstudio-1.0.143-x86_64.rpm

## Updates

Check weekly for updates for the R packages already installed by starting the correct version of R as root and running the following which list updates (using BioConductor rather than just `update.packages()` because often new packages come out which are not compatible with BioConductor):

    source("http://www.bioconductor.org/biocLite.R")
    biocValid()

To update, just run:

    source("http://www.bioconductor.org/biocLite.R")
    biocLite()

Sometimes you'll get a failure like this:

    installation of package ‘RJDBC’ had non-zero exit status

The solution is to exit R, and run this:

    R CMD javareconf

Then start R again and redo the update.

Sometimes package updates fail because of a lock file such as:

    /opt/bioit/R-core/3.4.1/lib64/R/library/00LOCK-RMySQL/

Deleting that should allow you to complete an update.
