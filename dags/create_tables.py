import boto3
import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries, insert_table_queries
from data_to_s3 import get_the_lastest_added
from data_to_s3 import dag_path

def drop_tables(cur, conn):
    """
    this function will drop any old tables in the RDS
    
    cur: is the cursoer to  execute commands
    conn: the connection to the postgresql database
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
    return True

def create_tables(cur, conn):
    """
    this function will create the tables in the RDS
    
    cur: is the cursoer to  execute commands
    conn: the connection to the postgresql database
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
    return True

def insert_to_tables(cur, conn):
    """
    this function will create the tables in the RDS
    
    cur: is the cursoer to  execute commands
    conn: the connection to the postgresql database
    """

    if not create_tables(cur,conn):# to check if the tables are created or not
        create_tables(cur,conn)
    else:
        last_added = get_the_lastest_added()
        print(last_added)
        taking_data_from_s3= open(dag_path+'/processed_data/'+last_added, 'r')
        print(taking_data_from_s3)
        try:
            cur.copy_from(taking_data_from_s3, 'staging_surf_report', sep=",") #using copy_from to insert data to staging_surf_report
            print("Data inserted using copy_from_datafile() successfully....")  
        except (Exception, psycopg2.DatabaseError) as err:
            print(psycopg2.DatabaseError)
            print(Exception)
            show_psycopg2_exception(err)
            cur.close()
        conn.commit()



        for query in insert_table_queries:
            cur.execute(query)
            conn.commit()
    
def main():
    """
    this function read the credentials in dwh.cfg file
    
    dwh.cfg: file will have the credentials for the cluster and IAM role
    cur: is the cursoer to  execute commands
    conn: the connection to the postgresql database
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)
    insert_to_tables(cur,conn)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()