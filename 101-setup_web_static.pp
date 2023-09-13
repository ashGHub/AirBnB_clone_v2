# This script configures a server to deploy a static website
$data_folder = '/data'
$web_static_folder = "${data_folder}/web_static"
$release_folder = "${web_static_folder}/releases"
$test_folder = "${release_folder}/test"
$shared_folder = "${web_static_folder}/shared"

$symbolic_link = "${web_static_folder}/current"

$nginx_config = '/etc/nginx/sites-available/default'
$location_confg = "location /hbnb_static/ { alias ${symbolic_link}/; }\n"
$user_name = 'ubuntu'

$index_cnt = @("EOT")
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOT

$nginx_conf = @("EOT")
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
}
EOT

package { 'nginx':
  ensure => installed,
}

$folders = [$data_folder, $web_static_folder, $release_folder, $test_folder, $shared_folder]
file { $folders:
  ensure => directory,
}

file { "${test_folder}/index.html":
  ensure  => file,
  content => $index_cnt
}

file { $symbolic_link:
  ensure  => link,
  target  => $test_folder
}

file { 'insert line':
  path    => $nginx_config,
  content => $nginx_conf,
}

exec { "sudo chown -R ${user_name}:${user_name} ${data_folder}/":
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

exec { 'restart_nginx':
  command => 'sudo service nginx restart',
  path    => ['/usr/sbin', '/usr/bin', '/sbin', '/bin']
}
