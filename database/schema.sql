-- Reference schema for SQLite.
-- The application creates these tables automatically on startup.
-- You do not need to run this file for normal setup.

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    key VARCHAR(100) NOT NULL UNIQUE,
    value TEXT
);

CREATE TABLE IF NOT EXISTS knowledge_items (
    id INTEGER PRIMARY KEY,
    question VARCHAR(500) NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(100) DEFAULT 'general',
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME
);

CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY,
    channel VARCHAR(50) DEFAULT 'web',
    external_id VARCHAR(200),
    customer_name VARCHAR(200),
    customer_phone VARCHAR(50),
    status VARCHAR(50) DEFAULT 'active',
    created_at DATETIME,
    updated_at DATETIME
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER,
    customer_name VARCHAR(200) NOT NULL,
    customer_phone VARCHAR(50),
    service VARCHAR(200),
    appointment_time DATETIME NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    notes TEXT,
    status VARCHAR(50) DEFAULT 'confirmed',
    created_at DATETIME,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
