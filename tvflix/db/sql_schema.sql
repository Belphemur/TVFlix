-- Created by Vertabelo (http://vertabelo.com)
-- Script type: create
-- Scope: [tables, references, sequences, views, procedures]
-- Generated at Mon Feb 23 15:35:46 UTC 2015



-- tables
-- Table: Comments
-- Comments posted by the user on a specific show. A user can only post ONE comment per show.
CREATE TABLE Comments (
    comment_id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    user_id integer,
    show_id integer NOT NULL,
    comment text NOT NULL,
    posted datetime NOT NULL,
    updated datetime CHECK (updated IS NULL OR updated > posted),
    FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE SET NULL  ON UPDATE CASCADE,
    FOREIGN KEY (show_id) REFERENCES Shows (show_id) ON DELETE CASCADE 
);

CREATE UNIQUE INDEX Comments_one_per_user_show
ON Comments (user_id ASC, show_id ASC)
;


-- Table: Episodes
CREATE TABLE Episodes (
    ep_id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    show_id integer NOT NULL,
    title varchar(50),
    season integer NOT NULL CHECK (season >=0),
    number integer NOT NULL CHECK (number >= 0),
    bcast_date date NOT NULL,
    summary text,
    FOREIGN KEY (show_id) REFERENCES Shows (show_id) ON DELETE CASCADE  ON UPDATE CASCADE
);

-- Table: Shows
-- Different shows
CREATE TABLE Shows (
    show_id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    showlabel varchar(100) NOT NULL,
    title varchar(100) NOT NULL,
    start_year integer NOT NULL CHECK (start_year >=1900),
    end_year integer CHECK (end_year IS NULL OR end_year >= start_year),
    bcast_day integer CHECK (bcast_day IS NULL OR bcast_day BETWEEN 0 AND 6),
    summary text NOT NULL,
    channel varchar(25) NOT NULL
);

CREATE UNIQUE INDEX Show_label
ON Shows (showlabel ASC)
;


-- Table: Shows_Tags
-- Represent the Many to Many relation between shows and tags
CREATE TABLE Shows_Tags (
    show_id integer NOT NULL,
    tag_id integer NOT NULL,
    CONSTRAINT Shows_Tags_pk PRIMARY KEY (show_id,tag_id),
    FOREIGN KEY (show_id) REFERENCES Shows (show_id) ON DELETE CASCADE  ON UPDATE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tags (tag_id) ON DELETE CASCADE  ON UPDATE CASCADE
);

-- Table: Tags
-- Represent the different gender (drame, thriller, etc ...) that a show can have
CREATE TABLE Tags (
    tag_id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    name varchar(25) NOT NULL
);

CREATE UNIQUE INDEX Tags_idx_1
ON Tags (name ASC)
;


-- Table: Users
-- User that post comments
CREATE TABLE Users (
    user_id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    username varchar(155) NOT NULL,
    password varchar(100) NOT NULL,
    api_key varchar(64) NOT NULL,
    admin boolean NOT NULL
);

CREATE UNIQUE INDEX Users_api_key
ON Users (api_key ASC)
;


CREATE UNIQUE INDEX Users_username
ON Users (username ASC)
;



-- views
-- View: Episode_ShowLabel

CREATE VIEW Episode_ShowLabel AS
SELECT ep.*, s.showlabel FROM Episodes ep
LEFT JOIN Shows s
ON s.show_id = ep.show_id
GROUP BY s.showlabel, ep.season;




-- End of file.

