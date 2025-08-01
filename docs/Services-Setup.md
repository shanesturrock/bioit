# Services Setup

## Introduction

The following guide sets up various web services with SSL via NGINX and some other nice stuff.

## Rstudio Server Install

Download the installer:

### Rocky Linux 8

    wget https://download2.rstudio.org/server/rhel8/x86_64/rstudio-server-rhel-2025.05.0-496-x86_64.rpm

### Rocky Linux 9

    wget https://download2.rstudio.org/server/rhel9/x86_64/rstudio-server-rhel-2025.05.0-496-x86_64.rpm

### Rocky Linux 8 and 9

You need to specify where R is by doing the following before installing the rstudio server package:

    sudo mkdir /etc/rstudio
    sudo vi /etc/rstudio/rserver.conf

Paste the following into the rserver.conf file you're creating (changing the version of R as necessary):

    # Location of R
    rsession-which-r=/opt/bioit/R-core/4.5.0/bin/R
    # R library path
    rsession-ld-library-path=/opt/bioit/R-core/4.5.0/lib64/R/lib
    # Only listen localhost
    www-address=localhost
    # Connection port
    www-port=9797

Note that this will cause the server to only listen to localhost and port 9797.  You should add the localhost option even if using a vanilla install as the free RStudio Server package doesn't support SSL and we need to use NGINX to provide that.

Install the server:

    sudo yum install rstudio-server-rhel-2025.05.0-496-x86_64.rpm

For better performance you should edit the `/etc/rstudio/rsession.conf` file and add the following:

    # R Session Configuration File

    session-save-action-default=no

    # overrides the user/project restore workspace setting
    r-restore-workspace=0

If SELinux is enabled, do the following to allow the server to actually work and any time you upgrade versions:

    sudo chcon -R -t bin_t /usr/lib/rstudio-server/bin/

If you want to store the R session data on a local drive such as in `/usr/local/rstudio/$USER` you should create that directory and directories for each user inside here. Then shut down the rstudio-server and run this `sudo systemctl edit rstudio-server` and add the following:

    [Service]
    Environment="RSTUDIO_DATA_HOME=/usr/local/rstudio/$USER/rstudio"

You can create a full set of directories based on your `/home/` directory using the following:

    ( cd /home && find . -maxdepth 1 -type d -not -name . -exec sh -c 'for d do mkdir -p "/usr/local/rstudio/$d/rstudio" ; user="${d:2}" ; chown $user:$user -R /usr/local/rstudio/$d ; chmod 700 /usr/local/rstudio/$d ; done ' sh {} + )

If you add new users, don't forget to create this directory because the new user won't be able to log in. Set the ownership to their account and permissions to 700 like their regular home directory is. If you're migrating from having the rstudio directory in user's home directories, you can move the file from `/home/$USER/.local/share/rstudio` into `/usr/local/rstudio/$USER/rstudio` and then start the rstudio-server again.

Restart the service to make config channges take effect:

    sudo systemctl restart rstudio-server

You should now be able to open the RStudio Server interface by going to `http://localhost:9797` using Firefox inside the X2Go remote desktop.

## JupyterLab Install

Create the directory for the install:

    sudo mkdir /opt/jupyter
    sudo chown build:build jupyter

Make sure password free sudo is enabled as per the installation page. JupyterLab is installed by running the script in `~/bioit/bin`

    build_jupyterlab 4.4.3

If you want to include jupyter-ai, uncomment that line in this script before running it. You'll also need ollama.service installed and set up some LLMs for it to use.

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
    sudo systemctl restart nginx

At this point, SELinux should allow JupyterHub access to authentication and will continue to work.

## Jupyter Remote Desktop

It might be useful to have a remote desktop solution inside Jupyterhub. Assuming the Mate Desktop is already installed as per the installation page and X2Go config, you can do the following to add a launcher inside JupyterHub as the build user:

    sudo dnf -y install tigervnc tigervnc-server tigervnc-selinux
    cd /opt/jupyter/jupyterlab/4.4.3/jupyterlab_4.4.3/bin/
    ./pip install jupyter-remote-desktop-proxy

Set mate-session instead of xfce4-session in this file:

    sed -i -e 's/xfce4/mate/g' /opt/jupyter/jupyterlab/4.4.3/jupyterlab_4.4.3/lib/python3.10/site-packages/jupyter_remote_desktop_proxy/share/xstartup

