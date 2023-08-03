# Installation

## Install a minimal CentOS 7 / Rocky Linux 8 environment

After a minimal install you should install EPEL, compilers and a GUI since they will be needed for users.

### CentOS 7

    yum -y install epel-release
    yum -y groupinstall "Development Tools"
    yum -y groupinstall "X Window System"
    yum -y groupinstall "Mate Desktop"
    yum -y install libreoffice
    systemctl set-default multi-user.target
    yum -y install centos-release-scl
    yum -y install devtoolset-9 sysstat figlet rh-python38-python
    yum -y install devscripts perl-LWP-Protocol-https
    yum -y update
    reboot

### Rocky Linux 8

    dnf -y install epel-release
    /usr/bin/crb enable
    dnf -y groupinstall "Development Tools"
    dnf -y install libreoffice
    systemctl set-default multi-user.target
    dnf -y update
    reboot

X11 GUI won't start, but if you want it to run use this:

    systemctl set-default graphical.target

If the machine will mount NFS storage you need to install the following:

### CentOS 7

    yum -y install nfs-utils

### Rocky Linux 8

    dnf -y install nfs-utils

Also, if you're using NFS mounted home directories and you've got selinux enabled you'll need to set the following otherwise key authenticated ssh won't work:

    setsebool -P use_nfs_home_dirs 1

Install `wget` as this makes it much easier to download packages:

### CentOS 7

    yum -y install wget

### Rocky Linux 8

    dnf -y install wget

You should not install EPEL `R-core or bowtie` on this system so do the following to remove it if it is already installed:

### CentOS 7

    yum remove R-core

### Rocky Linux 8

    dnf remove R-core

To prevent `R-core or bowtie` being installed from EPEL edit `/etc/yum.repos.d/epel.repo` and add the following line after the `gpgcheck=1` for the `[epel]` section:

    exclude=R-core bowtie2

If you try the following you should now get an error that there's no package available:

    yum install R-core

This will mean the `R-core` package from the BioIT repo will be installed once that is added.

## Prevent kernel updates

The machine will need a reboot any time a kernel update is applied. To avoid this add the following line to each section of the `CentOS-Base.repo` or `Rocky-BaseOS.repo` file in `/etc/yum.repos.d`:

    exclude=kernel*

If there's a bad kernel issue comment this line out, update the kernel and reboot the machine to apply the update but otherwise this should be fine and will allow the machine to stay up for extended periods.

## Other useful packages

The rpmfusion repo is also good to have as many packages not included in the base or EPEL are there. Install it with:

### CentOS 7

    yum localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm

### Rocky Linux 8

    dnf -y localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm

An example package would be ffmpeg which can be used to encode mp4 videos for some workflows. Install that with:

### CentOS 7

    yum -y install ffmpeg

### Rocky Linux 8

    dnf -y install ffmpeg

## Tools required for application support

The following packages are required for building the suite of applications on a fresh BioIT server:

### CentOS 7

    yum -y install ncurses-devel zlib-devel bzip2-devel xz-devel libcurl-devel openssl-devel environment-modules boost-devel cmake yum-plugin-changelog rpm-build git git-lfs screen htop root root-tree-viewer root-physics libX11-devel libXt-devel postgresql-devel readline-devel libxml2-devel gsl-devel mariadb-devel java-devel cairo-devel libpng-devel libjpeg-devel mlocate texinfo texinfo-tex tex texlive-* ant boost-devel perl-Test-Base sparsehash-devel openmpi-devel sqlite-devel python-devel python-nose python-pip perl-GD perl-GDGraph parallel gnuplot tcl-devel tk-devel perl-Env perl-Statistics-Descriptive cmake3 emacs-nox perl-Perl4-CoreLibs lapack-devel mpich-devel java-1.6.0-openjdk-devel zeromq-devel ghc cifs-utils python34-pip python34-devel perl-Archive-Tar perl-PerlIO-gzip hdf5-devel python-networkx gtk3-devel pigz tkinter python34-tkinter tcsh python-devel python34-devel python36-Cython libtiff-devel tmux pyqt4-devel nano python36-libs python36-devel python36-tkinter python36 python36-setuptools python36-pip python2-matplotlib NLopt-devel libsodium-devel libgit2-devel mysql++-devel lpsolve-devel suitesparse-devel mariadb-devel libsqlite3x-devel motif-devel motif-static motif ImageMagick-devel ImageMagick-c++-devel udunits2-devel proj-devel proj-epsg incron unixODBC-devel v8-devel librsvg2-devel xemacs libzstd-devel

