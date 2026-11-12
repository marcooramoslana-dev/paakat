CREATE DATABASE IF NOT EXISTS paakat
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE paakat;

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE,
    slug VARCHAR(120) NOT NULL UNIQUE,
    description TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS elements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NULL,
    name VARCHAR(160) NOT NULL UNIQUE,
    slug VARCHAR(160) NOT NULL UNIQUE,
    description TEXT NULL,
    location VARCHAR(255) NULL,
    era VARCHAR(120) NULL,
    image_url VARCHAR(500) NULL,
    clip_prompt TEXT NULL,
    CONSTRAINT fk_elements_category
        FOREIGN KEY (category_id) REFERENCES categories (id)
        ON DELETE SET NULL,
    INDEX idx_elements_category (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS recognitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    element_id INT NULL,
    label VARCHAR(160) NOT NULL,
    confidence FLOAT NOT NULL,
    image_path VARCHAR(500) NULL,
    device_id VARCHAR(120) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recognitions_element
        FOREIGN KEY (element_id) REFERENCES elements (id)
        ON DELETE SET NULL,
    INDEX idx_recognitions_label (label),
    INDEX idx_recognitions_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
