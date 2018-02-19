# Proxmoxx / Ansible notes

## Recommended ~/.ssh/config setup

Bung the following into your ~/.ssh/config, which will let you ssh to VMs inside the 
proxmoxx system via names like `bioit/qmaster`:

    # Connecting to bioit hypervisor, also used as jump host for VMs
    Host chips bioit
         HostName 202.37.129.73
         User root
         ControlPath ~/.ssh/cm-%r@%h:%p
         ControlMaster auto
         ControlPersist 10m
    # General rule for using a jump host
    Host */*
         ProxyCommand ssh $(dirname %h) -W $(basename %h):%p
    # The above isn't very rsync/scp/ansible-friendly. This one is like the above but using +
    Host *+*
            ProxyCommand ssh -W $(echo %h | sed 's/^.*+//;s/^\([^:]*$\)/\1:22/') $(echo %h | sed 's/+[^+]*$//;s/\([^+%%]*\)%%\([^+]*\)$/\2 -l \1/;s/:\([^:+]*\)$/ -p \1/')


## VM setup

* Select CentOS ISO, hardware requirements etc and boot.
* Next next next until language (English New Zealand), timezone (select Auckland)
* Select default partitioninng
* Enable networking (eth0 switch) and set hostname (e.g. qmaster)
* Create root password (note it in proxmox VM notes), no extra users
* Wait for install to finish. Reboot, log in and use ip addr to show ip address.

* On chips, add an entry in /etc/dnsmasq.d/rtg.conf that maps the mac address to the desired IP address
* On chips, add an entry in /etc/hosts that maps the IP address to the desired host name
* On chips, service dnsmasq reload

* Other handy packages that aren't available in the minimal centos install:

    sudo yum install -y emacs-nox nfs-utils rsync


### Set up mounts

Temporary RTG nas mounts:

````
echo "adenine:/export/nas /nas nfs defaults 0 2" >>/etc/fstab
mkdir /nas && mount /nas
````


Bio-IT proper mounts:

````
mkdir -p /work/masseyifs
mkdir -p /sequencing/masseyifs
mkdir -p /home/masseyifs
mkdir -p /scratch/masseyifs
mkdir -p /opt/bioit
mkdir /databases
ln -s /sequencing /archive
ln -s /work /active

cat <<EOF >>/etc/fstab
chips:/home/masseyifs /home/masseyifs nfs defaults 0 2
chips:/scratch/masseyifs /scratch/masseyifs nfs defaults 0 2
chips:/sequencing/masseyifs /sequencing/masseyifs nfs defaults 0 2
chips:/work/masseyifs /work/masseyifs nfs defaults 0 2
chips:/opt/bioit /opt/bioit nfs defaults 0 2
chips:/databases /databases nfs defaults 0 2
EOF

mount -a
````


### Example resizing a disk in VM

* In proxmox, extend the size of the disk
* In the VM, edit the partition table to make the current one bigger. CAUTION, DON'T DO THESE AS IS, CHECK FOR YOUR USE CASE

````
fdisk /dev/sda
p
d 2
n p 2 <default> <default>
t 2 8e
p
w
````

* Reboot

* Grow the physical volume, then the root logical volume

````
sudo pvresize /dev/sda2
sudo lvextend -r -l 100%FREE /dev/mapper/centos_com?-root
lvs
df -h
````


### When using a cloned VM

A clone is identical, so some stuff may need to be updated if you want
multiple copies running. See:
https://pve.proxmox.com/wiki/Duplicate_Virtual_Machines

(However, it looks like some of this gets done automatically, I think I
only had to regenerate the ssh keys)


### Ansible user creation.

Ensure you are using a recent enough version of ansible. I installed it
in a python virtual environment, so I need to activate it via:

    source ~/venv/ansible/bin/activate

First, if you get errors like this:

    ERROR! SSH Error: data could not be sent to the remote host. Make sure this host can be reached over ssh

You probably need to edit `/etc/ansible/ansible.cfg` and set `scp_if_ssh = True`

Then you can install the usernames etc via:

    ansible-playbook -i environments/testing users.yml -u root --ask-pass --limit bioit-len-test-2

Where bioit-len-test-2 is the name of the new VM. After it has completed
successfully (i.e. including the ssh setup tasks), you don't need to use
-u root --ask-pass.

