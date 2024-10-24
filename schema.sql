-- schema.sql

-- Create the users table
CREATE TABLE `users` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Create the messages table
CREATE TABLE `messages` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `user1` VARCHAR(100) DEFAULT NULL,
    `user2` VARCHAR(100) DEFAULT NULL,
    `message` TEXT DEFAULT NULL,
    `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Add foreign key constraints (optional, but recommended)
ALTER TABLE `messages`
  ADD CONSTRAINT `fk_user1` FOREIGN KEY (`user1`) REFERENCES `users` (`username`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_user2` FOREIGN KEY (`user2`) REFERENCES `users` (`username`) ON DELETE CASCADE;

-- schema.sql

-- Existing tables (users and messages) remain unchanged

-- Create the user_profiles table
CREATE TABLE `user_profiles` (
    `username` VARCHAR(100) NOT NULL,
    `avatar` VARCHAR(255) DEFAULT NULL,
    `status_message` VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (`username`),
    FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Create the read_receipts table
CREATE TABLE `read_receipts` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `message_id` INT(11) NOT NULL,
    `reader` VARCHAR(100) NOT NULL,
    `read_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`reader`) REFERENCES `users` (`username`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
