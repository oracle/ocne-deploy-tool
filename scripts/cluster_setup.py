#!/usr/bin/python
#
# OCNE Deployment Tool
#
# Copyright (c) 2020,2021 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at
# https://oss.oracle.com/licenses/upl.
#
# Description: Python script to collect OCNE cluster setup info
# from user and create the global variable file
# and host inventory file for use by Ansible.
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
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=consider-using-enumerate
# pylint: disable=too-many-branches
# pylint: disable=consider-using-with
# pylint: disable=unspecified-encoding

import os
import os.path
import re

## Function to collect and store OCNE cluster specific information such as nodes, version and yum repository

def setocneconfig(nr_control_nodes,nr_worker_nodes,vm_ram,use_dhcp):
    currentdir = os.path.dirname(os.path.abspath(__file__))
    os.system('echo "[virtualmachines]" >> "%s"/hosts.ini' % (currentdir))
    controlplanenodes = []
    controlplanefqdn = []
    workernodes = []
    workernodefqdn = []
    os.system('echo "use_dhcp: %s" >> %s/all.yml' % (use_dhcp, currentdir))

## Here we collect name, FQDN and IP address for cluster nodes along with Gateway IP and Netmask for static IP configuration
    if use_dhcp == "false" :
        vm_gateway = raw_input("\nEnter Network Gateway IP Address:")
        vm_netmask = raw_input("Enter Network Netmask:")
        os.system('echo "vm_netmask: "%s"" >> %s/all.yml;echo "vm_gateway: "%s"" >> %s/all.yml' % (vm_netmask, currentdir, vm_gateway, currentdir))
        for i in range(int(nr_control_nodes)):
            x = i+1
            print("\nEntering Control Plane Node No."+str(x)+" Details")
            vm_name = raw_input("Enter the Name of Control Plane Node:")
            vm_fqdn = raw_input("Enter the FQDN of Control Plane Node:")
            vm_ipaddr = raw_input("Enter the IP Address of Control Plane Node:")
            os.system('echo "%s ansible_host=%s ansible_ssh_host=%s ansible_user=root" >> %s/hosts.ini' % (vm_name, vm_fqdn, vm_ipaddr, currentdir))
            controlplanenodes.append(vm_name)
            controlplanefqdn.append(vm_fqdn)
        for j in range(int(nr_worker_nodes)):
            x = j+1
            print("\nEntering Worker Node No."+str(x)+" Details")
            vm_name = raw_input("Enter the Name of Worker Node:")
            vm_fqdn = raw_input("Enter the FQDN of Worker Node:")
            vm_ipaddr = raw_input("Enter the IP Address of Worker Node:")
            os.system('echo "%s ansible_host=%s ansible_ssh_host=%s ansible_user=root" >> %s/hosts.ini' % (vm_name, vm_fqdn, vm_ipaddr, currentdir))
            workernodes.append(vm_name)
            workernodefqdn.append(vm_fqdn)

## Here we collect name, FQDN and MAC address for cluster nodes for DHCP IP configuration
    else :
        for i in range(int(nr_control_nodes)):
            x = i+1
            print("\nEntering Control Plane Node No."+str(x)+" Details")
            vm_name = raw_input("Enter the Name of Control Plane Node:")
            vm_fqdn = raw_input("Enter the FQDN of Control Plane Node:")
            vm_mac = raw_input("Enter the MAC Address of Control Plane Node:")
            os.system('echo "%s ansible_host=%s ansible_vm_mac=%s ansible_user=root" >> %s/hosts.ini' % (vm_name, vm_fqdn, vm_mac, currentdir))
            controlplanenodes.append(vm_name)
            controlplanefqdn.append(vm_fqdn)
        for j in range(int(nr_worker_nodes)):
            x = j+1
            print("\nEntering Worker Node No."+str(x)+" Details")
            vm_name = raw_input("Enter the Name of Worker Node:")
            vm_fqdn = raw_input("Enter the FQDN of Worker Node:")
            vm_mac = raw_input("Enter the MAC Address of Worker Node:")
            os.system('echo "%s ansible_host=%s ansible_vm_mac=%s ansible_user=root" >> %s/hosts.ini' % (vm_name, vm_fqdn, vm_mac, currentdir))
            workernodes.append(vm_name)
            workernodefqdn.append(vm_fqdn)

    os.system('echo " " >> %s/hosts.ini' % (currentdir))
    os.system('echo "[virtualmachines:vars]" >> "%s"/hosts.ini' % (currentdir))
    os.system('echo "vm_ram=%sMiB" >> %s/hosts.ini; echo " " >> %s/hosts.ini' % (vm_ram, currentdir, currentdir))

