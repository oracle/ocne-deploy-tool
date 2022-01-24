#!/usr/bin/python
#
# OCNE Deployment Tool
#
# Copyright (c) 2020,2021 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at
# https://oss.oracle.com/licenses/upl.
#
# Description: Python script to setup the OLVM environment details.
#
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.
#
# pylint: disable=consider-using-f-string
# pylint: disable=undefined-variable
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=consider-using-sys-exit
# pylint: disable=redefined-outer-name

import os
import os.path
import socket
from getpass import getpass

## Function to input OLVM cluster, storage domain, container registry and basedir in to the all.yml

def allyaml(currentdir,olvm_cluster,storage_domain,container_registry):
    os.system('echo "---" > "%s"/all.yml; echo "olvm_cluster: "%s"" >> "%s"/all.yml; echo "storage_domain: "%s"" >> "%s"/all.yml ' % (currentdir, olvm_cluster, currentdir, storage_domain, currentdir))
    os.system('echo "container_registry: "%s"" >> "%s"/all.yml' % (container_registry, currentdir))

## Function to query if proxy needs to be used and collect and add info to all.yml respectively.

def proxyconf(currentdir):
    useproxy = raw_input("Are you using proxy in your environment? (y/N)?:")
    if useproxy.lower() == ("y"):
        use_proxy = "true"
    elif useproxy.lower() == ("n"):
        use_proxy = "false"
    if use_proxy == "true":
        http_proxy = raw_input("Enter value http_proxy:")
        https_proxy = raw_input("Enter value https_proxy:")
        no_proxy = raw_input("Enter value for no_proxy:")
        os.system('echo "use_proxy: "%s"" >> "%s"/all.yml; echo "my_https_proxy: "%s"" >> "%s"/all.yml; echo "my_http_proxy: "%s"" >> "%s"/all.yml; echo "my_no_proxy: "%s"" >> "%s"/all.yml ' % (use_proxy, currentdir, https_proxy, currentdir, http_proxy, currentdir, no_proxy, currentdir))
    elif use_proxy == "false":
        os.system('echo "use_proxy: "%s"" >> "%s"/all.yml' % (use_proxy, currentdir))

## Function to add OLVM FQDN, CA Certificate file location and user

def hosts(currentdir,olvm_fqdn,olvm_cafile,olvm_user):
    os.system('echo "[olvm]" > "%s"/hosts.ini; echo "%s ansible_user=root" >> "%s"/hosts.ini; echo " " >> "%s"/hosts.ini' % (currentdir, olvm_fqdn, currentdir, currentdir))
    os.system('echo "[olvm:vars]" >> "%s"/hosts.ini; echo "olvm_fqdn=%s" >> "%s"/hosts.ini; echo "olvm_user=%s" >> "%s"/hosts.ini; echo "olvm_cafile=%s" >> "%s"/hosts.ini;  echo " " >> "%s"/hosts.ini' % (currentdir, olvm_fqdn, currentdir, olvm_user, currentdir, olvm_cafile, currentdir, currentdir))

## Function to get password to setup for the VMs and store in to password.yml

def passyaml(currentdir,olvm_passwd):
    vm_passwd = getpass('Enter password to set for VMs:')
    os.system('echo "---" > "%s"/password.yml; echo "olvm_password: %s" >> "%s"/password.yml; echo "vm_root_passwd: %s" >> "%s"/password.yml' % (currentdir, olvm_passwd, currentdir, vm_passwd, currentdir ))
    os.system('echo "Encrypting password.yml with Ansible Vault"')
    os.system('echo "!!WARNING: The Ansible Vault password entered below will be required during deployment phase. Do not misplace it. Store in a secure location if you want to reuse it at a later time!!"')
    retcode = os.system('ansible-vault encrypt "%s"/password.yml' % (currentdir))
    if retcode != 0 :
        exit(2)


## Main Function to collect OLVM env details and call corresponding functions to store in to files.

if __name__ == "__main__":

    hostname = socket.gethostname()
    olvm_fqdn = raw_input("Enter OLVM manager FQDN [%s]:" % hostname)
    if not olvm_fqdn:
        olvm_fqdn = hostname
    olvm_passwd = getpass('Enter OLVM admin user password:')
    olvm_user = "admin@internal"
    olvm_cafile = "/etc/pki/ovirt-engine/ca.pem"
    olvm_cluster = raw_input("Enter OLVM Cluster Name [Default] :")
    if not olvm_cluster:
        olvm_cluster = "Default"
    storage_domain = raw_input("Enter Storage Domain Name:")
    currentdir = os.path.dirname(os.path.abspath(__file__))
    # basedir = os.path.abspath(os.path.join(currentdir, os.pardir))
    container_registry = "container-registry.oracle.com/olcne"
    allyaml(currentdir,olvm_cluster,storage_domain,container_registry)
    proxyconf(currentdir)
    hosts(currentdir,olvm_fqdn,olvm_cafile,olvm_user)
    passyaml(currentdir,olvm_passwd)
