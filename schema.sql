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
