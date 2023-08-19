-- creates a database and a table
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- creates server user
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- give user all privileges for a database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- give user select privileges for a database
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';