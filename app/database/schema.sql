CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    is_admin BOOLEAN DEFAULT false,
    is_banned BOOLEAN DEFAULT false,
    username VARCHAR(255) UNIQUE,
    full_name VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)