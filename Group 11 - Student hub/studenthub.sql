CREATE DATABASE StudentHub;
USE StudentHub;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    marks1 INT,
    marks2 INT,
    marks3 INT,
    marks4 INT,
    marks5 INT,
    marks_obtained INT,
    total_marks INT DEFAULT 500,
    percentage FLOAT,
    grade VARCHAR(2),
    status VARCHAR(10)
);
