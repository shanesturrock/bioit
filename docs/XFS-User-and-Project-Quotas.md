# XFS User and Project Quotas

Quotas are baked into the XFS file system so setting them is trivial and should be easy to script up. For now, here's how to set up quotas, add and remove them.

## Enable quotas

Example setting user quotas on home:

Edit entry in `/etc/fstab`:

    /dev/mapper/cl-home     /home                   xfs     defaults,usrquota,grpquota,prjquota        1 2

Now execute the following command:

    mount -o remount /home

Future reboots will mount the storage correctly, this is just to avoid having to reboot the server to enable the quotas.

## Test the quotas

Test that the quotas are applied:

    xfs_quota -x -c "state" /home
     User quota state on /home (/dev/mapper/cl-home)
      Accounting: ON
      Enforcement: ON
      Inode: #10305 (2 blocks, 2 extents)
     Group quota state on /home (/dev/mapper/cl-home)
      Accounting: ON
      Enforcement: ON
      Inode: #10306 (2 blocks, 2 extents)
     Project quota state on /home (/dev/mapper/cl-home)
      Accounting: ON
      Enforcement: ON
      Inode: #10306 (2 blocks, 2 extents)
     Blocks grace time: [7 days]
     Inodes grace time: [7 days]
     Realtime Blocks grace time: [7 days]

This shows that the quotas are enabled for users, groups and projects.

Report quota for users, groups and projects:

     xfs_quota -x -c "report -h -ugp" /home
     User quota on /home (/dev/mapper/cl-home)
                            Blocks              
     User ID      Used   Soft   Hard Warn/Grace   
     ---------- --------------------------------- 
     root            0      0      0  00 [------]
     shane       98.3M      0      0  00 [------]

     Group quota on /home (/dev/mapper/cl-home)
                            Blocks              
     Group ID     Used   Soft   Hard Warn/Grace   
     ---------- --------------------------------- 
     root            0      0      0  00 [------]
     shane       98.3M      0      0  00 [------]

     Project quota on /home (/dev/mapper/cl-home)
                            Blocks              
     Project ID   Used   Soft   Hard Warn/Grace   
     ---------- --------------------------------- 
     #0          98.3M      0      0  00 [------]

## Setting user quotas

Set a user quota:

     xfs_quota -x -c "limit -u bsoft=9g bhard=10g shane" /home

Rerun quota report and note that there is now a soft quota of 9GB and a hard limit of 10GB:

     xfs_quota -x -c "report -h -u" /homeUser quota on /home (/dev/mapper/cl-home)
                            Blocks              
     User ID      Used   Soft   Hard Warn/Grace   
     ---------- --------------------------------- 
     root            0      0      0  00 [------]
     shane      998.3M     9G    10G  00 [------]

Test the quota by creating a large file as the user in their home directory:

     fallocate -l 9G test.img

Now run the report and you'll see that the user is at their soft quota but with 7 days to get below it.

     xfs_quota -x -c "report -h -u" /homeUser quota on /home (/dev/mapper/cl-home)
                            Blocks              
     User ID      Used   Soft   Hard Warn/Grace   
     ---------- --------------------------------- 
     root            0      0      0  00 [------]
     shane        9.1G     9G    10G  00 [7 days]

If the user tries to go over the hard limit they'll get the following:

     fallocate -l 10G test.img
     fallocate: test.img: fallocate failed: Disk quota exceeded

## Change the quota

The quota can be changed by setting bsoft and bhard to a new value for the user:

     xfs_quota -x -c "limit bsoft=10g bhard=11g shane" /home

Rerun the report to show the new quotas:

     xfs_quota -x -c "report -h -u" /home
     User quota on /home (/dev/mapper/cl-home)
                            Blocks              
     User ID      Used   Soft   Hard Warn/Grace   
     ---------- --------------------------------- 
     root            0      0      0  00 [------]
     shane       98.3M    10G    11G  00 [------]

## Remove the quota

