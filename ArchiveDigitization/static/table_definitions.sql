CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, hash BLOB, salt TEXT, first TEXT, last TEXT)
CREATE TABLE IF NOT EXISTS files(id TEXT PRIMARY KEY, is_digitized INT, image_text TEXT)
CREATE TABLE IF NOT EXISTS tags(id TEXT, name TEXT, file_id TEXT)
CREATE TABLE IF NOT EXISTS _tags(id TEXT PRIMARY KEY, name TEXT)
