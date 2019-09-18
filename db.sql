CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username varchar(30) UNIQUE NOT NULL,
    created_at date,
    CHECK(username <> '')
);

CREATE TABLE Chat_Users (
	chat_id	INTEGER,
	user_id	INTEGER,
	PRIMARY KEY(chat_id, user_id),
	FOREIGN KEY(chat_id) REFERENCES Chat_Info(id),
    FOREIGN KEY(user_id) REFERENCES User(id)
);

CREATE TABLE Chat_Info (
	id	INTEGER PRIMARY KEY AUTOINCREMENT,
	name varchar(30) NOT NULL UNIQUE,
	created_at	date,
	CHECK(name <> '')
);

CREATE TABLE Message (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    chat_id INTEGER,
    user_id INTEGER,
    text TEXT,
    created_at date,
    FOREIGN KEY(chat_id, user_id) REFERENCES Chat_Users(chat_id, user_id),
    CHECK(text <> '')
);