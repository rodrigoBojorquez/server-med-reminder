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

CREATE TABLE medicines(
	id_medicine INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name_medicine VARCHAR(255),
    type_medicine_id INT NOT NULL,		-- llave foranea
    dose_hour TIME NOT NULL,
    dose_day DATE NOT NULL,
    dose_quantity INT NOT NULL,
    comments VARCHAR(1000),
    user_id INT NOT NULL,				-- llave foranea
    medicine_taken INT,
    
    FOREIGN KEY (type_medicine_id) REFERENCES type_medicine(id_type_medicine),
    FOREIGN KEY (user_id) REFERENCES users(id_user)
);