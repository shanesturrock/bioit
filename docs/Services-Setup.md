# Services Setup

## Introduction

The following guide sets up various web services with SSL via NGINX and some other nice stuff.

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

## Nagios Install (Rocky 8 only currently)

https://wiki.crowncloud.net/?how_to_install_nagios_on_rockylinux8
https://www.tecmint.com/install-nagios-in-rocky-linux-and-almalinux/

First of all switch SELinux into permissive mode otherwise things will fail:

    sudo setenforce permissive

We'll turn SELinux on again once things are working.

Install dependencies for Nagios as root:

    sudo -s
    dnf clean all
    dnf update
    dnf install -y php perl @httpd wget unzip glibc automake glibc-common gettext autoconf php php-cli gcc gd gd-devel net-snmp openssl-devel unzip net-snmp postfix net-snmp-utils

Before starting httpd remove the ssl.conf because we're going to put this behind NGINX.

    cd /etc/httpd/conf.d
    mv ssl.conf ssl.conf.bak

Also, we need to modify the `/etc/httpd/conf/httpd.conf` file to get Apache to listen on a non standard port by commenting out `Listen 80` and adding `Listen localhost:8282` otherwise Apache won't start.

Now start HTTPD and PHP

    systemctl enable --now httpd php-fpm
    systemctl start httpd
    systemctl start php-fpm

Verify the services are running correctly and if not you've probably forgotten to switch SELinux into permissive mode.

    systemctl start httpd
    systemctl start php-fpm

You can also test that Apache is running via a browser in X2Go and going to `http://localhost:8282` and you should see the HTTP Server Test Page.

If Apache and PHP are running correctly, move on to installing Nagios by first downloading and building the source code:

    cd /root
    wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.4.6.tar.gz
    tar -xzf nagios-4.4.6.tar.gz
    cd nagios-*/
    ./configure

