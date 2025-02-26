CREATE USER 'alessandro'@'localhost'
IDENTIFIED BY 'A1l2e3SQL$';

GRANT ALL PRIVILEGES ON film_db.* TO 'alessandro'@'localhost';

FLUSH PRIVILEGES;

SHOW GRANTS FOR 'alessandro'@'localhost';