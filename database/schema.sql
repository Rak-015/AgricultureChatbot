CREATE DATABASE IF NOT EXISTS agribot_db;
USE agribot_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(160) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS disease_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    image_path VARCHAR(255),
    disease_name VARCHAR(180) NOT NULL,
    confidence DECIMAL(6,2) NOT NULL,
    description_text TEXT,
    treatment TEXT,
    prevention TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS soil_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    ph DECIMAL(6,2), ec DECIMAL(6,2), oc DECIMAL(6,2), om DECIMAL(6,2),
    n DECIMAL(8,2), p DECIMAL(8,2), k_value DECIMAL(8,2), zn DECIMAL(8,2), fe DECIMAL(8,2),
    cu DECIMAL(8,2), mn DECIMAL(8,2), sand DECIMAL(8,2), silt DECIMAL(8,2), clay DECIMAL(8,2),
    caco3 DECIMAL(8,2), cec DECIMAL(8,2), result VARCHAR(40) NOT NULL, fertilizer TEXT, suggestions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS crop_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    n DECIMAL(8,2), p DECIMAL(8,2), k_value DECIMAL(8,2), temperature DECIMAL(6,2), humidity DECIMAL(6,2),
    ph DECIMAL(6,2), rainfall DECIMAL(8,2), crop_name VARCHAR(100) NOT NULL, reason_text TEXT, tips TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);
