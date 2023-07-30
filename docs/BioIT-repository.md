# BioIT Repository

## Introduction

The BioIT packages can be installed by cloning the bioit GitHub repository as follows:

    git clone https://github.com/shanesturrock/bioit.git

If CIS hardened, R packages won't install unless each user has a tmp directory for the package builds to happen inside. Each user neeeds a `${HOME}/.Renviron` file with this inside it (this should be created for each user as they're added but it won't be automatic)::

    TMP=${HOME}/tmp

You should also create that file with `mkdir ~/tmp` for the build user. Other users will need the same.

Run the setup command

### CentOS 7

This does all the steps including building RPMs

    ~/bioit/bin/setup_bioit

### Rocky Linux 8

For Rocky Linux 8 we aren't doing RPMs any more so run these two which will create the directories and then build the packages:

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

## Checking for new packages (Rocky Linux 8 only)

The `check_updates` alias added to the `.bashrc` during installation won't work until `uscan` is available. Unfortunately, the package including this that works on CentOS 7 isn't available for Rocky Linux 8 so the solution is to build a CentOS 7 container which will be used instead.

Build the container with this command:

    cd ~/bioit/bin
    export APPTAINER_TMPDIR=`pwd`/tmp
    mkdir $APPTAINER_TMPDIR
    apptainer build --fakeroot centos7_uscan.sif centos7_uscan.def

The TMPDIR is required on systems with high security such as CIS, regular Linux installs can omit it.

Now you can test the `version_check_modules` with the following:

    version_check_modules -av

This should report all the packages are up to date because it is a newly built system. If you see an update you can build that package using the appropriate build script. The `check_updates` alias will only show the updates needed.

## Set up the repository on a new machine (Only on CentOS 7 if you want the RPMs, otherwise skip to testing)

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

Lastly, configure the `/home/build/.rpmmacros` file by opening it in an editor and entering the following changing the gpg_name to suit:

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

## Keeping it up to date (CentOS 7 only, could use the container as per Rocky Linux 8 instead)

The uscan watch scripts need the following installed:

    sudo yum -y install dpkg-devel dpkg perl-TimeDate lzma dpkg-perl devscripts \ 
    perl-Crypt-SSLeay perl-LWP-Protocol-https perl-libwww-perl
    sudo yum -y groupinstall "Development"

You can run a version check for all installed packages by running:

    ~/bioit/bin/version_check -av

This will identify any updated source and you can then build the package and RPM as described on the specific tool page under applications.

Once built, put the new RPM into the repo directory and run the `createrepo` command. 

    cd /opt/bioit/repo
    createrepo -g bioit.xml /opt/bioit/repo
    sudo yum clean all
    sudo yum groupupdate bioit

A `buildrepo` alias can be setup to do updates by adding the following to your `.bash_profile`:

    alias buildrepo='cd /opt/bioit/repo ; createrepo . -g bioit.xml --database'

Now when you add new RPMs you can just run the `buildrepo` alias and they will be added to the repository.

## Testing (CentOS 7 and Rocky Linux 8)

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

## Rstudio Server Install

Download the installer:

    wget https://download2.rstudio.org/server/rhel8/x86_64/rstudio-server-rhel-2023.06.1-524-x86_64.rpm

If you're using meta-RPMs ignore the next bit but if only using environment modules you need to specify where R is by doing the following before installing the rstudio server package:

    sudo mkdir /etc/rstudio
    sudo vi /etc/rstudio/rserver.conf

Paste the following into the rserver.conf file you're creating (changing the version of R as necessary):

    # Location of R
    rsession-which-r=/opt/bioit/R-core/4.3.1/bin/R
    # R library path
    rsession-ld-library-path=/opt/bioit/R-core/4.3.1/lib64/R/lib
    # Only listen localhost
    www-address=localhost
    # Connection port
    www-port=8787

Note that this will cause the server to only listen to localhost and port 8787.  You should add the localhost option even if using a vanilla install as the free RStudio Server package doesn't support SSL and we need to use NGINX to provide that.

Install the server:

### CentOS 7

    sudo yum -y install rstudio-server-rhel-2023.06.1-524-x86_64.rpm    

### Rocky Linux 8

    sudo dnf -y install rstudio-server-rhel-2023.06.1-524-x86_64.rpm

If SELinux is enabled, do the following to allow the server to actually work:

    sudo chcon -R -t bin_t /usr/lib/rstudio-server/bin/
    sudo systemctl restart rstudio-server

You should now be able to open the RStudio Server interface by going to `http://localhost:8787` using Firefox inside the X2Go remote desktop.

## JupyterLab Install

Make sure password free sudo is enabled as per the installation page. JupyterLab is installed by running the script in `~/bioit/bin`

    build_jupyterlab 3.6.5

If it fails, you can remove it using:

    destroy_jupyterlab

Once running you can test it from Firefox in X2Go by going to `http://localhost:8080` and you will get an SSL warning but we'll deal with that via NGINX.

If you have SELinux enabled you'll find that you can't log in, or if you can you should log out and log back in again when you should get a failure. Once you've had this, you need to do the following to allow authentication to work:

    sudo setenforce permissive

Now try and log in and it will let you but audit.log will contain the information necessary to allow it to work in enforcing mode. You need to create a module using this:

    sudo grep denied /var/log/audit/audit.log | audit2allow -M jupyter-module
    sudo semodule -i jupyter-module.pp
    sudo setenforce enforcing
    sudo systemctl restart jupyterhub

At this point, SELinux should allow JupyterHub access to authentication and will continue to work.

## NoVNC inside JupyterLab

