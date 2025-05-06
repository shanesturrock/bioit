# BioIT Repository

## Introduction

The BioIT packages can be installed by cloning the bioit GitHub repository as follows:

    git clone https://github.com/shanesturrock/bioit.git

If CIS hardened, R packages won't install unless each user has a tmp directory for the package builds to happen inside. Each user neeeds a `${HOME}/.Renviron` file with this inside it (this should be created for each user as they're added but it won't be automatic)::

    TMP=${HOME}/tmp

You should also create that file with `mkdir ~/tmp` for the build user. Other users will need the same.

Run the setup command

### Rocky Linux 8 and 9

Run these two scripts which will create the directories and then build the packages:

    ~/bioit/bin/setup_dirs
    ~/bioit/bin/buildall

Before you can commit changes back from this checkout you need to set up git so it knows who you are:

    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"

Also run the following:

    git config --global push.default simple

If you want to store your credentials do the following:

    git config --global credential.helper store

Now, do a `git pull` and it will ask for your git username and password and these will be saved for future use and you won't be asked for them again.

All the packages are compiled as versions in `/opt/bioit` but by default they're not in the user's path unless they choose them with module load. RPMs have been created that set alternatives up to allow them to be run without calling module load and also allows the system to maintain updates and provide changelogs. To set this up, first make sure that `/opt/bioit` is installed on the machine and the modules are setup as per the Installation page. Once that is done, follow the instructions here to create the repository and then install all packages.

## Checking for new packages

Unfortunately, the uscan package needed for checking updates only works on CentOS 7 and isn't available for Rocky Linux 8 or 9 so the solution is to build an Ubuntu container which will be used instead.

Build the container with this command:

    cd ~/bioit/bin
    export APPTAINER_TMPDIR=`pwd`/tmp
    mkdir $APPTAINER_TMPDIR
    apptainer build --fakeroot ubuntu_uscan.sif ubuntu_uscan.def

The TMPDIR is required on systems with high security such as CIS, regular Linux installs can omit it.

Now you can test the `version_check_modules` with the following:

    version_check_modules -av

This should report all the packages are up to date because it is a newly built system. If you see an update you can build that package using the appropriate build script. The `check_updates` alias will only show the updates needed.

## Testing 

Where possible, tools should have a `tests` directory with a script called `run_test` which will verify that the currently installed version works as expected. To run all tests there is a script in the bin directory called `test_apps` which will work through all tools and execute their test and report whether they pass or fail. An example run will look like this:

    ./test_apps -v -t FastQC
    FastQC: Passed

The script has help (`-h`) and in addition to running individual tests, it can run all (`-a`) of them:

    ./test_apps -va
    FastQC: Passed
    SolexaQA++: Passed
    bamtools: Passed
    bedtools2: Passed
    bowtie: Passed
    bowtie2: Passed
    bwa: Passed
    vcftools: Passed
    picard: Passed
    tophat: Passed
    abyss: Passed
    cutadapt: Passed
    bismark: Passed
    velvet: Passed

## Adding new packages

To add a new package you can reference one of the earlier ones that may be very similar. Create the same directory structure with package name and src, and build as per the others, documenting this on a new page under [Applications](Applications.md) on this site to catch any specifics. You can copy a previous page to use as a template. Once the tool builds and you've created the module file which is tested and works, you should then create a fresh RPM again using a previous template and once that works copy the finished and signed RPM into the `repo/RPM` directory, add it to the `buildrpms` and into the `bioit.xml` file. Finally you can rerun the same `createrepo` process and do a `sudo yum groupinstall bioit` which should see your new package and add it to the system. In the git repo you can also add the new tool, create a `watch` script for `version_check` to run off and also add some tests if available. Don't forget to copy your changes modulefile and edit the `buildrpms` and `setup_bioit` scripts too.

## Next Step

Go to the [Services](Services-Setup.md) page.
