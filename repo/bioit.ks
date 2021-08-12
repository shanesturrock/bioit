install
text
reboot

# Need to set the IP address for the image to mirror.fsmg.org.nz manually
# because installer doesn't seem to understand the DNS
url --url=https://mirror.fsmg.org.nz/centos/7/os/x86_64/

lang en_US.UTF-8
keyboard us
network --onboot yes --device eth0 --bootproto dhcp
# root password will be ChangeMeNow
rootpw --iscrypted $1$thfc41$dgkI90H8xqOz61ha8zuyF.
selinux --disabled
timezone --utc Pacific/Auckland
zerombr
bootloader --location=mbr --append="rd_NO_PLYMOUTH"
clearpart --all
eula --agreed
services --enabled=NetworkManager,sshd
part / --fstype=xfs --grow --asprimary --size=200

%packages --nobase
coreutils
yum
rpm
e2fsprogs
ftp
openssh-server
openssh-clients
dhclient
ntp
yum-presto
yum-changelog
yum-utils
xauth
bind-utils
wget
man
screen
evince
blas
emacs
nfs-utils
gedit
mc
valgrind
cpan
cmake
glibc-static
libcurl-devel
libxml2-devel
libXp-devel
ncurses-devel
nautilus-open-terminal
environment-modules
# perl-Bio-SamTools
# perl-DBD-MySQL
# perl-Module-Build
python-matplotlib
postgresql-libs
postgresql-devel
xorg-x11-fonts-100dpi
xorg-x11-fonts-75dpi
vim-enhanced
tk
libreoffice
glibc.i686
libstdc++.i686
libgomp.i686
@Development tools
@X Window System
%end

%post --logfile /root/post.log

# Create bioit directory mount point
mkdir /opt/bioit

# Set run level
systemctl set-default multi-user.target

# Remove crash reporting
yum -y remove abrt

# Install required packages
yum -y install ncurses-devel zlib-devel bzip2-devel xz-devel libcurl-devel openssl-devel environment-modules boost-devel cmake yum-plugin-changelog rpm-build git screen htop root root-tree-viewer root-physics libX11-devel libXt-devel postgresql-devel readline-devel libxml2-devel gsl-devel mariadb-devel java-devel cairo-devel libpng-devel libjpeg-devel mlocate texinfo texinfo-tex tex texlive-* ant boost-devel perl-Test-Base sparsehash-devel openmpi-devel sqlite-devel python-devel python-nose python-pip perl-GD perl-GDGraph parallel gnuplot tcl-devel tk-devel perl-Env perl-Statistics-Descriptive cmake3 emacs-nox perl-Perl4-CoreLibs lapack-devel mpich-devel java-1.6.0-openjdk-devel zeromq-devel ghc cifs-utils python34-pip python34-devel perl-PerlIO-gzip hdf5-devel python-networkx gtk3-devel pigz tkinter python34-tkinter tcsh python-devel python34-devel python34-Cython libtiff-devel tmux pyqt4-devel nano python36-libs python36-devel python36-tkinter python36 python36-setuptools python36-pip python2-matplotlib NLopt-devel libsodium-devel libgit2-devel mysql++-devel lpsolve-devel suitesparse-devel mariadb-devel libsqlite3x-devel motif-devel motif-static motif ImageMagick-devel ImageMagick-c++-devel udunits2-devel proj-devel proj-epsg incron unixODBC-devel

# Fix problems building openmpi based tools and add local libs
echo "/usr/lib64/openmpi/lib/" > /etc/ld.so.conf.d/openmpi.conf
echo "/usr/local/lib" > /etc/ld.so.conf.d/local.conf
ldconfig

# Disable shutdown by normal users
echo "polkit.addRule(function(action, subject) {
    if ((action.id == "org.freedesktop.consolekit.system.stop" || action.id == "org.freedesktop.consolekit.system.restart") && subject.isInGroup("admin")) {
        return polkit.Result.YES;
    }
    else {
        return polkit.Result.NO;
    }
});" > /etc/polkit-1/rules.d/55-inhibit-shutdown.rules

# Set up automatic updates
yum -y install yum-cron
sed 's/update_cmd = default/update_cmd = security/g' --in-place /etc/yum/yum-cron.conf
sed 's/apply_updates = no/apply_updates = yes/g' --in-place /etc/yum/yum-cron.conf
systemctl enable yum-cron.service

# Install new compilers
yum -y install centos-release-scl
yum -y install devtoolset-9
yum -y install devscripts perl-LWP-Protocol-https

# Set up remote desktop
yum -y install epel-release
yum -y groupinstall "Mate Desktop"
yum -y install x2goserver-xsession
yum -y remove mate-screensaver
yum -y remove pulseaudio-gdm-hooks pulseaudio-utils pulseaudio-module-bluetooth pulseaudio

%end