It might be useful to have a remote desktop solution inside JupyterLab. Assuming the Mate Desktop is already installed as per the installation page and X2Go config, you can do the following to add a launcher inside JupyterHub as the build user:

    sudo dnf -y install tigervnc
    cd /opt/bioit/jupyterlab/3.6.5/jupyterlab_3.6.5/bin/
    ./pip install jupyter-remote-desktop-proxy
    cd /opt/bioit/jupyterlab/anaconda3/2023.07-1/bin
    ./conda install --channel conda-forge --prefix /opt/bioit/jupyterlab/3.6.5/jupyterlab_3.6.5 websockify

Set mate-session instead of xfce-session in this file:

    vi /opt/bioit/jupyterlab/3.6.5/jupyterlab_3.6.5/lib/python3.9/site-packages/jupyter_remote_desktop_proxy/share/xstartup

Restart the JupyterHub service

    sudo systemctl restart jupyterhub

Log in again and there will be a new desktop launcher. Clicking that will open a new tab with a Mate desktop session for the user. 

If you're running selinux you'll need to enable this again with:

    sudo setenforce permissive
    sudo grep denied /var/log/audit/audit.log | audit2allow -M vnc-module
    sudo semodule -i vnc-module.pp
    sudo setenforce enforcing
    sudo systemctl restart jupyterhub

Note: When a user logs ouf of this remote desktop they will need to stop their server in Hub Control otherwise they won't be able to start a new desktop. If they just close the tab, the remote desktop will continue running and they can reconnect with the desktop button in JupyterHub. They also need to make sure they don't open a JupyterHub session inside this desktop and connect to the desktop because that will go into a recursive image. They should also not use this and another desktop session such as X2Go as there will be clashes in the files.

## NGINX config

Install nginx:

    sudo dnf -y install nginx

Edit the `/etc/nginx/nginx.conf` file using the reference provided in `~/bioit/bin`

You need SSL certs, these can be generated like this:

    openssl genrsa -des3 -out private.key 2048
    openssl req -key private.key -new -out server.csr
    openssl x509 -signkey private.key -in server.csr -req -days 365 -out server.crt

If you want the key to last longer, set more than 365 days.

Put the crt and key files inside `/etc/nginx/ssl` and reference them from `nginx.conf`

If you created the key with a passphrase, create `global.pass` inside `/etc/nginx/ssl` and make it only readable by root. Put the passphrase inside this which will allow nginx to decrypt the certs and serve them. Uncomment the relevant line in the `nginx.conf` file.

A DNS entry needs to exist for the aliases used in the conf file so make sure that's done.

Lastly, you need to start nginx:

    sudo systemctl start nginx

If you have SELinux enabled, it will fail to work with a bad gateway message so set SELinux to permissive as we've already seen:

    sudo setenforce permissive
    sudo grep denied /var/log/audit/audit.log | audit2allow -M nginx-module
    sudo semodule -i nginx-module.pp
    sudo setenforce enforcing
    sudo systemctl restart nginx

It should now work and you won't get the warning from JupyterHub about it not being SSL. It should also be accessible from external machines. If you still get the bad gateway message on the new HTTPS connection, redo the SELinux audit step and restart nginx. If it also happens with RStudio Server, do this again until it all works.

If you still can't connect from outside and the firewall is running do the following:

    sudo firewall-cmd --zone=public --permanent --add-service=https
    sudo firewall-cmd --reload

Now any machine on the local network should be able to access the server (assuming the various aliases have been registered in DNS of course.)

## RDP support (Rocky Linux 8)

This is pretty simple, just do the following:

    sudo dnf -y install xrdp
    sudo systemctl enable xrdp
    sudo systemctl start xrdp

To connect, each user needs to have a `.Xclients` file with `mate-session` and `chmod+x` the file.

Allow access through the firewall:

    sudo firewall-cmd --permanent --add-port=3389/tcp
    sudo firewall-cmd --reload

It should now be possible to use MS Remote Desktop to connect to the IP address.

## Nice login banner

Having a nice banner about the machine can be done as follows:

    sudo dnf -y install neofetch figlet
    echo `hostname -s` | figlet > hostname-banner
    echo -e "This server is the property of\nXXXX Ltd.\n\nAll access is monitored." >> hostname-banner
    sudo mv hostname-banner /etc

Edit the crontab as root:

    sudo crontab -e

Paste in this for a non-gpu server:

    */2 * * * * neofetch --config /home/build/bioit/bin/neofetch.conf --ascii /etc/hostname-banner > /etc/motd

Or this for a gpu server:

    */2 * * * * neofetch --config /home/build/bioit/bin/neofetch_gpu.conf --ascii /etc/hostname-banner > /etc/motd

Now when you log in you'll see a nice banner and updated stats on the machine.

## Adding new packages

To add a new package you can reference one of the earlier ones that may be very similar. Create the same directory structure with package name and src, and build as per the others, documenting this on a new page under [Applications](Applications.md) on this site to catch any specifics. You can copy a previous page to use as a template. Once the tool builds and you've created the module file which is tested and works, you should then create a fresh RPM again using a previous template and once that works copy the finished and signed RPM into the `repo/RPM` directory, add it to the `buildrpms` and into the `bioit.xml` file. Finally you can rerun the same `createrepo` process and do a `sudo yum groupinstall bioit` which should see your new package and add it to the system. In the git repo you can also add the new tool, create a `watch` script for `version_check` to run off and also add some tests if available. Don't forget to copy your changes modulefile and edit the `buildrpms` and `setup_bioit` scripts too.

## Next Step

Go to the [Applications](Applications.md) page.
