# NFS User and Group Quotas

For machines that share storage via NFS, quotas should be enabled on the NFS server. The server file system can be XFS or EXT4 although with the latter, some extra steps are needed to enable quotas.

## Enable quotas on EXT4

For XFS, follow the instructions on XFS quotas. This section covers EXT4.

Before doing anything, ensure that the quota package installed:

    yum install quota

Once the quota package is installed you can set up the quotas.

Example setting user quotas on home (note with EXT4 you can't have project quotas):

Edit entry in `/etc/fstab`:

    /dev/mapper/cl-home     /home                   xfs     defaults,usrquota,grpquota        1 2

Now execute the following command:

    mount -o remount /home

Future reboots will mount the storage correctly, this is just to avoid having to reboot the server to enable the quotas.

## Create the quota database file

Execute the following:

    quotacheck -cugv /home

Turn on quotas:

    quotaon /home

## Modify quotas for Users

Using the `edquota` command you can modify user and group quotas. Note that for group quotas to apply, a directory needs to be `chmod g+s` so that all files created inside belong to the group rather than the user.

## Install the NFS server

Install the `nfs-utils` package:

    yum -y install nfs-utils

Turn on the NFS service

    systemctl enable nfs-server.service
    systemctl start nfs-server.service

To enable quotas to be detected on the client you need the rpc-rquotad service to be running.

    systemctl enable rpc-rquotad
    systemctl start rpc-rquotad

Export the file system by modifying `/etc/exports` and setting the IP address

    /home	10.0.0.0/16(rw,sync,no_root_squash,no_subtree_check)

This will allow any host in the 10.0.X.X range to mount the file system.

## Mount remote directory on another server

The client also needs the `quota` package installed so run the following there too:

    sudo yum -y install quota

On the client add the following to the `/etc/fstab` file (where 10.0.2.4 in this case is the NFS server):

    10.0.2.4:/home	/home	nfs	defaults,timeo=14,soft	0 0

As long as `/home` exists you should be able to mount the remote NFS using:

    mount /home

## Test the quotas

Test that the quotas are applied:

## Setting quotas

Set a user quota:

    edquota -u joebloggs

Set the soft and hard values. Note these are in bytes.

Set a group quota:

    edquota -g test

Note that even if the NFS server is running XFS, project quotas can't be seen on the NFS client, just user and group quotas. This means that is better to set up specific exports for each set of projects and also note that group quotas can be different on each export so you can have a group `test` and it can have independent quotas on two different discs. You can't have different quotas for the same group on a single disc though, you need separate partitions.

## Next Step

Go to the [BioIT-repository](BioIT-repository.md) page.
