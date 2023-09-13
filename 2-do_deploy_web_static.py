#!/usr/bin/python3
"""
Fabric script that distributes an archive to a web server
For local testing, expected to run using the sudo su user
"""


from fabric.api import *
from os import path

# private key file command argument, -I ~/.ssh/id_rsa
# env.user = 'ubuntu'
# env.hosts = ['3.85.54.213', '54.90.35.144']

local_ips = ['localhost', '127.0.0.1']
web_static_folder = '/data/web_static'
release_folder = f'{web_static_folder}/releases'
symbolic_link = f'{web_static_folder}/current'


def do_deploy(archive_path):
    """ Distributes an archive to a web server """
    if not path.exists(archive_path):
        return False
    try:
        # extract zip file info
        zip_file = archive_path.split("/")[-1]
        zip_file_name = zip_file.split(".")[0]
        zip_file_path = f"/tmp/{zip_file}"
        new_release = f"{release_folder}/{zip_file_name}"

        is_local = env.host_string in local_ips
        # get command to use depending on local or remote
        command = local if is_local else run

        if is_local:
            # upload archive to /tmp/ directory
            local(f"cp {archive_path} /tmp/")
        else:
            # upload archive to /tmp/ directory
            put(archive_path, "/tmp/")

        # create release folder
        command(f"mkdir -p {new_release}")
        # unzip file to release folder
        command(f"tar -xzf {zip_file_path} -C {new_release}")
        # delete zip file
        command(f"rm {zip_file_path}")
        # move files to release folder, take it out from web_static folder
        command(f"cp -r {new_release}/web_static/* {new_release}/")
        # delete unziped web_static folder
        command(f"rm -rf {new_release}/web_static")
        # create new symbolic link
        command(f"ln -sf {new_release} {symbolic_link}")
        return True
    except Exception:
        return False
