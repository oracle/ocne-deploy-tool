#!/usr/bin/python
#
# OCNE Deployment Tool
#
# Copyright (c) 2020,2021 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at
# https://oss.oracle.com/licenses/upl.
#
# Description: Python script to collect and store VM configuration details from user.
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
# pylint: disable=too-many-arguments

import os
import os.path

## Function to store generic VM configuration information common to all VMs being created

def setvmconfig(os_version,olvm_template,vm_network,vm_network_profile,vm_chrony,vm_dns,vm_dns_domain,vm_timezone,disk_download_url,disk_location):
    currentdir = os.path.dirname(os.path.abspath(__file__))
    if vm_network != "ovirtmgmt" :
        os.system('echo "vm_network: "%s"" >> %s/all.yml;echo "vm_network_profile: "%s"" >> %s/all.yml ' % (vm_network, currentdir, vm_network_profile, currentdir))
    else :
        os.system('echo "vm_network: ovirtmgmt" >> %s/all.yml;echo "vm_network_profile: %s" >> %s/all.yml' % (currentdir, vm_network_profile, currentdir))
    os.system('echo "ol_version: "%s"" >> %s/all.yml; echo "olvm_template: "%s"" >> %s/all.yml; echo "vm_chrony: server "%s" iburst" >> %s/all.yml; echo "vm_dns: "%s"" >> %s/all.yml; echo "vm_dns_domain: "%s"" >> %s/all.yml' % (os_version, currentdir, olvm_template, currentdir, vm_chrony, currentdir, vm_dns, currentdir, vm_dns_domain, currentdir))
    os.system('echo "vm_timezone: "%s"" >> %s/all.yml;echo "disk_download_url: "%s"" >> %s/all.yml;echo "disk_location: "%s"" >> %s/all.yml' % (vm_timezone, currentdir, disk_download_url, currentdir, disk_location, currentdir))

## Main Function to collect generic VM configuration information.

if __name__ == "__main__":

    os_version = raw_input("Enter OS version for VMs (ol7 OR ol8) [ol8]:")
    if not os_version:
        os_version = "ol8"
    olvm_template = raw_input("Enter Template Name to Create VMs:")
    vm_network = raw_input("Enter Logical network for guest VMs [ovirtmgmt]:")
    if not vm_network:
        vm_network = "ovirtmgmt"
    vm_network_profile = raw_input("Enter VNIC Profile of the Logical network [ovirtmgmt]:")
    if not vm_network_profile:
        vm_network_profile = "ovirtmgmt"
    vm_dns = raw_input("Enter DNS Server IP Address:")
    vm_dns_domain = raw_input("Enter DNS Search Domain String:")
    vm_timezone = raw_input("Enter VM timezone (Enter in format -> Region/Location; Ex: Asia/Kolkata) :")
    vm_chrony = raw_input("Enter IP Address OR FQDN of NTP Server:")
    disk_download_url = raw_input("Enter the URL to Download the QCOW2 image from:")
    disk_location = "/tmp/olvm_template_disk.qcow2"
    setvmconfig(os_version,olvm_template,vm_network,vm_network_profile,vm_chrony,vm_dns,vm_dns_domain,vm_timezone,disk_download_url,disk_location)
