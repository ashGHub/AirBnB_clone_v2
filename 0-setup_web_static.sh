#!/usr/bin/env bash
# Sets up a web servers for the deployment AirBnB Clone

# Install Nginx if it not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Folder variables
TEST_FOLDER='/data/web_static/releases/test/'
SHARED_FOLDER='/data/web_static/shared/'
SYMBOLIC_LINK='/data/web_static/current'
NGINX_CONFIG='/etc/nginx/sites-available/default'

# Create the folders and subfolders if they don't already exist
sudo mkdir -p "$TEST_FOLDER"
sudo mkdir -p "$SHARED_FOLDER"

# Create a fake HTML file
INDEX_CONT="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
echo "$INDEX_CONT" | sudo tee "$TEST_FOLDER/index.html"

# Create a symbolic link
sudo ln -sf "$TEST_FOLDER" "$SYMBOLIC_LINK"
# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Configure Nginx to serve the content of /hbnb_static
# the trailing slash is important which is /hbnb_static/
LOCATION_CONFIG="location /hbnb_static/ { alias $SYMBOLIC_LINK/; }"
# Insert of not already present
if ! grep "$LOCATION_CONFIG" "$NGINX_CONFIG"
then
    sudo sed -i "56i $LOCATION_CONFIG\n" "$NGINX_CONFIG"
fi
sudo service nginx restart

exit 0
