import os
from contextlib import contextmanager
from glob import glob
from typing import Callable, Iterator

import pandas as pd
import psycopg2
from psycopg2.extensions import cursor

import sql_queries as sql


@contextmanager
def get_connection() -> cursor:
    """ensure the connection is committed and closed, or rollbacked in case of errors

    Yields:
        psycopg2 cursor
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    try:
        yield cur
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.commit()
        conn.close()


def get_files(filepath: str) -> Iterator[str]:
    """Get the absolute path for all json files in a given folder

    Args:
        filepath (str): Folder path

    Yields:
        Iterator[str]: Absolute path for a json file
    """
    for root, _, files in os.walk(filepath):
        files = glob(os.path.join(root, "*.json"))
        for file in files:
            yield os.path.abspath(file)


def process_song_file(cur: cursor, filepath: str):
    """Process a song file

    Args:
        cur (cursor): Conected cursor
        filepath (str): Path for a json file
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = list(df.loc[0, ["song_id", "title", "artist_id", "year", "duration"]].values)
    song_data = [str(col) for col in song_data]
    cur.execute(sql.song_table_insert, song_data)

    # insert artist record
    cols = ["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]
    artist_data = list(df.loc[0, cols].values)

    # converting all cells to str
    artist_data = [str(col) for col in artist_data]
    cur.execute(sql.artist_table_insert, artist_data)


def process_log_file(cur: cursor, filepath: str):
    """Process a log file

    Args:
        cur (cursor): Conected cursor
        filepath (str): Path for a json file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    df.ts = df.ts.astype("datetime64[ms]")
    df["hour"] = df.ts.dt.hour
    df["day"] = df.ts.dt.day
    df["week"] = df.ts.dt.week
    df["month"] = df.ts.dt.month
    df["year"] = df.ts.dt.year
    df["weekday"] = df.ts.dt.weekday

    for row in df.itertuples(index=False):
        time_vals = (
            f"{row.ts:%Y-%m-%d %H:%M:%S}",
            row.hour,
            row.day,
            row.week,
            row.month,
            row.year,
            row.weekday,
        )
        time_vals = [str(col) for col in time_vals]
        cur.execute(sql.time_table_insert, time_vals)

        user_vals = (row.userId, row.firstName, row.lastName, row.gender, row.level)
        cur.execute(sql.user_table_insert, user_vals)

        # get songid and artistid from song and artist tables
        cur.execute(sql.song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        cur.execute(
            sql.songplay_table_insert,
            (
                f"{row.ts:%Y-%m-%d %H:%M:%S}",
                str(row.userId),
                str(row.level),
                str(songid),
                str(artistid),
                str(row.sessionId),
                str(row.location),
                str(row.userAgent),
            ),
        )


def process_data(cur: cursor, filepath: str, func: Callable):
    """Process files on a given path using a given function

    Args:
        cur (cursor): Conected cursor
        filepath (str): Path for a json file
        func (Callable): ETL funcion
    """
    # get all files matching extension from directory
    all_files = list(get_files(filepath))

    # get total number of files found
    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        print(f"{i}/{num_files} files processed.")


def main():
    with get_connection() as cur:
        process_data(cur, filepath="data/song_data", func=process_song_file)
        process_data(cur, filepath="data/log_data", func=process_log_file)

        cur.execute(
            """UPDATE artists SET "location" = NULL WHERE "location" IN ('', 'NULL', 'NaN');
               UPDATE artists SET "latitude" = NULL WHERE "latitude" = 'NaN';
               UPDATE artists SET "longitude" = NULL WHERE "longitude" = 'NaN';
               UPDATE songplays SET "song_id" = NULL WHERE "song_id" = 'None';
               UPDATE songplays SET "artist_id" = NULL WHERE "artist_id" = 'None';
               """
        )


if __name__ == "__main__":
    main()