# BioIT admin with ansible

This playbook is for managing chunks of BioIT administration

It has been tested and used in production with `CentOS 7` virtual servers. Other distros won't likely work at this time.

## What's included?
* Set up NFS mounts
* Installation of slurm cluster
* Manage users and groups
* Disables servers from asking for sudo password
* Disables ssh root access and password login for ssh

## How to setup an environment

`group_vars/all/users.yml` file contains the list of company super admins which should gain access to all created servers. Remove our example data and put list of your admins over there instead.

Create new folder inside `environments` for certain deployments. For example these can be: `production`, `testing` or `clientnamehere-cluster`.

### Inventory structure

Then create or edit the inventory file for the servers at `environments/{{your-environment}}/inventory`. This is an example:
```
[slurm-controllers]
xxx.xxx.xxx.xxx

[slurm-compute-nodes]
yyy.yyy.yyy.yyy
zzz.zzz.zzz.zzz

[slurm-submit-hosts]
zzz.zzz.zzz.zzz

[servers]
zzz.zzz.zzz.zzz
yyy.yyy.yyy.yyy
```
You can use hostnames or ip-addresses here. `servers` should mostly be for VMs that don't fit into one of the other categories.

### Non-admin user accounts

Then add people involved with certain environments into:
```
environments/{{your-environment}}/group_vars/all/users.yml
```

## How to deploy

This is how you would deploy configuration for an environment named `production` initially with user `root`. Please provide your ssh password for ansible.

```console
ansible-playbook -i environments/production site.yml -u root --ask-pass
```

**Notice: You only need to do this once! On the next run you can run it like this:**
```console
ansible-playbook -i environments/production site.yml -u your-user-name-here
```

You can run a partial playbook using tags, e.g.:

```console
ansible-playbook -i environments/production site.yml -u your-user-name-here --tags users
```

```console
ansible-playbook -i environments/production site.yml -u your-user-name-here --tags slurm
```
