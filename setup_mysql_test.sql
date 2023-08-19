-- creates a database and a table
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- creates server user
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- give user all privileges for a database
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- give user select privileges for a database
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';