# Updating

## Introduction

The following guide covers running updates on an already configured server.

## Before rebooting

Edit the `/etc/yum.repos.d/Rocky-BaseOS.repo` and comment out the `exclude=kernel*` line if you want to do a full update. Normally the server will only apply security updates but it is generally a good idea to update the kernel at least once a year.

Also, edit the `/etc/ssh/sshd_config` and enable root login by changing `PermitRootLogin No` to `Yes` and restart the sshd with `service sshd restart`. Check you can now log in as root. This is to avoid issues after a restart with NFS not mounting preventing regular users logging in.

In the root `crontab` there's `@reboot mount -a` (if not, add it) which should avoid the above scenario.

## Updating

First issue `dnf clean all` and then `dnf update` which should offer all the updates. Answer `y` if you're happy with this and then `reboot` should apply all this. If you don't have access to the console it is likely to take upwards of 20 mins to complete the reboot, then try logging in as your `build` user and if that fails with `too many authentication failures` switch to the root account and check the NFS came back up properly. If not, mount it by issuing `mount -a` from the root user account. Then try logging in as `build` again which should now work as the server will be able to access your account storage now.

## Checking the update worked

Sometimes services won't start. This is often because it has replcaed the `/etc/httpd/conf.d/ssl.conf` file breaking nginx. Edit that file and empty it, then restart httpd, nginx and anything else that hasn't started properly.

## Next Step

Go to the [Applications](Applications.md) page.
