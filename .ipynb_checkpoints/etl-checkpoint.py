import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """ Creates the SONG and ARTIST table from a JSON file
    
    Arguments: the directory path wehre to find the JSON file
    Returns: void
    """
    
    df = pd.read_json(filepath, lines=True)

    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    artist_nan = df.fillna(0.0)
    artist_data = artist_nan[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur, filepath):
    """ Creates the TIME and USER table from a JSON file

    It creates the SONGPLAY_DATA table
    from performing a lookup query from the JSON file based on the song's title, artist's name and length of the song
    
    Arguments: the directory path wehre to find the JSON file
    Returns: void
    """
    
    df = pd.read_json(filepath,lines=True)
    df = df.filter(like='NextSong', axis=0)

    t = pd.to_datetime(df['ts'], origin='unix', unit='ms')
    
    time_data = (t.dt.time, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week_of_year', 'month', 'year', 'weekday')
    series = pd.Series(time_data, index=column_labels).to_dict()
    time_df = pd.DataFrame(series)
    
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)


    for index, row in df.iterrows():       
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        songplay_data = [index, row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """ Get all files matching extension from directory
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()