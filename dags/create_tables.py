import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    this function will drop any old tables in the cluster
    
    cur: is the cursoer to  execute commands
    conn: the connection to the postgresql database
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    this function will create the tables in the cluster
    
    cur: is the cursoer to  execute commands
    conn: the connection to the postgresql database
    """
    for query in create_table_queries:
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
    print('hello')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()