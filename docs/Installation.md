## Install a standard CentOS 7 environment

Once installed and all updates applied, EPEL needs to be installed by running the following:

    yum -y install epel-release

Install `wget` as this makes it much easier to download packages:

    yum -y install wget

## Tools required for application support

Untar the `biology.tgz` file in `/opt` using the following:

    cd /opt
    tar xvf biology.tgz

The `/opt/biology` directory has a number of tools built from source. Run the following command to install the required packages to compile these tools and use them:

    yum -y install ncurses-devel zlib-devel bzip2-devel xz-devel libcurl-devel \ 
    openssl-devel environment-modules boost-devel cmake yum-plugin-changelog \
    rpm-build git screen htop root root-tree-viewer root-physics libX11-devel \
    libXt-devel postgresql-devel readline-devel libxml2-devel gsl-devel \
    mariadb-devel java-devel cairo-devel libpng-devel libjpeg-devel \
    mlocate texinfo texinfo-tex tex texlive-*

Note that there are module files in `/opt/biology/modulefiles` which will set up the environment for users when they need to choose a specific version. To enable this create `/etc/profile.d/biology.sh` with the following line:

    export MODULEPATH=/opt/biology/modulefiles:/usr/share/Modules/modulefiles:/etc/modulefiles

Now all users will be able to see the modules and can select specific versions.

Defaults tools and changelogs are provided by the meta-RPMS that are built to set alternatives with symlinks into `/usr/bin ` so they'll see them as usual. To set this up go to the [BioIT repository](https://github.com/shanesturrock/bioit/wiki/BioIT-repository) page.

## Secure ssh but retain admin access

Create a user account with admin rights:

    adduser shane
    passwd shane
    usermod -aG wheel shane

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