# Description
<!-- markdownlint-disable MD013 -->
Using the shell script
[ocne_olvm](../ocne_olvm),
you do not need to manually edit each file
to enter the values for the various variables required
for running the Ansible playbook.

You are prompted with questions for each variable and
you need to enter them at the command line.
Some fields have a default value
which will be selected if left empty.

It is the user's responsibility to provide correct and
valid input. If not done so, the Ansible playbook execution
may fail at any stage.

## Pre-requisites

1] Setup ssh private and public keys

You can either generate new ssh keys using ssh-keygen and
ssh-copy-id or use existing key pair.
Also ensure the public key is added to
the ~/.ssh/authorized_keys file of the OLVM server.

`ssh-keygen`

`ssh-copy-id root@<OLVM Manager FQDN>`

Copy the private key "id_rsa" to
[playbooks/files/](../playbooks/files/)
and the public key "id_rsa.pub" to
[playbooks/files/](../playbooks/files/)

2] This tool has to be run from the OLVM Server itself.

3] This tool has to be run either using the root user
OR the non-root user should have passwordless ssh access
to the root user.

## Script Usage

<!-- markdownlint-disable MD040 -->

```
    sh ocne_olvm [--help]
    --help    show this help message.

    The available options are:
        --deploy                       Deploy OCNE Cluster from scratch. Inclusive of all below options.
        --setup-environment            Setup OLVM Manager Information
        --add-vminfo                   Enter VM details
        --setup-cluster                Enter OCNE Cluster Information
        --run-playbook                 Execute the Ansible Playbook
```

## To Deploy from Scratch

Run the shell script with the `--deploy` option
to setup all the variables required by the Ansible playbook in one go.

This is basically a wrapper on all the below options
and runs through them in one go.

## To Setup OLVM Manager Details

Run the shell script with the `--setup-environment`
option to set the OLVM Manager Details only.

## To Setup VM Details

Run the shell script with the `--add-vminfo`
option to add the VM related details such as
the Oracle Linux version, location to download the qcow2 image, etc.

## To Setup OCNE Cluster Details

Run the shell script with the `--setup-cluster` option
to provide the OCNE cluster related information
such as VM hostnames, control plane and worker
node names, OCNE version, yum repository name, etc.

## To Run the Playbook only

Run the shell script with the `--run-playbook` option
to run the Ansible playbook only using a backup of
the variable files created during a previous run of the script.

## Backups

The backups of the hosts.ini, group_vars/all.yml and
password.yml are stored here after every failed or
successful run of the tool only when using the automated scripts.

This is done at the end playbook execution.
To be more precise, at the end of the `--run-playbook` phase.

The backup stored contains of all information such as
the VM and OCNE cluster details from the current run.

All files backed up in a given run will be stored in a
separate directory named with the timestamp at which
they were taken within the
[backups/](../backups) folder.
