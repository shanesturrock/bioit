The storage array needs to be configured for CentOS 7.

Install the `sg3_utils` and `multipath` packages:

    yum -y install sg3_utils device-mapper-multipath

Run the following command:

    rescan-scsi-bus.sh

To use multipath copy the `multipath.conf` file into `/etc`:

    cp /usr/share/doc/device-mapper-multipath-0.4.9/multipath.conf .

Enable multipath at boot and start it:

    systemctl enable multipathd
    systemctl start multipathd

Now run the following to check the Compellant is visible:

    multipath -ll
    mpatha (36000d31003828e000000000000000005) dm-3 COMPELNT,Compellent Vol
    size=250T features='1 queue_if_no_path' hwhandler='0' wp=rw
    `-+- policy='service-time 0' prio=1 status=active
      |- 8:0:2:1 sdb 8:16 active ready running
      |- 8:0:3:1 sde 8:64 active ready running
      |- 1:0:6:1 sdc 8:32 active ready running
      `- 1:0:7:1 sdd 8:48 active ready running

In our case, the file system showed up as `/dev/mapper/mpatha1` (possibly because I had previously created a file system on it) so we should add a label to that with the following:

    xfs_admin -L RAID /dev/mapper/mpatha1

Now we can edit the /etc/fstab and add the following line:

    LABEL=RAID /raid xfs defaults,discard,prjquota 0 0

Finally, `mkdir` the mount point and then mount the file system

    mkdir /raid
    mount /raid

That should be it.