### Rocky Linux 8

    dnf -y install git git-lfs ncurses-devel zlib-devel bzip2-devel xz-devel libcurl-devel openssl-devel environment-modules boost-devel cmake yum-plugin-changelog rpm-build screen htop root-tree-viewer root-physics libX11-devel libXt-devel postgresql-devel readline-devel libxml2-devel gsl-devel mariadb-devel java-devel cairo-devel libpng-devel libjpeg-devel mlocate texinfo texinfo-tex tex texlive-* ant boost-devel perl-Test-Base sparsehash-devel openmpi-devel sqlite-devel perl-GD perl-GDGraph parallel gnuplot tcl-devel tk-devel perl-Env perl-Statistics-Descriptive cmake3 emacs-nox perl-Perl4-CoreLibs lapack-devel mpich-devel python3-devel python3-nose python3-pip zeromq-devel ghc cifs-utils perl-Archive-Tar perl-PerlIO-gzip hdf5-devel python3-networkx gtk3-devel pigz python3-tkinter tcsh python3-Cython tmux  nano python3-libs python3-setuptools libsodium-devel libgit2-devel lpsolve-devel suitesparse-devel mariadb-devel libsqlite3x-devel motif-devel motif-static motif ImageMagick-devel ImageMagick-c++-devel udunits2-devel proj-devel incron unixODBC-devel librsvg2-devel xemacs apptainer libtiff-devel python2 python38 perl-Test-Harness rsync jasper-devel selinux-policy-devel

Packages necessary to run most old CentOS 7 binaries on Rocky Linux 8

    dnf -y install compat-openssl10 ncurses-compat-libs compat-libgfortran-48

Fix an issue building augustus with this (no longer needed because Augustus has mysql turned off in the build):

    ln -s /usr/lib64/mysql/libmysqlclient.so /usr/lib64/libmysqlclient.so

