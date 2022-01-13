#!/usr/bin/python
#
# OCNE Deployment Tool
#
# Copyright (c) 2020,2021 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at
# https://oss.oracle.com/licenses/upl.
#
# Description: Python script to create backup of global variable
# and host inventory files and call the Ansible playbook
# to deploy the OCNE cluster.
#
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.
#
# pylint: disable=consider-using-f-string
# pylint: disable=undefined-variable
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long

import datetime
import os
import os.path


## Function to run the playbooks and store backup of host inventory file, variable file and password file if chosen
def deploy_cluster():
    """Runs playbooks and performs backup"""
    today = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    currentdir = os.path.dirname(os.path.abspath(__file__))
    basedir = os.path.abspath(os.path.join(currentdir, os.pardir))
    save_config = raw_input("Do you want to save current VM and OCNE cluster configuration settings and encrypted passwords? {y/N):")
    if save_config.lower() == ("y"):
        save_config = "true"
    elif save_config.lower() == ("n"):
        save_config = "false"
    os.system('export ANSIBLE_HOST_KEY_CHECKING=False; ansible-playbook -i %s/hosts.ini -e@%s/all.yml -e@%s/password.yml %s/playbooks/deploy.yml --ask-vault-pass' % (currentdir, currentdir, currentdir, basedir))
    if save_config == "true":
        save_password = raw_input("Do you want to save the passwords also in an encrypted file? {y/N):")
        if save_password.lower() == ("y"):
            save_password = "true"
        elif save_password.lower() == ("n"):
            save_password = "false"
        else :
            os.system('echo "Incorrect choice!! Password file will not be backed up"')
            save_password = "false"
        os.system('mkdir %s/backups/%s; mv %s/all.yml %s/backups/%s/all.yml' % (basedir, today, currentdir, basedir, today))
        os.system('mv %s/hosts.ini %s/backups/%s/hosts.ini' % (currentdir, basedir, today))
        if save_password == "true":
            os.system('mv %s/password.yml %s/backups/%s/password.yml' % (currentdir, basedir, today))
            os.system('echo "Configuration files and encrypted passwords backed up successfully!!"')
        elif save_password == "false":
            os.system('rm -f %s/password.yml ' % (currentdir))
            os.system('echo "Configuration files backed up successfully!!"')

    elif save_config == "false":
        os.system('rm -f %s/all.yml;rm -f %s/hosts.ini; rm -f %s/password.yml' % (currentdir, currentdir, currentdir))
        os.system('echo "Configuration files and passwords deleted!!"')

## Main Function to call the above function
if __name__ == "__main__":

    deploy_cluster()
