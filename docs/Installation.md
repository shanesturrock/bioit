# Installation

## Install a minimal Rocky Linux 8 / Rocky Linux 9 environment

After a minimal install you should install EPEL, compilers and a GUI since they will be needed for users. It is easier to follow along with these instructions if you ssh into the shell from a terminal on your local machine. By default, a minimal install will have the root login enabled but we'll disable this later.

### Rocky Linux 8

    dnf -y install epel-release
    /usr/bin/crb enable
    dnf -y groupinstall "Standard"
    dnf -y groupinstall "Development Tools"
    dnf -y install libreoffice
    systemctl set-default multi-user.target
    dnf -y install gcc-toolset-9
    dnf -y update
    reboot

### Rocky Linux 9

    dnf -y install epel-release
    /usr/bin/crb enable
    dnf -y groupinstall "Standard"
    dnf -y groupinstall "Development Tools"
    dnf -y install libreoffice
    systemctl set-default multi-user.target
    dnf -y update
    reboot

X11 GUI won't start, but if you want it to run use this:

    systemctl set-default graphical.target

To enable the login window you need gdm:

### Rocky Linux 8 and 9

    dnf -y install gdm

Rebooting should bring up the chooser but do that later once the desktop is installed. You also need to choose the Mate desktop once that is installed.

If the machine will mount NFS storage you need to install the following:

### Rocky Linux 8 and 9

    dnf -y install nfs-utils

Also, if you're using NFS mounted home directories and you've got selinux enabled you'll need to set the following otherwise key authenticated ssh won't work:

    setsebool -P use_nfs_home_dirs 1

Install `wget` as this makes it much easier to download packages:

### Rocky Linux 8 and 9

    dnf -y install wget

You should not install EPEL `R-core or bowtie` on this system so do the following to remove it if it is already installed:

### Rocky Linux 8 and 9

    dnf remove R-core

To prevent `R-core or bowtie` being installed from EPEL edit `/etc/yum.repos.d/epel.repo` and add the following line after the `gpgcheck=1` for the `[epel]` section:

    exclude=R-core bowtie2

If you try the following you should now get an error that there's no package available:

    yum install R-core

This will mean the `R-core` package from the BioIT repo will be installed once that is added.

## Prevent kernel updates

The machine will need a reboot any time a kernel update is applied. To avoid this add the following line to each section of the `Rocky-BaseOS.repo` file in `/etc/yum.repos.d`:

    exclude=kernel*

If there's a bad kernel issue comment this line out, update the kernel and reboot the machine to apply the update but otherwise this should be fine and will allow the machine to stay up for extended periods.

## Other useful packages

The rpmfusion repo is also good to have as many packages not included in the base or EPEL are there. Install it with:

### Rocky Linux 8

    dnf -y localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm

### Rocky Linux 9

    dnf -y localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm

An example package would be ffmpeg which can be used to encode mp4 videos for some workflows. Install that with:

### Rocky Linux 8 and 9

    dnf -y install ffmpeg

## Tools required for application support

The following packages are required for building the suite of applications on a fresh BioIT server:

### Rocky Linux 8

    dnf -y install git git-lfs ncurses-devel zlib-devel bzip2-devel xz-devel libcurl-devel openssl-devel environment-modules boost-devel cmake yum-plugin-changelog rpm-build screen htop btop root-tree-viewer root-physics libX11-devel libXt-devel postgresql-devel readline-devel libxml2-devel gsl-devel mariadb-devel java-devel cairo-devel libpng-devel libjpeg-devel mlocate texinfo texinfo-tex tex texlive-* ant boost-devel perl-Test-Base sparsehash-devel openmpi-devel sqlite-devel perl-GD perl-GDGraph parallel gnuplot tcl-devel tk-devel perl-Env perl-Statistics-Descriptive cmake3 emacs-nox perl-Perl4-CoreLibs lapack-devel mpich-devel python3-devel python3-nose python3-pip zeromq-devel ghc cifs-utils perl-Archive-Tar perl-PerlIO-gzip hdf5-devel python3-networkx gtk3-devel pigz python3-tkinter tcsh python3-Cython tmux nano python3-libs python3-setuptools libsodium-devel libgit2-devel lpsolve-devel suitesparse-devel mariadb-devel libsqlite3x-devel motif-devel motif-static motif ImageMagick-devel ImageMagick-c++-devel udunits2-devel proj-devel incron unixODBC-devel librsvg2-devel xemacs apptainer libtiff-devel python2 python38 perl-Test-Harness rsync jasper-devel selinux-policy-devel xterm python39 netcdf-devel setools-console glpk-devel yum-utils python39-devel lftp mpfr-devel cargo pandoc

### Rocky Linux 9

