## Introduction

All the packages are compiled as versions in `/opt/bioit` but by default they're not in the user's path unless they choose them with module load. RPMs have been created that set alternatives up to allow them to be run without calling module load and also allows the system to maintain updates and provide changelogs. To set this up, first make sure that `/opt/bioit` is installed on the machine and the modules are setup as per the Installation page. Once that is done, follow the instructions here to create the repository and then install all packages.

## Set up the repository on a new machine

First you need to su to the build user. Before you do this to prevent issues with the gpg signing you should run the following command:

    chmod o+rw $(tty)

Now you can su to the build user and do the following:

    sudo yum -y install createrepo
    sudo cp ~/bioit/repo/bioit.repo /etc/yum.repos.d

Next you need to create a GPG signature to apply to RPMs:

    rm -rf /home/build/.gnupg/
    gpg --gen-key

This will ask for the details of the key. You need to use a real username and e-mail address. I've used my own here but you can use a different one if you like. You also need to give it a passphrase. Helpful tip, if it just skips past without letting you enter the passphrase you didn't do the chmod mentioned as the first step so log out of build and do that, then su back to build.

Once you've created the key you can do the following to verify your keys were created:

    gpg --list-keys

Next you need to export the publibc key to a text file which you can import into RPM. Use the same username here as you used to create the key:

    gpg --export -a 'Shane Sturrock' > RPM-GPG-KEY-BioIT

Check it actually created a key. If the file is empty you didn't use the same username as the key was created with.

Now you can import the key into RPM:

    sudo rpm --import RPM-GPG-KEY-BioIT 

Verify that the key has been imported with the following:

    rpm -q gpg-pubkey --qf '%{name}-%{version}-%{release} --> %{summary}\n'

Lastly, configure the /home/build/.rpmmacros file by opening it in an editor and entering the following changing the gpg_name to suit:

    %_signature gpg
    %_gpg_path /home/build/.gnupg
    %_gpg_name Shane Sturrock
    %_gpgbin /bin/gpg

Now build all the RPMs and sign them with your new key.

    ~/bioit/bin/buildrpms
    mv ~/rpmbuild/RPMS/x86_64/*.rpm /opt/bioit/repo/RPMS
    rpm --addsign /opt/bioit/repo/RPMS/*.rpm

Put in your passphrase to apply the signature. You can check the signature using `rpm --checksig`

    rpm --checksig vcftools-0.1.15-1.el7.bioit.x86_64.rpm 

Now create the repo:

    createrepo -g bioit.xml /opt/bioit/repo

Your repo should now be ready. In future, as you create new RPMs, remember to sign them using `rpm --addsign` before moving them into the RPMS directory.

## Install the packages

    sudo yum clean all
    sudo yum -y groupinstall bioit

As new packages are added to the system, don't forget to add them into the `bioit.xml` file and copy their signed RPMs into the `/opt/bioit/repo/RPMS` directory.

## Keeping it up to date

The uscan watch scripts need the following installed:

    sudo yum -y install dpkg-devel dpkg perl-TimeDate lzma dpkg-perl devscripts \ 
    perl-Crypt-SSLeay perl-LWP-Protocol-https perl-libwww-perl
    sudo yum -y groupinstall "Development"

You can run a version check for all installed packages by running:

    ~/bioit/bin/version_check -avf

This will download any updated source and you can then build the package and RPM as described on the specific tool page under applications.

Once built, put the new RPM into the repo directory and run the `createrepo` command.

    cd /opt/bioit/repo
    createrepo -g bioit.xml /opt/bioit/repo
    sudo yum clean all
    sudo yum groupupdate bioit

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
    tophat: Passed
    vcftools: Passed
    picard: Passed

## Adding new packages

To add a new package you can reference one of the earlier ones that may be very similar. Create the same directory structure with package name and src, and build as per the others, documenting this on a new page under [Applications](https://github.com/shanesturrock/bioit/wiki/Applications) on this site to catch any specifics. You can copy a previous page to use as a template. Once the tool builds and you've created the module file which is tested and works, you should then create a fresh RPM again using a previous template and once that works copy the finished and signed RPM into the `repo/RPM` directory, add it to the `buildrpms` and into the `bioit.xml` file. Finally you can rerun the same `createrepo` process and do a `sudo yum groupinstall bioit` which should see your new package and add it to the system. In the git repo you can also add the new tool, create a `watch` script for `version_check` to run off and also add some tests if available. Don't forget to copy your changes modulefile and edit the `buildrpms` and `setup_bioit` scripts too.