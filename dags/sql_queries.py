
# DROP TABLES if existed

staging_surf_report_table_drop = "DROP table IF EXISTS staging_surf_report"
tides_table_drop = "DROP table IF EXISTS tides"

# CREATE TABLES

staging_surf_report_table_create = ("""CREATE TABLE IF NOT EXISTS staging_surf_report(
                                timestamp TIMESTAMP PRIMARY KEY,
                                surf_min INTEGER,
                                surf_max INTEGER,
                                surf_optimalScore INTEGER,
                                surf_plus BOOL,
                                surf_humanRelation VARCHAR(255),
                                surf_raw_min NUMERIC,
                                surf_raw_max NUMERIC,
                                speed NUMERIC,
                                direction NUMERIC,
                                directionType VARCHAR(255),
                                gust NUMERIC,
                                optimalScore INTEGER,
                                temperature NUMERIC,
                                condition VARCHAR(255)
                        )
                """)

tides_table_create = ("""CREATE TABLE IF NOT EXISTS tides(
                                tide_timestamp TIMESTAMP PRIMARY KEY,
                                tide_type VARCHAR(255),
                                height NUMERIC
    )
""")


# FINAL TABLES

surf_report_insert = ("""
        INSERT INTO surf_report
      (timestamp, surf_min,surf_max,surf_optimalScore,surf_plus,surf_humanRelation,surf_raw_min,surf_raw_max,speed,direction,directionType,gust,optimalScore,temperature,condition)
        SELECT *
    FROM staging_surf_report
        WHERE NOT EXISTS(SELECT timestamp
                    FROM surf_report 
                   WHERE staging_surf_report.timestamp = surf_report.timestamp);""")

# QUERY LISTS

create_table_queries = [staging_surf_report_table_create, tides_table_create]
drop_table_queries = [staging_surf_report_table_drop, tides_table_drop]
insert_table_queries = [surf_report_insert]