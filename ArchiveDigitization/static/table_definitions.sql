CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, hash BLOB, salt TEXT, first TEXT, last TEXT)
CREATE TABLE IF NOT EXISTS files(id TEXT PRIMARY KEY, category TEXT, is_digitized INT, image_text TEXT)