Restart the JupyterHub and nginx services

    sudo systemctl restart jupyterhub
    sudo systemctl restart nginx

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

    sudo systemctl enable nginx
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

## Nice login banner

Having a nice banner about the machine can be done as follows:

    sudo dnf -y install neofetch figlet
    echo `hostname -s` | figlet > /etc/hostname-banner
    sudo echo -e "This server is the property of\nXXXX Ltd.\n\nAll access is monitored." >> /etc/hostname-banner
    sudo mkdir /etc/neofetch

Now set up neofetch for a non-gpu server:

    sudo cp /home/build/bioit/bin/neofetch.conf /etc/neofetch/neofetch.conf

or for a gpu server:

    sudo cp /home/build/bioit/bin/neofetch_gpu.conf /etc/neofetch/neofetch.conf

Finally create the motd.sh script in `/etc/profile.d`:

     sudo echo '#!/bin/bash' > /etc/profile.d/motd.sh; sudo echo 'printf "\n"' >> /etc/profile.d/motd.sh ; sudo echo 'neofetch --config /etc/neofetch/neofetch.conf --ascii /etc/hostname-banner' >> /etc/profile.d/motd.sh

Now when you log in you'll see a nice banner and updated stats on the machine.

## Nagios Install

Before doing anything, make sure crony is enabled otherwise logs will be funky:

    systemctl enable --now chronyd

Check you date, time and timezone are correct using `timedatectl`,

To ease the install of nagios and plugins, switch SELinux into permissive mode otherwise things will fail:

    sudo setenforce permissive

We'll turn SELinux on again once things are working.

Install dependencies for Nagios as root:

### Rocky Linux 8 and 9

    sudo -s
    dnf clean all
    dnf update
    dnf install -y php perl @httpd wget unzip glibc automake glibc-common gettext autoconf php php-cli gcc gd gd-devel net-snmp openssl-devel unzip net-snmp postfix net-snmp-utils

Before starting httpd remove the ssl.conf because we're going to put this behind NGINX.

    cd /etc/httpd/conf.d
    mv ssl.conf ssl.conf.bak

Also, we need to modify the `/etc/httpd/conf/httpd.conf` file to get Apache to listen on a non standard port by commenting out `Listen 80` and adding `Listen localhost:8282` otherwise Apache won't start.

Now start HTTPD and PHP

    systemctl enable httpd php-fpm
    systemctl enable php-fpm
    systemctl start httpd
    systemctl start php-fpm

Verify the services are running correctly and if not you've probably forgotten to switch SELinux into permissive mode.

    systemctl status httpd
    systemctl status php-fpm

You can also test that Apache is running via a browser in X2Go and going to `http://localhost:8282` and you should see the HTTP Server Test Page.

If Apache and PHP are running correctly, move on to installing Nagios by first downloading and building the source code:

    cd /root
    wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.5.9.tar.gz
    tar -xzf nagios-4.5.9.tar.gz
    cd nagios-4.5.9
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

Now set permissions for this file so Apache can use it:

    chmod 640 /usr/local/nagios/etc/htpasswd.users
    chown nagios:nagios /usr/local/nagios/etc/htpasswd.users
    systemctl restart httpd

Start Nagios:

    systemctl enable nagios --now

Check the service is running:

    systemctl status nagios

Note that it still won't work properly because there are no plugins but you should be able to get into the interface via a brwoser in X2Go at `http://localhost:8282/nagios` using the `nagiosadmin` account and the password you set for it. Once passed the login you'll get an error in services but that's because of the missing plugins so we'll fix that next.

## Nagios plugins install

Install the dependencies for plugins (still as root):

    dnf -y install gcc glibc glibc-common make gettext automake autoconf wget openssl-devel

Download and unpack the plugins:

    cd /root
    wget http://www.nagios-plugins.org/download/nagios-plugins-2.4.11.tar.gz
    tar xzf nagios-plugins-2.4.11.tar.gz

Build the plugins:

    cd nagios-plugins-2.4.11
    ./configure --with-nagios-user=nagios --with-nagios-group=nagios
    make
    make install

Restart Nagios and try the web interface again.

    systemctl restart nagios

Now you should be able to go into the services for localhost and get OKs for the default set of services as they refresh. Services can be customised later.

# Nagios pnp4nagios install

