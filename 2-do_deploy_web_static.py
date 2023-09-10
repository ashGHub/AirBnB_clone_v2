#!/usr/bin/python3
"""Fabric script that distributes an archive to a web server"""

from fabric.api import *
from os import path
from datetime import datetime


local_ips = ['localhost', '127.0.0.1']

env.user = 'ubuntu'
env.hosts = ['3.85.54.213', '54.90.35.144']
# private key file command argument, -I ~/.ssh/id_rsa


def do_pack():
    """Generates a .tgz archive of web_static folder"""
    try:
        local("mkdir -p versions")
        # Date format: YYYYMMDDHHMMSS, e.g. 20210202025436
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = f"versions/web_static_{date}.tgz"
        # Assumes web_static is in the same folder as this script
        local(f"tar -cvzf {file_path} web_static")
        return file_path
    except Exception:
        return None


def do_deploy(archive_path):
    """ Distributes an archive to a web server """
    # deployment path
    web_static_folder = '/data/web_static'
    release_folder = f'{web_static_folder}/releases'
    symbolic_link = f'{web_static_folder}/current'

    if not path.exists(archive_path):
        return False
    try:
        # extract zip file info
        zip_file = archive_path.split("/")[-1]
        zip_file_name = zip_file.split(".")[0]
        zip_file_path = f"/tmp/{zip_file}"
        current_release = f"{release_folder}/{zip_file_name}"

        is_local = env.host_string in local_ips
        if is_local:
            # upload archive to /tmp/ directory
            local(f"cp {archive_path} /tmp/")
        else:
            # upload archive to /tmp/ directory
            put(archive_path, "/tmp/")

        # get command to use depending on local or remote
        command = local if is_local else run
        # create release folder
        command(f"mkdir -p {current_release}")
        # unzip file to release folder
        command(f"tar -xzf {zip_file_path} -C {current_release}")
        # delete zip file
        command(f"rm {zip_file_path}")
        # move files to release folder, take it out from web_static folder
        command(f"cp -r {current_release}/web_static/* {current_release}/")
        # delete unziped web_static folder
        command(f"rm -rf {current_release}/web_static")
        # create new symbolic link
        command(f"ln -sf {current_release} {symbolic_link}")
        return True
    except Exception:
        return False
