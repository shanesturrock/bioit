# Storage Setup

The storage array needs to be configured for CentOS 7.

Install the `sg3_utils` and `multipath` packages:

    yum -y install sg3_utils device-mapper-multipath

Run the following command:

    rescan-scsi-bus.sh

To use multipath copy the `multipath.conf` file into `/etc`:

    cp /usr/share/doc/device-mapper-multipath-0.4.9/multipath.conf .

Add the following changes:

    devices {
            device {
                    vendor COMPELNT
                    product "Compellent Vol"
                    path_checker tur
                    prio alua
                    path_selector "service-time 0"
                    path_grouping_policy group_by_prio
                    no_path_retry 24
                    hardware_handler "1 alua"
                    failback immediate
                    rr_weight priorities
            }
    }

Enable multipath at boot and start it:

    systemctl enable multipathd
    systemctl start multipathd

Now run the following to check the Compellant is visible:

    multipath -ll
    mpatha (36000d31003828e000000000000000005) dm-3 COMPELNT,Compellent Vol
    size=250T features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
    |-+- policy='service-time 0' prio=50 status=active
    | |- 8:0:1:1 sde 8:64 active ready running
    | `- 1:0:1:1 sdc 8:32 active ready running
    `-+- policy='service-time 0' prio=1 status=enabled
      |- 8:0:0:1 sdd 8:48 active ready running
      `- 1:0:0:1 sdb 8:16 active ready running

In our case, the file system showed up as `/dev/mapper/mpatha` so we should create an xfs file system and add a label to that with the following:

    mkfs.xfs -L RAID -f /dev/mapper/mpatha

Now we can edit the /etc/fstab and add the following line:

    LABEL=RAID /raid xfs defaults,discard,prjquota 0 0

Finally, `mkdir` the mount point and then mount the file system

    mkdir /raid
    mount /raid

That should be it.

## Issues after a reboot

After a reboot it may be that the storage just mounts as a normal SCSI device. To fix this, unmount it, rerun the `rescan-scsi-bus.sh` command and restart the multipathd. Once that is done, remount the raid and it should show as `/dev/mapper/mpatha` again and `multipath -ll` will return the correct output.

## Next Step

Go to the [XFS-User-and-Project-Quotas](XFS-User-and-Project-Quotas.md) page.
