# Installation

## Install a minimal CentOS 7 environment

After a minimal install you should install EPEL, compilers and a GUI since they will be needed for users.

    yum -y install epel-release
    yum -y groupinstall "Development Tools"
    yum -y groupinstall "X Window System"
    yum -y groupinstall "Mate Desktop"
    yum -y install libreoffice
    systemctl set-default graphical.target
    yum -y update
    reboot

The machine should now come back up with a full GUI running. If the machine will only be used remotely then you can use the following instead:

    systemctl set-default multi-user.target

This will prevent the X11 GUI from starting, but later when you install X2go, that will still work fine.

If the machine will mount NFS storage you need to install the following:

    yum -y install nfs-utils

Also, if you're using NFS mounted home directories and you've got selinux enabled you'll need to set the following otherwise key authenticated ssh won't work:

    setsebool -P use_nfs_home_dirs 1

Install `wget` as this makes it much easier to download packages:

    yum -y install wget

You should not install EPEL `R-core or bowtie` on this system so do the following to remove it if it is already installed:

    yum remove R-core

To prevent `R-core or bowtie` being installed from EPEL edit `/etc/yum.repos.d/epel.repo` and add the following line after the `gpgcheck=1` for the `[epel]` section:

    exclude=R-core bowtie

If you try the following you should now get an error that there's no package available:

    yum install R-core

This will mean the `R-core` package from the BioIT repo will be installed once that is added.

## Prevent kernel updates

The machine will need a reboot any time a kernel update is applied. To avoid this add the following line to each section of the `CentOS-Base.repo` file in `/etc/yum.repos.d`:

    exclude=kernel*

If there's a bad kernel issue comment this line out, update the kernel and reboot the machine to apply the update but otherwise this should be fine and will allow the machine to stay up for extended periods.

## Turn off the automatic bug reporting tool

Users can't see the crash reports anyway so remove it using:

    yum -y remove abrt

## Tools required for application support

The following packages are required for building the suite of applications on a fresh BioIT server:

    yum -y install ncurses-devel zlib-devel bzip2-devel xz-devel libcurl-devel openssl-devel environment-modules boost-devel cmake yum-plugin-changelog rpm-build git screen htop root root-tree-viewer root-physics libX11-devel libXt-devel postgresql-devel readline-devel libxml2-devel gsl-devel mariadb-devel java-devel cairo-devel libpng-devel libjpeg-devel mlocate texinfo texinfo-tex tex texlive-* ant boost-devel perl-Test-Base sparsehash-devel openmpi-devel sqlite-devel python-devel python-nose python-pip perl-GD perl-GDGraph parallel gnuplot tcl-devel tk-devel perl-Env perl-Statistics-Descriptive cmake3 emacs-nox perl-Perl4-CoreLibs lapack-devel mpich-devel java-1.6.0-openjdk-devel zeromq-devel ghc cifs-utils python34-pip python34-devel perl-PerlIO-gzip hdf5-devel python-networkx gtk3-devel pigz tkinter python34-tkinter tcsh python-devel python34-devel python34-Cython libtiff-devel tmux pyqt4-devel nano python36-libs python36-devel python36-tkinter python36 python36-setuptools python36-pip python2-matplotlib NLopt-devel libsodium-devel

Defaults tools and changelogs are provided by the meta-RPMS that are built to set alternatives with symlinks into `/usr/bin` so they'll see them as usual. To set this up go to the [BioIT repository](BioIT-repository.md) page, but not just yet.

Lastly, the Oracle JDK is required to build IGV (as of 2.4.1) due to it needing JavaFX. Once built it will run with the standard OpenJDK. To install it download the current release using the following command:

    wget --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u172-b11/a58eab1ec242421181065cdc37240b08/jdk-8u172-linux-x64.rpm

If that doesn't work, go to [this site](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) and download it manually after accepting the license.

Install the downloaded RPM:

    yum install jdk-8u172-linux-x64.rpm

It won't be the default after this but the IGV build script will manually set the `$JAVA_HOME` and `$JAVA_PATH` variables it needs to build IGV using this. The `version_check` script includes a check that the Oracle JDK is the latest version. Update by downloading the newest version when this warns that it is out of date.

## Disable shutdown by normal users

The user's desktop will have a shutdown button and they could in theory close the whole machine down. To stop this, create the following file:

    /etc/polkit-1/rules.d/55-inhibit-shutdown.rules

And paste the following in:

    polkit.addRule(function(action, subject) {
        if ((action.id == "org.freedesktop.consolekit.system.stop" || action.id == "org.freedesktop.consolekit.system.restart") && subject.isInGroup("admin")) {
            return polkit.Result.YES;
        }
        else {
            return polkit.Result.NO;
        }
    });

Now when users log in they won't see the shutdown button and they won't be able to call the shutdown command from the shell either.

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

This should now allow you to install the latest x2go client for your platform and connect to the server via the GUI MATE Desktop environment.

Since users are connecting remotely and assuming there are no local connections, the screensaver should be removed as this gets rid of the lock screen menu item which has caught some users out as we have no passwords:

    yum -y remove mate-screensaver

## Next Step

Go to the [Storage-Setup](Storage-Setup.md) page.
