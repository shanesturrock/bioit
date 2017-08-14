# Installation

## Install a standard CentOS 7 environment

Once installed and all updates applied, EPEL needs to be installed by running the following:

    yum -y install epel-release

Install `wget` as this makes it much easier to download packages:

    yum -y install wget

You should not install EPEL `R-core` on this system so do the following to remove it if it is already installed:

    yum remove R-core

To prevent `R-core` being installed from EPEL edit `/etc/yum.repos.d/epel.repo` and add the following line after the `gpgcheck=1` for the `[epel]` section:

    exclude=R-core

If you try the following you should now get an error that there's no package available:

    yum install R-core

This will mean the `R-core` package from the BioIT repo will be installed once that is added.

## Tools required for application support

Untar the `bioit.tgz` file in `/opt` using the following:

    cd /opt
    tar xvf bioit.tgz

The `/opt/bioit` directory has a number of tools built from source. Run the following command to install the required packages to compile these tools and use them:

    yum -y install ncurses-devel zlib-devel bzip2-devel xz-devel libcurl-devel openssl-devel environment-modules boost-devel cmake yum-plugin-changelog rpm-build git screen htop root root-tree-viewer root-physics libX11-devel libXt-devel postgresql-devel readline-devel libxml2-devel gsl-devel mariadb-devel java-devel cairo-devel libpng-devel libjpeg-devel mlocate texinfo texinfo-tex tex texlive-* ant boost-devel perl-Test-Base sparsehash-devel openmpi-devel sqlite-devel

Note that there are module files in `/opt/bioit/modulefiles` which will set up the environment for users when they need to choose a specific version. To enable this create `/etc/profile.d/bioit.sh` with the following line:

    export MODULEPATH=/opt/bioit/modulefiles:/usr/share/Modules/modulefiles:/etc/modulefiles

Now all users will be able to see the modules and can select specific versions.

Defaults tools and changelogs are provided by the meta-RPMS that are built to set alternatives with symlinks into `/usr/bin ` so they'll see them as usual. To set this up go to the [BioIT repository](BioIT-repository.md) page, but not just yet.

## Secure ssh but retain admin access

Create a build user account with admin rights which will be used to do tool updates:

    adduser build
    passwd build
    usermod -aG wheel build

Since this user will be used for the BioIT repo, change the permissions on the home directory from the default 700 to 755 using the following:

    chmod 755 /home/build

Also, add the following to the build user's `.bashrc` file to make building tools nicer:

    alias buildrepo="cd /opt/bioit/repo ; createrepo . -g bioit.xml --database"
    alias cleanbuild="rm -rf /home/build/rpmbuild/SPECS/* \
      /home/build/rpmbuild/SRPMS/* /home/build/rpmbuild/SOURCES/* \
      /home/build/rpmbuild/RPMS/*"
    export PATH=/home/build/bioit/bin:$PATH

The `buildrepo` alias will be used to add new packages and updates. The `cleanbuild` alias is for emptying out the rpmbuild directory, and the `$PATH` variable has the bioit gitrepo `bin` directory added so you can use the various tools that are in there.

This user can now use sudo allowing us to disable root ssh logins but make sure you can ssh into this account before you do so. This means creating the `.ssh` directory and inside that the authorized_keys file which you'll paste the public key for the machine you're logging in from (make sure it is all on a single line) and `chmod 600 authorized_keys` otherwise ssh won't use it. Also `chmod 700 ~/.ssh` for the same reason.

Once that user can log in and also sudo works for it, go ahead and make the following changes to the sshd_config:

    PermitRootLogin No
    MaxAuthTries 3
    ClientAliveInterval 120
    ClientAliveCountMax 2
    UseDNS no

Then restart the ssh daemon.

    systemctl restart sshd.service

## Setup automatic updates

    yum -y install yum-cron

edit `/etc/yum/yum-cron.conf` adding the following:

    update_cmd = security
    apply_updates = yes

Enable and start the service

    systemctl enable yum-cron.service
    systemctl start yum-cron.service

## Install remote desktop

    yum -y install x2goserver-xsession
    yum -y groupinstall "Xfce"
    yum -y install firefox libreoffice
    yum -y groupinstall "MATE Desktop"

This should now allow you to install the latest x2go client for your platform and connect to the server via the GUI with the choice of XFCE or MATE Desktop environments.

## Next Step

Go to the [Storage-Setup](Storage-Setup.md) page.