For this command to work you need to enable the rocky-devel repo found in `/etc/yum.repos.d/rocky-devel.repo` with these two lines:

    includepkgs=lpsolve-devel
    enabled=1

Do a `dnf clean all` and then do the following:

    dnf -y install git git-lfs ncurses-devel zlib-devel bzip2-devel xz-devel libcurl-devel openssl-devel environment-modules boost-devel cmake yum-plugin-changelog rpm-build screen htop btop root-tree-viewer root-physics libX11-devel libXt-devel postgresql-devel readline-devel libxml2-devel gsl-devel mariadb-devel java-devel cairo-devel libpng-devel libjpeg-devel mlocate texinfo texinfo-tex tex texlive-* ant boost-devel perl-Test-Base sparsehash-devel openmpi-devel sqlite-devel perl-GD perl-GDGraph parallel gnuplot tcl-devel tk-devel perl-Env cmake3 emacs-nox perl-Perl4-CoreLibs lapack-devel mpich-devel python3-devel python3-pip zeromq-devel ghc cifs-utils perl-Archive-Tar perl-PerlIO-gzip hdf5-devel python3-networkx gtk3-devel pigz python3-tkinter tcsh python3-Cython tmux nano python3-libs python3-setuptools libsodium-devel libgit2-devel lpsolve-devel suitesparse-devel mariadb-devel libsqlite3x-devel motif-devel motif ImageMagick-devel ImageMagick-c++-devel udunits2-devel proj-devel incron unixODBC-devel librsvg2-devel apptainer libtiff-devel perl-Test-Harness rsync jasper-devel selinux-policy-devel xterm python39 netcdf-devel setools-console glpk-devel yum-utils lftp mpfr-devel cargo pandoc perl-Sys-Hostname perl-FindBin

Packages necessary to run most old CentOS 7 binaries:

### Rocky Linux 8

    dnf -y install compat-openssl10 ncurses-compat-libs compat-libgfortran-48

### Rocky Linux 9

    dnf -y install compat-openssl11 ncurses-compat-libs compat-libgfortran-48

For containerised tools to work the following directory needs to exist in the root of the file system. If not you need to create it but only those that aren't already present.

    mkdir /raid 

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

## Other useful user programs

A couple of nice programs are `ncdu` and `baobab` both of which allow uers to see how much disc space they're using.

    dnf -y install ncdu baobab

## Secure ssh but retain admin access

Create a build user account with admin rights which will be used to do tool updates:

    adduser build
    usermod -aG wheel build
    passwd build

For sudo without password (helps with the installations later) do the following:

    vi /etc/sudoers.d/build

Paste this into it:

    %build  ALL=(ALL) NOPASSWD:ALL

The following should be added for all installations:

    alias check_updates="version_check_modules -av | egrep -v \"Up to date\""
    export PATH=/home/build/bioit/bin:$PATH


This user can now use sudo allowing us to disable root ssh logins but make sure you can ssh into this account before you do so. This means creating the `.ssh` directory and inside that the authorized_keys file which you'll paste the public key for the machine you're logging in from (make sure it is all on a single line) and `chmod 600 authorized_keys` otherwise ssh won't use it. Also `chmod 700 ~/.ssh` for the same reason.

If you're running Linux or Windows from your desktop you can easily transfer your ssh public key into the new machine using the following command:

    ssh-copy-id -i ~/.ssh/id_rsa.pub build@<IPADDR>

Remember to replace `<IPADDR>` with the actual address or hostname (if it is registered in DNS)

