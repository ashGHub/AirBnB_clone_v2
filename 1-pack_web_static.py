#!/usr/bin/python3
"""
Fabric script that archive web_static folder
For local testing, expected to run using the sudo su user
"""


from fabric.api import local
from datetime import datetime


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
