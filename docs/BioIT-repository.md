## Introduction

All the packages are compiled as versions in `/opt/biology` but by default they're not in the user's path unless they choose them with module load. RPMs have been created that set alternatives up to allow them to be run without calling module load and also allows the system to maintain updates and provide changelogs. To set this up, first make sure that `/opt/biology` is installed on the machine and the modules are setup as per the Installation page. Once that is done, follow the instructions here to create the repository and then install all packages.

## Set up the repository on a new machine

    yum -y install createrepo
    cp /opt/biology/bioitrepo/bioit.repo /etc/yum.repos.d
    cd /opt/biology/bioitrepo
    sh ./buildall.sh
    mv ~/rpmbuild/RPMS/x86_64/*.rpm /opt/biology/bioitrepo/RPMS
    createrepo -g bioit.xml /opt/biology/bioitrepo

## Install the packages

    yum clean all
    yum -y groupinstall bioit

As new packages are added to the system, don't forget to add them into the `bioit.xml` file and copy their completed RPMs into the `/opt/biology/bioitrepo/RPMS` directory.

## Keeping it up to date

The uscan watch scripts need the following installed:

    yum -y install dpkg-devel dpkg perl-TimeDate lzma dpkg-perl devscripts \ 
    perl-Crypt-SSLeay perl-LWP-Protocol-https perl-libwww-perl
    yum -y groupinstall "Development"

You can run a version check for all installed packages by running:

    ~/bioit/bin/version_check -avf

This will download any updated source and you can then build the package and RPM as described on the specific tool page under applications.

Once built, put the new RPM into the bioitrepo directory and run the `createrepo` command.

    cd /opt/biology/bioitrepo
    createrepo -g bioit.xml /opt/biology/bioitrepo
    yum clean all
    yum groupupdate bioit

## Adding new packages

To add a new package you can reference one of the earlier ones that may be very similar. Create the same directory structure with package name and src, and build as per the others, documenting this on a new page under [Applications](https://github.com/shanesturrock/bioit/wiki/Applications) on this site to catch any specifics. You can copy a previous page to use as a template. Once the tool builds and you've created the module file which is tested and works, you should then create a fresh RPM again using a previous template and once that works copy the finished RPM into the `bioitrepo/RPM` directory, add it to the `buildall.sh` and into the `bioit.xml` file. Finally you can rerun the same `createrepo` process and do a `yum groupupdate bioit` which should see your new package and add it to the system. In the git repo you can also add the new tool, create a `watch` script for `version_check` to run off and also add some tests if available.