songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS 
songplays (songplay_id SERIAL PRIMARY KEY, start_time numeric NOT NULL, user_id numeric NOT NULL, level text, song_id text NOT NULL, artist_id text NOT NULL, session_id numeric, location text, user_agent text);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS 
users (user_id text PRIMARY KEY, first_name text, last_name text, gender varchar(1), level text);""")

song_table_create = (""" 
CREATE TABLE IF NOT EXISTS 
songs (song_id varchar PRIMARY KEY, title varchar, artist_id varchar, year int, duration numeric);""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS 
artists (artist_id text PRIMARY KEY, name text, location text, latitude float, longitude float);""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS 
time (start_time time NOT NULL PRIMARY KEY, hour numeric, day numeric, week numeric, month numeric, year numeric, weekday numeric);""")

songplay_table_insert = (""" 
INSERT INTO songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level) 
VALUES (%s, %s, %s, %s, %s) 
ON CONFLICT (user_id)
DO UPDATE SET level = excluded.level
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s);
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id)
DO NOTHING
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday) 
VALUES (%s, %s, %s, %s, %s, %s, %s);
""")

song_select = (""" 
SELECT songs.song_id, artists.artist_id 
FROM songs 
JOIN artists 
ON songs.artist_id = artists.artist_id
WHERE songs.title=(%s) AND artists.name=(%s) AND songs.duration=(%s)

""")

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]