CREATE DATABASE IF NOT EXISTS photoshare;
USE photoshare;

CREATE TABLE Users (
    user_id INTEGER AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    birth_date DATE,
    hometown VARCHAR(100),
    gender VARCHAR(100),
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE Friends (
    user_id1 INTEGER,
    user_id2 INTEGER,
    PRIMARY KEY (user_id1 , user_id2),
    FOREIGN KEY (user_id1)
        REFERENCES Users (user_id),
    FOREIGN KEY (user_id2)
        REFERENCES Users (user_id)
);

CREATE TABLE Albums (
    albums_id INTEGER AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    date DATE,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (albums_id),
    FOREIGN KEY (user_id)
        REFERENCES Users (user_id)
);

CREATE TABLE Photos (
    photo_id INTEGER AUTO_INCREMENT,
    caption VARCHAR(100),
    data LONGBLOB,
    albums_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (photo_id),
    FOREIGN KEY (albums_id)
        REFERENCES Albums (albums_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES Users (user_id)
);

CREATE TABLE Tags (
    photo_id INTEGER,
    tag VARCHAR(100),
    PRIMARY KEY (photo_id , tag),
    FOREIGN KEY (photo_id)
        REFERENCES Photos (photo_id) ON DELETE CASCADE
);

CREATE TABLE Comments (
    comment_id INTEGER AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    photo_id INTEGER NOT NULL,
    text VARCHAR(1000),
    date DATE,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (user_id)
        REFERENCES Users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (photo_id)
        REFERENCES Photos (photo_id) ON DELETE CASCADE
);

CREATE TABLE Likes (
    photo_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (photo_id , user_id),
    FOREIGN KEY (photo_id)
        REFERENCES Photos (photo_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES Users (user_id) ON DELETE CASCADE
);

INSERT INTO Users (email, password) VALUES ('guest@bu.edu', 'guest');
INSERT INTO Users (email, password) VALUES ('test@bu.edu', 'test');
INSERT INTO Users (email, password) VALUES ('test1@bu.edu', 'test');



