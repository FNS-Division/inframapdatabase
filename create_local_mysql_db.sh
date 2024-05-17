#To install MySQL on a Ubuntu resource

sudo apt install mysql-server

# Check status of MySQL server

sudo service mysql status

# Launch MySQL from the terminal prompt as the root user

sudo mysql -u root

# Create a new database, e.g called inframapdb

CREATE DATABASE inframapdb;

# Check that it has been created

SHOW DATABASES;

# Create database users and set password for that user, e.g create a new user called inframapuser with password Fantastic-Planet-85

CREATE USER 'inframapuser'@'localhost' IDENTIFIED BY 'my-password-5678';

# Grant this new user all privileges on the database

GRANT ALL PRIVILEGES ON inframapdb.* TO 'inframapuser'@'localhost';
FLUSH PRIVILEGES;

# Exit MySQL

exit

# Log back in as the new user, and enter password when prompted

mysql -u inframapuser -p