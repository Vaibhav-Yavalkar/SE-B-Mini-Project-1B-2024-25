CREATE DATABASE newsapp;

USE newsapp;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(255) NOT NULL,
    email_address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    interest varchar(255) NOT NULL
);

CREATE TABLE bookmarks (
    bookmark_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    headline TEXT,
    href VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);