This is going to do the install in `/usr/local` and is better than using the RPM packages as it will be more configurable and easy to debug. Next build the source (assuming the previous step looks to have found all the dependencies it needed:

    make all

If that compiles successfully (Check the `Compile finished` output) we next need to create the nagios user account:

    make install-groups-users
    usermod -aG nagios apache

Next, install the software itself:

    make install
    make install-init
    make install-daemoninit
    make install-commandmode
    make install-config
    make install-webconf

Create the Nagios Web user account `nagiosadmin`(which will be used to log into the interface) giving it a password you can remember:

    htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin
    chmod 640 /usr/local/nagios/etc/htpasswd.users
    chown nagios:nagios /usr/local/nagios/etc/htpasswd.users
    systemctl restart httpd

Start Nagios:

    systemctl enable nagios --now

Check the service is running:

    systemctl status nagios

Note that it still won't work properly because there are no plugins but you should be able to get into the interface via a brwoser in X2Go at `http://localhost:8282/nagios` using the `nagiosadmin` account and the password you set for it. Once passed the login you'll get an error in services but that's because of the missing plugins so we'll fix that next.

## Nagios plugins install

https://kifarunix.com/install-nagios-plugins-on-rocky-linux-8/

Install the dependencies for plugins (still as root):

    dnf -y install gcc glibc glibc-common make gettext automake autoconf wget openssl-devel

Download and unpack the plugins:

    cd /root
    wget http://www.nagios-plugins.org/download/nagios-plugins-2.3.3.tar.gz
    tar xzf nagios-plugins-2.3.3.tar.gz

Build the plugins:

    cd nagios-plugins-2.3.3
    ./configure --with-nagios-user=nagios --with-nagios-group=nagios
    make
    make install

Restart Nagios and try the web interface again.

    systemctl restart nagios

Now you should be able to go into the services for localhost and get OKs for the default set of services. This can be customised later.

# Nagios pnp4nagios install

Download PNP4Nagios http://www.pnp4nagios.org/doku.php?id=start
untar it
dnf -y install rrdtool rrdtool-perl perl-Time-HiRes perl-GD php-xml php-gd
./configure
make all
make fullinstall
vi /usr/local/nagios/etc/nagios.cfg
Append this:
process_performance_data=1
# service performance data
service_perfdata_file=/usr/local/pnp4nagios/var/service-perfdata
service_perfdata_file_template=DATATYPE::SERVICEPERFDATA\tTIMET::$TIMET$\tHOSTNAME::$HOSTNAME$\tSERVICEDESC::$SERVICEDESC$\tSERVICEPERFDATA::$SERVICEPERFDATA$\tSERVICECHECKCOMMAND::$SERVICECHECKCOMMAND$\tHOSTSTATE::$HOSTSTATE$\tHOSTSTATETYPE::$HOSTSTATETYPE$\tSERVICESTATE::$SERVICESTATE$\tSERVICESTATETYPE::$SERVICESTATETYPE$
service_perfdata_file_mode=a
service_perfdata_file_processing_interval=15
service_perfdata_file_processing_command=process-service-perfdata-file

# host performance data
host_perfdata_file=/usr/local/pnp4nagios/var/host-perfdata
host_perfdata_file_template=DATATYPE::HOSTPERFDATA\tTIMET::$TIMET$\tHOSTNAME::$HOSTNAME$\tHOSTPERFDATA::$HOSTPERFDATA$\tHOSTCHECKCOMMAND::$HOSTCHECKCOMMAND$\tHOSTSTATE::$HOSTSTATE$\tHOSTSTATETYPE::$HOSTSTATETYPE$
host_perfdata_file_mode=a
host_perfdata_file_processing_interval=15
host_perfdata_file_processing_command=process-host-perfdata-file
vi /usr/local/nagios/etc/objects/commands.cfg
Append this:
define command{
       command_name    process-service-perfdata-file
       command_line    /bin/mv /usr/local/pnp4nagios/var/service-perfdata /usr/local/pnp4nagios/var/spool/service-perfdata.$TIMET$
}

define command{
       command_name    process-host-perfdata-file
       command_line    /bin/mv /usr/local/pnp4nagios/var/host-perfdata /usr/local/pnp4nagios/var/spool/host-perfdata.$TIMET$
}

Enable npcd service
/usr/local/pnp4nagios/bin/npcd -d -f /usr/local/pnp4nagios/etc/npcd.cfg
systemctl enable npcd.service

Restart Nagios and HTTPD
systemctl restart nagios.service
systemctl restart httpd.service

If it starts again OK remove install.php file
rm -f /usr/local/pnp4nagios/share/install.php

It then fails, edit data.php file:
vi /usr/local/pnp4nagios/share/application/models/data.php
Go to line 979 and replace
if (sizeof($pages) > 0){
with:
if (is_array($pages) && sizeof($pages) > 0) {

Edit json.php
vi /usr/local/pnp4nagios/share/application/lib/json.php
Change line 133 to
function Services_JSON_construct($use = 0)
Change line 783 to
function Services_JSON_Error_construct($message = 'unknown error', $code = null,
Change line 797 to
function Services_JSON_Error_construct($message = 'unknown error', $code = null,

Save the file. At this point graphs should start appearing.

This might help getting the graphs used by the services
https://arkit.co.in/pnp4nagios-installation-configuration/

Add the following to objects/template.cfg
define host {
        name host-pnp
        action_url /pnp4nagios/index.php/graph?host=$HOSTNAME$&srv=_HOST_' class='tips' rel=/pnp4nagios/index.php/popup?host=$HOSTNAME$&srv=_HOST_
        register 0
        }

define service {
        name srv-pnp
        action_url /pnp4nagios/index.php/graph?host=$HOSTNAME$&srv=$SERVICEDESC$' class='tips' rel=/pnp4nagios/index.php/popup?host=$HOSTNAME$&srv=$SERVICEDESC$
        register 0
        }

Then for each thing you want the graph on change local-service to local-service,srv-pnp in objects/localhost.cfg

Restart nagios and you should now be able to click on the graph next to each service to see the historical charts.

## Next Step

Go to the [Applications](Applications.md) page.