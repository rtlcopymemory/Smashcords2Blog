CREATE SCHEMA Smashcords2Blog;

SET search_path TO Smashcords2Blog;

CREATE TABLE IF NOT EXISTS Server
(
    serverID   NUMERIC PRIMARY KEY,
    name       VARCHAR(32),
    inviteLink VARCHAR(128)
);

CREATE TABLE IF NOT EXISTS Category
(
    serverID NUMERIC REFERENCES Server ON DELETE CASCADE ON UPDATE CASCADE,
    catName  VARCHAR(32),
    PRIMARY KEY (serverID, catName)
);

CREATE TABLE IF NOT EXISTS Post
(
    serverID NUMERIC,
    catName  VARCHAR(32),
    title    VARCHAR(64),
    subtitle VARCHAR(128),
    content  TEXT,
    PRIMARY KEY (serverID, catName, title),
    FOREIGN KEY (serverID, catName) REFERENCES Category ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Role
(
    serverID NUMERIC REFERENCES Server ON DELETE CASCADE ON UPDATE CASCADE,
    roleID   NUMERIC,
    PRIMARY KEY (serverID, roleID)
)