Once that user can log in and also sudo works for it, go ahead and make the following changes to the `/etc/ssh/sshd_config` file (be sure to comment out `PermitRootLogin Yes` from this file first so it doesn't override the new setting):

    PermitRootLogin No
    MaxAuthTries 3
    ClientAliveInterval 120
    ClientAliveCountMax 2
    UseDNS no

Then restart the ssh daemon.

    systemctl restart sshd.service

## Setup automatic updates

Now that you have the build user setup to do sudo, you can use that for the rest. From the build user run:

    sudo -s

This should get you a root shell.

### Rocky Linux 8 and 9

    dnf -y install dnf-automatic

edit `/etc/dnf/automatic.conf` adding the following:

    upgrade_type = security
    apply_updates = yes

Start the service

    systemctl enable --now dnf-automatic.timer
    systemctl status dnf-automatic.timer

## Install remote desktop

Since Rocky Linux doesn't have the groupinstall "Mate Desktop" you need to install all the following:

### Rocky Linux 8

    dnf -y install x2goserver mate-desktop mate-session-manager NetworkManager-adsl NetworkManager-bluetooth NetworkManager-libreswan-gnome NetworkManager-openvpn-gnome NetworkManager-ovs NetworkManager-ppp NetworkManager-team NetworkManager-wifi NetworkManager-wwan abrt-desktop abrt-java-connector adwaita-gtk2-theme alsa-plugins-pulseaudio atril atril-caja atril-thumbnailer caja caja-actions caja-image-converter caja-open-terminal caja-sendto caja-wallpaper caja-xattr-tags dconf-editor engrampa eom firewall-config gnome-disk-utility gnome-epub-thumbnailer gstreamer1-plugins-ugly-free gtk2-engines gucharmap gvfs-afc gvfs-afp gvfs-archive gvfs-fuse gvfs-gphoto2 gvfs-mtp gvfs-smb initial-setup-gui libmatekbd libmatemixer libmateweather libsecret lm_sensors marco mate-applets mate-backgrounds mate-calc mate-control-center mate-desktop mate-dictionary mate-disk-usage-analyzer mate-icon-theme mate-media mate-menus mate-menus-preferences-category-menu mate-notification-daemon mate-panel mate-polkit mate-power-manager mate-screensaver mate-screenshot mate-search-tool mate-session-manager mate-settings-daemon mate-system-log mate-system-monitor mate-terminal mate-themes mate-user-admin mate-user-guide mozo network-manager-applet nm-connection-editor p7zip p7zip-plugins pluma seahorse seahorse-caja xdg-user-dirs-gtk firefox

You can replace `x2goserver` with `xrdp` to use Microsoft Remote Desktop.

### Rocky Linux 9

    dnf -y install xrdp mate-desktop mate-session-manager NetworkManager-adsl NetworkManager-bluetooth NetworkManager-libreswan-gnome NetworkManager-openvpn-gnome NetworkManager-ovs NetworkManager-ppp NetworkManager-team NetworkManager-wifi NetworkManager-wwan dwaita-gtk2-theme alsa-plugins-pulseaudio atril atril-caja atril-thumbnailer caja caja-actions caja-image-converter caja-open-terminal caja-sendto caja-wallpaper caja-xattr-tags dconf-editor engrampa eom firewall-config gnome-disk-utility gnome-epub-thumbnailer gstreamer1-plugins-ugly-free gtk2-engines gucharmap gvfs-fuse gvfs-gphoto2 gvfs-mtp gvfs-smb initial-setup-gui libmatekbd libmatemixer libmateweather libsecret lm_sensors marco mate-applets mate-backgrounds mate-calc mate-control-center mate-desktop mate-dictionary mate-disk-usage-analyzer mate-icon-theme mate-media mate-menus mate-menus-preferences-category-menu mate-notification-daemon mate-panel mate-polkit mate-power-manager mate-screensaver mate-screenshot mate-search-tool mate-session-manager mate-settings-daemon mate-system-log mate-system-monitor mate-terminal mate-themes mate-user-admin mate-user-guide mozo network-manager-applet nm-connection-editor p7zip p7zip-plugins pluma seahorse seahorse-caja xdg-user-dirs-gtk firefox

You can replace `x2goserver` with `xrdp` to use Microsoft Remote Desktop.

Since users are connecting remotely and assuming there are no local connections, the screensaver should be removed as this gets rid of the lock screen menu item which has caught some users out as we have no passwords:

### Rocky Linux 8 and 9

    dnf -y remove mate-screensaver

Also remove the pulseaudio tools to stop logs being filled with errors as users try and start it from x2go:

### Rocky Linux 8 and 9

    dnf -y remove pulseaudio-gdm-hooks pulseaudio-utils pulseaudio-module-bluetooth pulseaudio

## Turn off the automatic bug reporting tool

Users can't see the crash reports anyway so remove it using:

### Rocky Linux 8 (9 doesn't have this)

    dnf -y remove abrt

## Test the remote desktop

### X2go solution

On your client you should install the X2Go client for your own desktop from here:

    https://wiki.x2go.org/doku.php/download:start

Once that is installed, create a config pointing at your new BioIT server and choose Mate as the session type and use the build user. It should connect and bring up a Mate Desktop session. No need to modify the firewall settings because X2Go runs over the ssh daemon.

### XRDP solution

Run the following as super user in a terminal:

    systemctl start xrdp
    systemctl enable xrdp
    firewall-cmd --permanent --add-port=3389/tcp
    firewall-cmd --reload

Then, each user needs a file called `.Xclients` in their home directory which contains `mate-session` and is executable for the RDP session to launch.

## Proxy SSL certificate

If the system is behind a firewall that strips SSL certificates a number of things won't work unless the root cert is imported as follows:

    cp root_certificate.crt /etc/pki/ca-trust/source/anchors/
    update-ca-trust extract

## Next Step

Go to the [Storage-Setup](Storage-Setup.md) page.
