CREATE DATABASE IF NOT EXISTS ctf_db;
USE ctf_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES ('admin', '0e123123464646876543456789');

CREATE TABLE flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    flag VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO flags (user_id, flag) VALUES (1, 'MAC{Typ3_jugg11ng_1s_s0_stup1d_h00rah_php}');
