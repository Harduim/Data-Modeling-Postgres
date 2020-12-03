# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = """
CREATE TABLE songplays (
    "songplay_id" int NOT NULL IDENTITY, -- <=======
    "start_time" date NOT NULL,
    "user_id" date NOT NULL,
    "level" int NOT NULL,
    "song_id" varchar NOT NULL,
    "artist_id" varchar NOT NULL,
    "session_id" int NOT NULL,
    "location" text NOT NULL,
    "user_agent" text NOT NULL
);
"""

user_table_create = """
CREATE TABLE users (
    "user_id" int NOT NULL,
    "first_name" varchar NULL,
    "last_name" varchar NULL,
    "gender" char NULL,
    "level" varchar NULL
);
"""

song_table_create = """
CREATE TABLE songs (
    "song_id" varchar NOT NULL,
    "title" varchar NOT NULL,
    "artist_id" varchar NOT NULL,
    "year" int NOT NULL,
    "duration" float NOT NULL
);
"""

artist_table_create = """
CREATE TABLE artists (
    "artist_id" varchar NOT NULL,
    "name" varchar NOT NULL,
    "location" varchar NULL,
    "latitude" float NULL,
    "longitude" float NULL
);
"""

time_table_create = """
CREATE TABLE "time" (
    "start_time" date NOT NULL,
    "hour" int NOT NULL,
    "day" int NOT NULL,
    "week" int NOT NULL,
    "month" int NOT NULL,
    "year" int NOT NULL,
    "weekday" int NOT NULL
);
"""

# INSERT RECORDS

songplay_table_insert = """
INSERT INTO songplays
("start_time", "user_id", "level", "song_id", "artist_id", "session_id", "location", "user_agent")
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

user_table_insert = """
INSERT INTO users
("user_id", "first_name", "last_name", "gender", "level")
VALUES(%s, %s, %s, %s, %s);
"""

song_table_insert = """
INSERT INTO songs
("song_id", "title", "artist_id", "year", "duration")
VALUES(%s, %s, %s, %s, %s);
"""

artist_table_insert = """
INSERT INTO artists
("artist_id", "name", "location", "latitude", "longitude")
VALUES(%s, %s, %s, %s, %s);
"""


time_table_insert = """
INSERT INTO "time"
("start_time", "hour", "day", "week", "month", "year", "weekday")
VALUES(%s, %s, %s, %s, %s, %s, %s);
"""

# FIND SONGS

song_select = """
SELECT "song_id", "artist_id"
FROM songs AS s
INNER JOIN artists AS a ON s.artist_id = a.artist_id
WHERE s.duration = %s AND
      a.artist_name" = %s AND
      s.duration = %s;
"""

# QUERY LISTS

create_table_queries = [
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]
drop_table_queries = [
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop,
]