## Here we create operator node group and add the first control-plane node to it to double as operator node
    os.system('echo [ocne_op] >> %s/hosts.ini; echo %s >> %s/hosts.ini; echo " " >> %s/hosts.ini' % (currentdir, controlplanenodes[0], currentdir, currentdir))

## Here we create control-plane node group and add control-plane nodes names to it
    os.system('echo [ocne_kube_control] >> %s/hosts.ini' % (currentdir))
    for k in range(len(controlplanenodes)):
        os.system('echo %s >> %s/hosts.ini' % (controlplanenodes[k], currentdir))
    os.system('echo " " >> %s/hosts.ini' % (currentdir))

## Here we create worker node group and add worker nodes names to it
    os.system('echo [ocne_kube_worker] >> %s/hosts.ini' % (currentdir))
    for l in range(len(workernodes)):
        os.system('echo %s >> %s/hosts.ini' % (workernodes[l], currentdir))
    os.system('echo " " >> %s/hosts.ini' % (currentdir))
    os.system('echo "ha: true" >> %s/all.yml' % (currentdir))
    virtualip = raw_input("\nEnter the Virtual IP Address to be used with Nginx Load Balancer:")
    os.system('echo "virtual_ip: %s" >> %s/all.yml' % (virtualip, currentdir))
    ocne_version =  raw_input("Enter the OCNE Version to Deploy [1.4.0] :")
    ocne_repo = raw_input("Enter the OCNE Yum Repository Name [ol8_olcne14] :")

## Here we set default values for OCNE version and OCNE yum repository if not provided by user
    version = "ol_version"
    search = open("scripts/all.yml")
    for line in search:
        if version in line:
            version = line
    if version[14] == "7":
        if not ocne_version:
            ocne_version = "1.4.0"
            if not ocne_repo:
                if ocne_version.startswith('1.4'):
                    ocne_repo = "ol7_olcne14"
                elif ocne_version.startswith('1.3'):
                    ocne_repo = "ol7_olcne13"
                elif ocne_version.startswith('1.2'):
                    ocne_repo = "ol7_olcne12"
                elif ocne_version.startswith('1.1'):
                    ocne_repo = "ol7_olcne11"
            elif ocne_repo:
                print("\nYou have entered OCNE repo but no OCNE version. Either enter only OCNE version or enter both or leave both empty to select defaults")
                return
        elif ocne_version:
            if not ocne_repo:
                if ocne_version.startswith('1.4'):
                    ocne_repo = "ol7_olcne14"
                elif ocne_version.startswith('1.3'):
                    ocne_repo = "ol7_olcne13"
                elif ocne_version.startswith('1.2'):
                    ocne_repo = "ol7_olcne12"
                elif ocne_version.startswith('1.1'):
                    ocne_repo = "ol7_olcne11"
                else:
                    print("\nYou are using Oracle Linux 7, but entered an invalid/unsupported OCNE version.")
                    return
    elif version[14] == "8":
        if not ocne_version:
            ocne_version = "1.4.0"
            if not ocne_repo:
                if ocne_version.startswith('1.4'):
                    ocne_repo = "ol8_olcne14"
                elif ocne_version.startswith('1.3'):
                    ocne_repo = "ol8_olcne13"
                elif ocne_version.startswith('1.2'):
                    ocne_repo = "ol8_olcne12"
            elif ocne_repo:
                print("\nYou have entered OCNE repo but no OCNE version. Either enter only OCNE version or enter both or leave both empty to select defaults")
                return
        elif ocne_version:
            if not ocne_repo:
                if ocne_version.startswith('1.4'):
                    ocne_repo = "ol8_olcne14"
                elif ocne_version.startswith('1.3'):
                    ocne_repo = "ol8_olcne13"
                elif ocne_version.startswith('1.2'):
                    ocne_repo = "ol8_olcne12"
                else:
                    print("\nYou are using Oracle Linux 8, but entered an invalid/unsupported OCNE version.")
                    return

    os.system('echo "ocne_version: -%s" >> %s/all.yml' % (ocne_version, currentdir))
    os.system('echo "ocne_repo: %s" >> %s/all.yml' % (ocne_repo, currentdir))

## Get and set value for OCNE Environment and Kubernetes Module. Set to default if not entered.
    ocne_environment =  raw_input("Enter the name of OCNE Envrionment to Create [myenvironment] :")
    if not ocne_environment:
        ocne_environment = "myenvironment"
    ocne_k8s =  raw_input("Enter the name of Kubernetes Module to Create [mycluster] :")
    if not ocne_k8s:
        ocne_k8s = "mycluster"
    os.system('echo "ocne_environment: %s" >> %s/all.yml' % (ocne_environment, currentdir))
    os.system('echo "ocne_k8s: %s" >> %s/all.yml' % (ocne_k8s, currentdir))

