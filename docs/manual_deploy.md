# Setup OCNE Options

## Change to the repo directory

`cd ocne_olvm`

Set up the hosts to use in:
`hosts.ini`

Set the variables in:
`group_vars/all.yml`
This file has several variables that need to be set.
Each variable has a description along with it.

**NOTE :** Explanation of each variable required by the playbook is present in [docs/examples](./examples)

## Selecting Istio (optional)

You can deploy either:

- Only the Kubernetes module
- Helm, Istio (which includes Prometheus) and/or
  Operator Lifecycle Manager (OLM) along with Kubernetes module

Set deploy_istio in group_vars/all.yml to "true" if
Istio should be deployed else set to "false".

Set deploy_olm in group_vars/all.yml to "true" if
OLM should be deployed else set to "false".

## Setup encrypted password file

Edit password.yml and add the OLVM password and
the root password to be set for the VMs.
Remove the informative and extra lines at the beginning of the file.
Then encrypt it as below:
`ansible-vault encrypt password.yml`

## Setup ssh private and public keys

You can either generate new ssh keys using ssh-keygen
and ssh-copy-id or use existing key pair.
Also ensure the public key is added to the
~/.ssh/authorized_keys file of the OLVM server.

```
ssh-keygen

ssh-copy-id root@<OLVM Manager FQDN>
```

Copy the private key "id_rsa" to
[playbooks/files/](../playbooks/files/)
and the public key "id_rsa.pub" to
[playbooks/files/](../playbooks/files/)

## Disable host_key_checking in Ansible

Edit /etc/ansible/ansible.cfg and set "host_key_checking" to "False"

`host_key_checking = False`

## Run as root user

This tool has to be run either using the root user
OR the non-root user should have passwordless ssh access
to the root user.

## Running the Ansible Playbooks

## Kubernetes Deployment

To set up a cluster of OLCNE on Oracle Linux (7 or 8), run:

```
cd playbooks
ansible-playbook deploy.yml -i hosts.ini --ask-vault-pass
```

## Show Verbose Output

If you're debugging the Ansible, you can use `-v` to show
more info as you run it.
Add more `v`s to get even more info, like `-vvvv`.

For Example:

`ansible-playbook -v deploy.yml -i hosts.ini --ask-vault-pass`

## Running Individual Playbooks

You can run the ansible-playbook files independently
if you need to repeat a certain action.

For example:

```
cd playbooks
ansible-playbook kube-reset.yml -i hosts.ini
```

## Scaling the cluster

Define the necessary parameters in `group_vars/all.yml` and `hosts.ini`

To add more nodes run;

`ansible-playbook scale/upscale.yml -i hosts.ini --ask-vault-pass`

To remove nodes run;

`ansible-playbook scale/downscale.yml -i hosts.ini`

This removes all nodes that are not defined
in the `control_nodes` and `worker_nodes` parameter
in `group_vars/all.yml`

**Note :** This does not delete VMs from Oracle Linux Virtualization Manager.

## Cleaning up Nodes

To clean up the nodes on Oracle Linux (7 or 8), run:

`ansible-playbook undeploy.yml -i hosts.ini`

**Note :** This does not delete VMs from Oracle Linux Virtualization Manager.
