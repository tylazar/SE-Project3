create database Aoc;
use Aoc;

create table AOCs (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
	PRIMARY KEY (id)
);

create table Courses (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
	PRIMARY KEY (id)
);

create table Courses_completed (
	id INT NOT NULL AUTO_INCREMENT,
	Student_id INT,
	Course_id INT,
	PRIMARY KEY (id)
);

create table Courses_for_requirements (
	id INT NOT NULL AUTO_INCREMENT,
	Requirement_id INT NOT NULL,
	Course_id INT,
	PRIMARY KEY (id)
);

create table LAC_Requirements (
	student_id INT NOT NULL,
	Math_proficiency TINYINT NOT NULL,
	Divisional_coursework TINYINT NOT NULL,
	Disiplinary_breadth TINYINT NOT NULL,
	Diverse_perspective TINYINT NOT NULL,
	Eight_liberal_art TINYINT NOT NULL,
	PRIMARY KEY (id)
);

create table Professors (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(30) NOT NULL,
	email VARCHAR(320) NOT NULL,
	PRIMARY KEY (id)
);

create table Requirements (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(50),
	AOC_id INT NOT NULL,
	NUM_to_complete INT,
	PRIMARY KEY (id)
);

create table Requirements_completed (
	id INT NOT NULL AUTO_INCREMENT,
	Student_id INT NOT NULL,
	Requirement_id INT NOT NULL,
	NUM_completed INT NOT NULL,
	status TINYINT NOT NULL,
	PRIMARY KEY (id)
);

create table Student_aoc (
	Student_id INT NOT NULL,
	AOC_id INT NOT NULL,
	PRIMARY KEY (id)
);

create table Students (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(30) NOT NULL,
	email VARCHAR(320) NOT NULL,
	advisor INT,
	Graduation_year INT,
	Agreed_as_advisee TINYINT,
	PRIMARY KEY (id)
);

