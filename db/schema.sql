CREATE DATABASE med_reminder;
USE med_reminder;

CREATE TABLE users(
	id_user INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    user_password VARCHAR(50) NOT NULL,
    session_token VARCHAR(50) NOT NULL
);

CREATE TABLE type_medicine(
	id_type_medicine INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name_type_medicine VARCHAR(45)
);

CREATE TABLE status(
    id_status INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name_status VARCHAR(100)
);

CREATE TABLE medicines(
	id_medicine INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name_medicine VARCHAR(255) NOT NULL,
    type_medicine_id INT NOT NULL,		-- llave foranea
    dose_hour TIME NOT NULL,			-- hh:mm:ss
    dose_day DATE NOT NULL,				-- yyyy-mm-dd
    dose_quantity VARCHAR(100) NOT NULL,
    comments TEXT,
    user_id INT NOT NULL,               -- llave foranea
    medicine_group VARCHAR(20) NOT NULL,				
    status_id INT NOT NULL,
    
    FOREIGN KEY (type_medicine_id) REFERENCES type_medicine(id_type_medicine),
    FOREIGN KEY (user_id) REFERENCES users(id_user),
    FOREIGN KEY (status_id) REFERENCES status(id_status)
);