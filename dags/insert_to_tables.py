import psycopg2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sql_queries import create_table_queries, drop_table_queries, insert_table_queries
from data_to_s3 import get_the_lastest_added

def insert_to_tables():
    """
    this function will create the tables in the RDS
    
    cur: is the cursoer to  execute commands
    conn: the connection to the postgresql database
    """
    hook = PostgresHook(postgres_conn_id="RDS_conn")

    last_added = get_the_lastest_added()
    print(last_added)
    directory = 'C:\\surfing_dashboard_project\\processed_data\\'
    taking_data_from_s3= open(directory+last_added, 'r')
    print(taking_data_from_s3)

    try:
        with hook.get_conn() as conn:
            with conn.cursor() as cur:
                cur.copy_from(taking_data_from_s3, 'staging_surf_report', sep=",") #using copy_from to insert data to staging_surf_report
                print("Data inserted using copy_from_datafile() successfully....")
                for query in insert_table_queries:
                    cur.execute(query)
                    conn.commit()
    except (Exception, psycopg2.DatabaseError):
        print(psycopg2.DatabaseError)
        print(Exception)
        cur.close()

def main_insert():
    insert_to_tables()