Fix problems building openmpi based tools (also not needed any more as openmpi isn't included in builds):

    echo "/usr/lib64/openmpi/lib/" > /etc/ld.so.conf.d/openmpi.conf
    ldconfig

On CentOS 7 default tools and changelogs are provided by the meta-RPMS that are built to set alternatives with symlinks into `/usr/bin` so they'll see them as usual. To set this up go to the [BioIT repository](BioIT-repository.md) page, but not just yet. On Rocky Linux 8 we're not doing these meta-RPMS any more, just environment modules.

For containerised tools to work the following directories need to exist in the root of the file system. If they don't you need to create them but only those that aren't already present. Here's the full set, edit as necessary

    mkdir /raid /active /archive /data /databases /deepgene /dunninga /gbs_pine /scratch /sequencing /treestem

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

For sudo without password (helps with the installations later) do the following:

    sudo visudo -f /etc/sudoers

Paste this in at the end:

    %build  ALL=(ALL) NOPASSWD:ALL

Add the following to the build user's `.bashrc` file to make building tools nicer:

    alias buildrepo="cd /opt/bioit/repo ; createrepo . -g bioit.xml --database"
    alias cleanbuild="rm -rf /home/build/rpmbuild/SPECS/* \
      /home/build/rpmbuild/SRPMS/* /home/build/rpmbuild/SOURCES/* \
      /home/build/rpmbuild/RPMS/*"
    alias check_updates="version_check_modules -av | egrep -v \"Up to date\""
    export PATH=/home/build/bioit/bin:$PATH

The `buildrepo` alias will be used to add new packages and updates. The `cleanbuild` alias is for emptying out the rpmbuild directory, and the `$PATH` variable has the bioit gitrepo `bin` directory added so you can use the various tools that are in there. This is only on CentOS 7 and we won't be doing this moving forward.

This user can now use sudo allowing us to disable root ssh logins but make sure you can ssh into this account before you do so. This means creating the `.ssh` directory and inside that the authorized_keys file which you'll paste the public key for the machine you're logging in from (make sure it is all on a single line) and `chmod 600 authorized_keys` otherwise ssh won't use it. Also `chmod 700 ~/.ssh` for the same reason.

If you're running Linux or Windows from your desktop you can easily transfer your ssh public key into the new machine using the following command:

    ssh-copy-id -i ~/.ssh/id_rsa.pub build@<IPADDR>

Remember to replace `<IPADDR>` with the actual address or hostname (if it is registered in DNS)

Once that user can log in and also sudo works for it, go ahead and make the following changes to the `/etc/ssh/sshd_config` file (be sure to comment out PermitRootLogin Yes from this file first so it doesn't override the new setting):

    PermitRootLogin No
    MaxAuthTries 3
    ClientAliveInterval 120
    ClientAliveCountMax 2
    UseDNS no

Then restart the ssh daemon.

    systemctl restart sshd.service

## Setup automatic updates

### CentOS 7

    yum -y install yum-cron

edit `/etc/yum/yum-cron.conf` adding the following:

    update_cmd = security
    apply_updates = yes

Enable and start the service

    systemctl enable yum-cron.service
    systemctl start yum-cron.service

### Rocky Linux 8

    dnf -y install dnf-automatic

edit `/etc/dnf/automatic.conf` adding the following:

    upgrade_type = security
    apply_updates = yes

Start the service

    systemctl start dnf-automatic

## Install remote desktop

### CentOS 7

    yum -y install x2goserver-xsession

This should now allow you to install the latest x2go client for your platform and connect to the server via the GUI MATE Desktop environment.

### Rocky Linux 8

Since Rocky Linux doesn't have the groupinstall "Mate Desktop" you need to install all the following:

    dnf -y install x2goserver mate-desktop mate-session-manager NetworkManager-adsl NetworkManager-bluetooth NetworkManager-libreswan-gnome NetworkManager-openvpn-gnome NetworkManager-ovs NetworkManager-ppp NetworkManager-team NetworkManager-wifi NetworkManager-wwan abrt-desktop abrt-java-connector adwaita-gtk2-theme alsa-plugins-pulseaudio atril atril-caja atril-thumbnailer caja caja-actions caja-image-converter caja-open-terminal caja-sendto caja-wallpaper caja-xattr-tags dconf-editor engrampa eom firewall-config gnome-disk-utility gnome-epub-thumbnailer gstreamer1-plugins-ugly-free gtk2-engines gucharmap gvfs-afc gvfs-afp gvfs-archive gvfs-fuse gvfs-gphoto2 gvfs-mtp gvfs-smb initial-setup-gui libmatekbd libmatemixer libmateweather libsecret lm_sensors marco mate-applets mate-backgrounds mate-calc mate-control-center mate-desktop mate-dictionary mate-disk-usage-analyzer mate-icon-theme mate-media mate-menus mate-menus-preferences-category-menu mate-notification-daemon mate-panel mate-polkit mate-power-manager mate-screensaver mate-screenshot mate-search-tool mate-session-manager mate-settings-daemon mate-system-log mate-system-monitor mate-terminal mate-themes mate-user-admin mate-user-guide mozo network-manager-applet nm-connection-editor p7zip p7zip-plugins pluma seahorse seahorse-caja xdg-user-dirs-gtk firefox

Since users are connecting remotely and assuming there are no local connections, the screensaver should be removed as this gets rid of the lock screen menu item which has caught some users out as we have no passwords:

### CentOS 7

    yum -y remove mate-screensaver

### Rocky Linux 8

    dnf -y remove mate-screensaver

Also remove the pulseaudio tools to stop logs being filled with errors as users try and start it from x2go:

### CentOS 7

    yum -y remove pulseaudio-gdm-hooks pulseaudio-utils pulseaudio-module-bluetooth pulseaudio

### Rocky Linux 8

    dnf -y remove pulseaudio-gdm-hooks pulseaudio-utils pulseaudio-module-bluetooth pulseaudio

## Turn off the automatic bug reporting tool

Users can't see the crash reports anyway so remove it using:

### CentOS 7

    yum -y remove abrt

### Rocky Linux 8

    dnf -y remove abrt

## Test the remote desktop

On your client you should install the X2Go client for your own desktop from here:

    https://wiki.x2go.org/doku.php/download:start

Once that is installed, create a config pointing at your new BioIT server and choose Mate as the session type and use the build user. It should connect and bring up a Mate Desktop session. No need to modify the firewall settings because X2Go runs over the ssh daemon.

## Proxy SSL certificate

If the system is behind a firewall that strips SSL certificates a number of things won't work unless the root cert is imported as follows:

    cp root_certificate.crt /etc/pki/ca-trust/source/anchors/
    update-ca-trust extract

## Next Step

Go to the [Storage-Setup](Storage-Setup.md) page.
