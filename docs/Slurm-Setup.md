# Slurm Installation

Mostly based on https://www.slothparadise.com/how-to-install-slurm-on-centos-7-cluster/


## Munge install

Munge is used for authentication/encryption for intra-cluster Communications, and is needed on all machines wanting to particpate in the slurm cluster. There are already nice packages for this.

    sudo yum install -y epel-release && \
    sudo yum install -y munge munge-libs munge-devel

The above package install already creates a munge user.

If this is a new cluster install, then on the master, create the munge key:

    /usr/sbin/create-munge-key -r

Otherwise copy the existing server munge key into /etc/munge/ and ensure appropriate permissions.

Then enable and start the munge service:

    sudo systemctl enable munge
    sudo systemctl start munge

Test that munge is working via:

     munge -n | unmunge


## Slurm: package building

There aren't nice slurm pagkages, so we build them ourself.

First, install the packages that are needed to build slurm:

    sudo yum install -y rpm-build gcc openssl openssl-devel libssh2-devel pam-devel numactl numactl-devel hwloc hwloc-devel lua lua-devel readline-devel rrdtool-devel ncurses-devel gtk2-devel man2html libibmad libibumad perl-Switch perl-ExtUtils-MakeMaker mariadb-server mariadb-devel

    export VER=17.11.2
    curl -O https://download.schedmd.com/slurm/slurm-$VER.tar.bz2
    rpmbuild -ta slurm-$VER.tar.bz2

Copy the RPMs to somewhere central (NFS).


## Slurm: installation

Copy the RPMs to the various nodes.

We need a slurm user/group that is common across all nodes:

    export SLURMUSER=982
    sudo groupadd -g $SLURMUSER slurm
    sudo useradd -m -c "Slurm workload manager" -d /var/lib/slurm -u $SLURMUSER -g slurm -s /bin/bash slurm

Copy slurm config to all machines (contro / compute nodes / submit hosts):

     mkdir -p /etc/slurm
     cp slurm.conf /etc/slurm/


### Controller

Install the relevant RPMs:

    cd rpmbuild/RPMS/x86_64
    export VER=17.11.2
    sudo yum --nogpgcheck localinstall -y \
    slurm-$VER*.el7.centos.x86_64.rpm \
    slurm-devel-$VER*.el7.centos.x86_64.rpm \
    slurm-libpmi-$VER*.el7.centos.x86_64.rpm \
    slurm-perlapi-$VER*.el7.centos.x86_64.rpm \
    slurm-slurmctld-$VER*.el7.centos.x86_64.rpm \
    slurm-slurmd-$VER*.el7.centos.x86_64.rpm \
    slurm-slurmdbd-$VER*.el7.centos.x86_64.rpm \
    slurm-pam_slurm-$VER*.el7.centos.x86_64.rpm

On the controller we need to open appropriate ports:

    sudo firewall-cmd --permanent --zone=public --add-port=6817/udp
    sudo firewall-cmd --permanent --zone=public --add-port=6817/tcp
    sudo firewall-cmd --permanent --zone=public --add-port=6818/tcp
    sudo firewall-cmd --permanent --zone=public --add-port=6818/tcp
    sudo firewall-cmd --permanent --zone=public --add-port=7321/tcp
    sudo firewall-cmd --permanent --zone=public --add-port=7321/tcp
    sudo firewall-cmd --reload

However, if you want to test job submission on this node, we need to temporarily disable the firewall:

    sudo systemctl stop firewalld

Make sure we have the control directory (this must match the directory named in our slurm.conf):

    mkdir -p /var/spool/slurmctld && chown slurm: /var/spool/slurmctld && chmod 755 /var/spool/slurmctld;

Now try running the relevant slurm daemon manually first to check whether it is happy about things:

    sudo /usr/sbin/slurmctld -D -vv

If all is good, enable the service:

    sudo systemctl enable slurmctld.service
    sudo systemctl start slurmctld.service
    sudo systemctl status slurmctld.service


### Compute nodes

Install the RPMs:

    cd rpmbuild/RPMS/x86_64
    export VER=17.11.2
    sudo yum --nogpgcheck localinstall -y \
    slurm-$VER*.el7.centos.x86_64.rpm \
    slurm-libpmi-$VER*.el7.centos.x86_64.rpm \
    slurm-perlapi-$VER*.el7.centos.x86_64.rpm \
    slurm-slurmd-$VER*.el7.centos.x86_64.rpm \
    slurm-pam_slurm-$VER*.el7.centos.x86_64.rpm

On compute nodes, we also need to disable the firewall:

    sudo systemctl stop firewalld
    sudo systemctl disable firewalld

Try running the relevant slurm daemon manually first to check whether it is happy about things:

    sudo /usr/sbin/slurmd -D -vv

If all is good, enable the service:

    sudo systemctl enable slurmd.service
    sudo systemctl start slurmd.service
    sudo systemctl status slurmd.service


### Submit hosts

Install the RPMs:

    cd rpmbuild/RPMS/x86_64
    export VER=17.11.2
    sudo yum --nogpgcheck localinstall -y \
    slurm-$VER*.el7.centos.x86_64.rpm \
    slurm-perlapi-$VER*.el7.centos.x86_64.rpm \
    slurm-openlava-$VER*.el7.centos.x86_64.rpm \

On submit nodes, we also need to disable the firewall:

    sudo systemctl stop firewalld
    sudo systemctl disable firewalld

Run some test commands:

    sinfo
    scontrol show nodes
    srun -w com1 hostname


## Unanswered questions

* Do we need to enable job accounting (without accounting we can see queued and running jobs, but there isn't infromation on historical jobs)

* What is the best way to control resources


## Misc notes

There are several other RPMs build that aren't needed for our install:

    slurm-contribs-$VER*.el7.centos.x86_64.rpm
    slurm-example-configs-$VER*.el7.centos.x86_64.rpm
    slurm-openlava-$VER*.el7.centos.x86_64.rpm
    slurm-torque-$VER*.el7.centos.x86_64.rpm


Create various dirs (maybe this is optional?):

    sudo touch /var/log/slurmctld.log && sudo chown slurm: /var/log/slurmctld.log;
    sudo touch /var/log/slurmd.log && sudo chown slurm: /var/log/slurmd.log;
    touch /var/log/slurm_jobacct.log /var/log/slurm_jobcomp.log; \
    chown slurm: /var/log/slurm_jobacct.log /var/log/slurm_jobcomp.log;

     
