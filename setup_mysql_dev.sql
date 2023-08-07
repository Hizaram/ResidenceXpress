-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS residenceXpress_db;
CREATE USER IF NOT EXISTS 'rXpress_dev'@'localhost' IDENTIFIED BY 'rXpress_dev_pwd';
GRANT ALL PRIVILEGES ON `residenceXpress_db`.* TO 'rXpress_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'rXpress_dev'@'localhost';
FLUSH PRIVILEGES;