The quota can be removed by setting bsoft and bhard to 0m for the user:

     xfs_quota -x -c "limit bsoft=0g bhard=0g shane" /home

Rerunning the report shows the quota is gone again:

     xfs_quota -x -c "report -h -u" /home
     User quota on /home (/dev/mapper/cl-home)
                            Blocks              
     User ID      Used   Soft   Hard Warn/Grace   
     ---------- --------------------------------- 
     root            0      0      0  00 [------]
     shane      998.3M      0      0  00 [------]

Group quotas are handled in the same way but will limit all users in a particular group to a specific quota. Alternatively, XFS has project quotas which can be applied to specific directories.

## Project quotas

The XFS file system supports project or directory quotas which is good for us. To enable them we need a project folder on a mount that has quotas enabled, for example /projects, and then we need to do the following to create a new project and set a quota for it.

Create projects and projid in case they don't exist:

     touch /etc/projects /etc/projid

Create the directory:

     mkdir /raid/projects/testproject

Each project has a name and an ID. For example, this project is called testproject, and we'll give it the ID of 1.

     echo "1:/raid/projects/testproject" >> /etc/projects
     echo "testproject:1" >> /etc/projid

User and group ownerships on the project folder are as normal with Linux, this is just for setting quotas so make sure the directory belongs to a user so they can work in it.

     chown -R shane:shane /raid/projects/testproject

Initialise the project quota:

     xfs_quota -x -c "project -s testproject" /raid
     Setting up project testproject (path /raid/projects/testproject)...
     Processed 1 (/etc/projects and cmdline) paths for project testproject with recursion depth infinite (-1).

Now set the quota for that directory:

     xfs_quota -x -c "limit -p bsoft=1g bhard=2g testproject" /raid

Check the quota has been applied for the project:

     xfs_quota -x -c "report -h -p" /raid
     Project quota on / (/dev/mapper/cl-root)
                            Blocks              
     Project ID   Used   Soft   Hard Warn/Grace   
     ---------- --------------------------------- 
     #0           8.5G      0      0  00 [------]
     testproject     0     1G     2G  00 [------]

As the user, try and write a big file:

     cd /raid/projects/testproject
     fallocate -l 1500M test.img

Rerun the quota report:

     xfs_quota -x -c "report -h -p" /raid
     Project quota on / (/dev/mapper/cl-root)
                            Blocks              
     Project ID   Used   Soft   Hard Warn/Grace   
     ---------- --------------------------------- 
     #0           8.5G      0      0  00 [------]
     testproject  1.5G     1G     2G  00 [7 days]

As the user try and write another file to push over the hard limit:

     fallocate -l 2500M test.img
     fallocate: test.img: fallocate failed: No space left on device

Remove the quota for the project:

     xfs_quota -x -c "limit -p bsoft=0m bhard=0m testproject" /raid

Note if you run a report now, you'll still see testproject listed:

     xfs_quota -x -c "report -h -p" /Project quota on / (/dev/mapper/cl-root)
                            Blocks              
     Project ID   Used   Soft   Hard Warn/Grace   
     ---------- --------------------------------- 
     #0           8.5G      0      0  00 [------]
     testproject  1.5G      0      0  00 [------]

You also need to clear the quota to get rid of it entirely:

     xfs_quota -x -c "project -C testproject" /raid
     Clearing project testproject (path /raid/projects/testproject)...
     Processed 1 (/etc/projects and cmdline) paths for project testproject with recursion depth infinite (-1).

     xfs_quota -x -c "report -h -p" /raid
     Project quota on / (/dev/mapper/cl-root)
                            Blocks              
     Project ID   Used   Soft   Hard Warn/Grace   
     ---------- --------------------------------- 
     #0          10.0G      0      0  00 [------]

Don't forget to delete the test project from the `/etc/projects` and `/etc/projid` to make sure it is entirely gone.

## Next Step

Go to the [NFS-User-and-Group-Quotas](NFS-User-and-Group-Quotas.md) page.
