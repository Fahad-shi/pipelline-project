
# DROP TABLES if existed

staging_surf_report_table_drop = "DROP table IF EXISTS staging_surf_report"
surf_report_table_drop = "DROP table IF EXISTS surf_report"
staging_tides_table_drop = "DROP table IF EXISTS staging_tides"
tides_table_drop = "DROP table IF EXISTS tides"
# CREATE TABLES

staging_surf_report_table_create = ("""CREATE TABLE IF NOT EXISTS staging_surf_report(
                                id VARCHAR(255) PRIMARY KEY,
                                probability VARCHAR(255) ,
                                surf_min FLOAT,
                                surf_max FLOAT,
                                surf_optimalScore FLOAT,
                                surf_plus BOOL,
                                surf_humanRelation VARCHAR(255),
                                surf_raw_min NUMERIC,
                                surf_raw_max NUMERIC,
                                speed NUMERIC,
                                direction NUMERIC,
                                directionType VARCHAR(255),
                                gust NUMERIC,
                                optimalScore FLOAT,
                                temperature NUMERIC,
                                condition VARCHAR(255)
                        )
                """)

surf_report_table_create = ("""CREATE TABLE IF NOT EXISTS surf_report(
                                id VARCHAR(255)  PRIMARY KEY,
                                probability VARCHAR(255),
                                surf_min FLOAT,
                                surf_max FLOAT,
                                surf_optimalScore FLOAT,
                                surf_plus BOOL,
                                surf_humanRelation VARCHAR(255),
                                surf_raw_min NUMERIC,
                                surf_raw_max NUMERIC,
                                speed NUMERIC,
                                direction NUMERIC,
                                directionType VARCHAR(255),
                                gust NUMERIC,
                                optimalScore FLOAT,
                                temperature NUMERIC,
                                condition VARCHAR(255)
                        )
                """)


staging_tides_table_create = ("""CREATE TABLE IF NOT EXISTS staging_tides(
                                tide_timestamp BIGINT  PRIMARY KEY,
                                tide_type VARCHAR(255),
                                height NUMERIC
    )
""")

tides_table_create = ("""CREATE TABLE IF NOT EXISTS tides(
                                tide_timestamp BIGINT  PRIMARY KEY,
                                tide_type VARCHAR(255),
                                height NUMERIC
    )
""")



# FINAL TABLES

surf_report_insert = ("""
        INSERT INTO surf_report
      (id,probability, surf_min,surf_max,surf_optimalScore,surf_plus,surf_humanRelation,surf_raw_min,surf_raw_max,speed,direction,directionType,gust,optimalScore,temperature,condition)
        SELECT *
    FROM staging_surf_report
        WHERE NOT EXISTS(SELECT id
                    FROM surf_report 
                   WHERE staging_surf_report.id = surf_report.id);""")

tides_table_insert = ("""

        INSERT INTO tides(tide_timestamp,tide_type,height)
        SELECT * FROM staging_tides WHERE NOT EXISTS(SELECT tide_timestamp
                                                      FROM tides 
                                                      WHERE staging_tides.tide_timestamp = tides.tide_timestamp);


""")




select_all_surf_report = ("""
                          select * from surf_report;
""")

select_all_tides = ("""
                    select * from tides;
""")

# QUERY LISTS

create_table_queries = [staging_surf_report_table_create,surf_report_table_create,staging_tides_table_create, tides_table_create]
drop_table_queries = [staging_surf_report_table_drop,surf_report_table_drop,staging_tides_table_drop, tides_table_drop]
insert_table_queries = [surf_report_insert,tides_table_insert]