import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')



# DROP TABLES if existed

staging_surf_report_table_drop = "DROP table IF EXISTS staging_surf_report"
staging_tides_table_drop = "DROP table IF EXISTS staging_tides"

# CREATE TABLES

staging_surf_report_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events(
                                artist varchar,
                                auth varchar,
                                firstName varchar,
                                gender varchar,
                                itemInSession int,
                                lastName varchar,
                                length float,
                                level varchar,
                                location varchar,
                                method varchar,
                                page varchar,
                                registration float,
                                sessionId int,
                                song varchar,
                                status int,
                                ts timestamp,
                                userAgent varchar,
                                userId int
    )
""")

staging_tides_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs(
                                num_songs int,
                                artist_id varchar,
                                artist_latitude float,
                                artist_longitude float,
                                artist_location varchar,
                                artist_name varchar,
                                song_id varchar,
                                title varchar,
                                duration float,
                                year int
    )
""")

# load the from the API to s3

staging_surf_report_table_copy = (
    """
    COPY staging_events
    FROM {} 
    iam_role {}
    JSON {}
    REGION 'us-west-2'
    TIMEFORMAT as 'epochmillisecs';
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_tides_table_copy = (
    """
    COPY staging_songs
    FROM {} 
    iam_role {}
    FORMAT AS JSON 'auto'
    REGION 'us-west-2';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])


# STAGING TABLES from the s3 to s3 after analysis

staging_surf_report_table_copy = (
    """
    COPY staging_events
    FROM {} 
    iam_role {}
    JSON {}
    REGION 'us-west-2'
    TIMEFORMAT as 'epochmillisecs';
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_tides_table_copy = (
    """
    COPY staging_songs
    FROM {} 
    iam_role {}
    FORMAT AS JSON 'auto'
    REGION 'us-west-2';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])




# FINAL TABLES

songplay_table_insert = ("""INSERT INTO fact_songplay(start_time, user_id,level, song_id, artist_id, session_id, location, user_agent)
                                SELECT DISTINCT ste.ts, ste.userId , ste.level,
                                sts.song_id,sts.artist_id,ste.sessionId,
                                sts.artist_location,ste.userAgent 
                                FROM staging_events ste 
                                JOIN staging_songs sts
                                ON ste.song = sts.title AND ste.length = sts.duration 
                                AND ste.artist = sts.artist_name;
                       
                        
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_tides_table_create]
drop_table_queries = [staging_events_table_drop, staging_tides_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert]