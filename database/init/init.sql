CREATE DATABASE IF NOT EXISTS gears;
CREATE TABLE IF NOT EXISTS users(
        id CHAR(64) PRIMARY KEY NOT NULL,
        model VARCHAR(30) NOT NULL,
        codename VARCHAR(25) NOT NULL,
        friendlyname VARCHAR(256) DEFAULT NULL
      );

CREATE TABLE IF NOT EXISTS settings(
        userid CHAR(64),
        global JSON DEFAULT NULL,
        system JSON DEFAULT NULL,
        secure JSON DEFAULT NULL,
        FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE
      );

CREATE TABLE IF NOT EXISTS selectedoverlays (
        userid CHAR(64),
        overlayIds JSON DEFAULT NULL,
        FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE
      );

CREATE TABLE IF NOT EXISTS overlays (
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        author VARCHAR(256) NOT NULL,
        name VARCHAR(256) NOT NULL,
        description VARCHAR(1024) NOT NULL,
        url VARCHAR(1024) NOT NULL
      );