## Check if Istio should be deployed
    deployistio = raw_input("Do you want to deploy the Istio module? (y/N):")
    if deployistio.lower() == ("y"):
        deploy_istio = "true"
    elif deployistio.lower() == ("n"):
        deploy_istio = "false"
        ocne_helm = ''
    else:
        print("\nInvalid choice!! Istio module will not be deployed")
        deploy_istio = "false"
        ocne_helm = ''
    os.system('echo "deploy_istio: %s" >> %s/all.yml' % (deploy_istio, currentdir))

## Get and set value for Helm and Istio modules. Set to default if not entered.
    if deploy_istio == "true":
        ocne_helm =  raw_input("Enter the name of Helm Module to Create [myhelm] :")
        if not ocne_helm:
            ocne_helm = "myhelm"
        ocne_istio =  raw_input("Enter the name of Istio Module to Create [myistio] :")
        if not ocne_istio:
            ocne_istio = "myistio"
        os.system('echo "ocne_helm: %s" >> %s/all.yml' % (ocne_helm, currentdir))
        os.system('echo "ocne_istio: %s" >> %s/all.yml' % (ocne_istio, currentdir))

## Check if OLM should be deployed
    if bool(re.search("^1\.[3-4]", ocne_version)):
        deployolm = raw_input("Do you want to deploy the Operator Lifecycle Manager (OLM) module? (y/N):")
        if deployolm.lower() == ("y"):
            deploy_olm = "true"
        elif deployolm.lower() == ("n"):
            deploy_olm = "false"
        else:
            print("\nInvalid choice!! Operator Lifecycle Manager module will not be deployed")
            deploy_olm = "false"
        os.system('echo "deploy_olm: %s" >> %s/all.yml' % (deploy_olm, currentdir))
    else:
        os.system('echo "deploy_olm: false" >> %s/all.yml' % (currentdir))

## Get and set value for Helm and OLM modules. Set to default if not entered.
    if deploy_olm == "true":
        if not ocne_helm:
            ocne_helm =  raw_input("Enter the name of Helm Module to Create [myhelm] :")
            if not ocne_helm:
                ocne_helm = "myhelm"
        ocne_olm =  raw_input("Enter the name of OLM Module to Create [myolm] :")
        if not ocne_olm:
            ocne_olm = "myolm"
        os.system('echo "ocne_olm: %s" >> %s/all.yml' % (ocne_olm, currentdir))

## Always enable externalIPs Kubernetes Service
    os.system('echo "restricted_ips: true" >> %s/all.yml' % (currentdir))

## Here we create a string of control-plane AND worker node FQDNs for storing the control-plane node+port and worker node+port along with all_nodes for use while creating OCNE cluster
    controlplanestring = ""
    for m in range(len(controlplanefqdn)):
        controlplanestring += controlplanefqdn[m]+','
    controlplanestring = controlplanestring [:-1]
    workernodestring = ""
    for n in range(len(workernodefqdn)):
        workernodestring += workernodefqdn[n]+','
    workernodestring = workernodestring [:-1]
    allnodes = controlplanestring+','+workernodestring
    controlnodelist = ""
    for m in range(len(controlplanefqdn)):
        controlnodelist += controlplanefqdn[m]+':8090,'
    controlnodelist = controlnodelist [:-1]
    workernodelist = ""
    for m in range(len(workernodefqdn)):
        workernodelist += workernodefqdn[m]+':8090,'
    workernodelist = workernodelist [:-1]
    os.system('echo "control_nodes: %s" >> %s/all.yml' % (controlnodelist, currentdir))
    os.system('echo "worker_nodes: %s" >> %s/all.yml' % (workernodelist, currentdir))
    os.system('echo "all_nodes: %s" >> %s/all.yml' % (allnodes, currentdir))

### Main Function to collect OCNE env details and call corresponding function to store in to file
if __name__ == "__main__":

    vm_ram = raw_input("Enter Amount of Memory to be Allocated to each VM in MiB (Minimum 4096) [4096]:")
    if not vm_ram:
        vm_ram = "4096"
    usedhcp = raw_input("Are you using DHCP server to allocate IP addresses? (y/N):")
    if usedhcp.lower() == ("y"):
        use_dhcp = "true"
    elif usedhcp.lower() == ("n"):
        use_dhcp = "false"
    nr_total_nodes = raw_input("\nEnter the Total Number of Nodes:")
    nr_control_nodes = raw_input("Enter the Number of Control Plane Nodes:")
    nr_worker_nodes = raw_input("Enter the Number of Worker Nodes:")
    setocneconfig(nr_control_nodes,nr_worker_nodes,vm_ram,use_dhcp)