Install required dependencies for PNP4Nagios:

    dnf -y install rrdtool rrdtool-perl perl-Time-HiRes perl-GD php-xml php-gd php-json php-mbstring
    
Download and install PNP4Nagios:

    cd /root
    wget https://github.com/pnp4nagios/pnp4nagios/archive/refs/tags/v0.6.27-5.tar.gz
    tar xvf v0.6.27-5.tar.gz
    cd pnp4nagios-0.6.27-5
    ./configure
    make all
    make fullinstall

Now we need to modify the `/usr/local/nagios/etc/nagios.cfg` file adding the following:

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

Edit `/usr/local/nagios/etc/objects/commands.cfg` and comment out the process-host-perfdata and process-service-perfdata commands then append the following:

    define command{
           command_name    process-service-perfdata-file
           command_line    /bin/mv /usr/local/pnp4nagios/var/service-perfdata /usr/local/pnp4nagios/var/spool/service-perfdata.$TIMET$
    }
    
    define command{
           command_name    process-host-perfdata-file
           command_line    /bin/mv /usr/local/pnp4nagios/var/host-perfdata /usr/local/pnp4nagios/var/spool/host-perfdata.$TIMET$
    }

Also edit `/usr/local/nagios/etc/objects/templates.cfg` and append the following:

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

Lastly, edit `/usr/local/nagios/etc/objects/localhost.cfg` and for each service modify the `use local-service` line to be `use local-service,srv-pnp` and write out the file. Restart Nagios:

Edit `/usr/local/pnp4nagios/etc/npcd.cfg` and change the `perfdata_spool_dir =` definition to:

    perfdata_spool_dir = /usr/local/pnp4nagios/var/spool

Enable npcd service

    /usr/local/pnp4nagios/bin/npcd -d -f /usr/local/pnp4nagios/etc/npcd.cfg
    systemctl enable npcd.service --now

Restart Nagios and HTTPD

    systemctl restart nagios.service
    systemctl restart httpd.service

Open `http://localhost:8282/pnp4nagios/` in your browser via X2Go and check everything passes. If it starts again OK remove install.php file

    rm -f /usr/local/pnp4nagios/share/install.php

Create missing directory to store the data for localhost and set ownerships for nagios and pnp4nagios to avoid permissions issues:

    mkdir /usr/local/pnp4nagios/var/log/pnp4nagios/rrd/localhost
    chown -R nagios:nagios /usr/local/nagios /usr/local/pnp4nagios

Restart Nagios and HTTPD again:

    systemctl restart nagios.service
    systemctl restart httpd.service

As usual, it will take a while for the charts to show up as Nagios cycles through refreshes so be patient.

Also need to re-enable SELinux now that everything is working so do the following:

    cd /root
    grep denied /var/log/audit/audit.log | audit2allow -M nagios-module
    semodule -i nagios-module.pp
    setenforce enforcing
    systemctl restart nagios
    systemctl restart httpd

Check you can still interact with Nagios with SELinux enabled now.

At this point, all the local services are running but now we need NGINX to provide SSL Nagios so edit `/etc/nginx/nginx.conf` and add a server entry for the nagios DNS alias just as for jupyterhub and rstudio. You'll again need to do the SELinux work for nginx too:

    cd /root
    sudo setenforce permissive
    sudo grep denied /var/log/audit/audit.log | audit2allow -M nginx-module
    sudo semodule -i nginx-module.pp
    sudo setenforce enforcing
    sudo systemctl restart nginx

Now you should be able to go to the nagios alias from outside localhost. Check all the other services too and redo this process any time you hit an error until it all works. Reboot the machine to make sure it all comes back correctly too.

To avoid having to put in `hostname/nagios` you can copy the example `index.html.example` from the `bin/nagios_examples` directory to `/var/www/html/index.html` making sure you change `HOSTNAME` to the actual nagios server hostname alias. Once you've done that, restart apache (httpd) and you should now be able to go to your nagios alias and arrive at the home page directly.

Also note that you'll need to open port 80 for this to work from outside the host:

    sudo firewall-cmd --zone=public --permanent --add-service=http
    sudo firewall-cmd --reload

It isn't a security risk because the server immediately bounces the user over to the HTTPS port but it needs to be open for this redirect to work. Otherwise, just stick with appending `/nagios` if it is a worry.

## Next Step

Go to the [Updating](Updating.md) page.
