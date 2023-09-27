#!/usr/bin/python3
"""
Fabric script that distributes an archive to a web server
For local testing, expected to run using the sudo su user
"""


from fabric.api import *
from os import path
from datetime import datetime

# env.key_filename = '~/.ssh/id_rsa'
# env.user = 'ubuntu'
# env.hosts = ['3.85.54.213', '54.90.35.144']


local_ips = ['localhost', '127.0.0.1']
web_static_folder = '/data/web_static'
release_folder = '{}/releases'.format(web_static_folder)
symbolic_link = '{}/current'.format(web_static_folder)


def do_pack():
    """Generates a .tgz archive of web_static folder"""
    try:
        local("mkdir -p versions")
        # Date format: YYYYMMDDHHMMSS, e.g. 20210202025436
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = "versions/web_static_{}.tgz".format(date)
        # Assumes web_static is in the same folder as this script
        local("tar -cvzf {} web_static".format(file_path))
        return file_path
    except Exception:
        return None


def do_deploy(archive_path):
    """ Distributes an archive to a web server """
    if not path.exists(archive_path):
        return False
    try:
        # extract zip file info
        zip_file = archive_path.split("/")[-1]
        zip_file_name = zip_file.split(".")[0]
        zip_file_path = "/tmp/{}".format(zip_file)
        new_release = "{}/{}".format(release_folder, zip_file_name)

        is_local = env.host_string in local_ips
        # get command to use depending on local or remote
        command = local if is_local else run

        if is_local:
            # upload archive to /tmp/ directory
            local("cp {} /tmp/".format(archive_path))
        else:
            # upload archive to /tmp/ directory
            put(archive_path, "/tmp/")

        # create release folder
        command("mkdir -p {}".format(new_release))
        # unzip file to release folder
        command("tar -xzf {} -C {}".format(zip_file_path, new_release))
        # delete zip file
        command("rm {}".format(zip_file_path))
        # copy files to release folder from web static folder
        command("cp -r {}/web_static/* {}/".format(new_release, new_release))
        # delete unziped web_static folder
        command("rm -rf {}/web_static".format(new_release))
        # create new symbolic link
        command("ln -sf {} {}".format(new_release, symbolic_link))
        return True
    except Exception:
        return False
