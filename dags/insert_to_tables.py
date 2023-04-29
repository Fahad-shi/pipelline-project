import psycopg2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sql_queries import create_table_queries, drop_table_queries, insert_table_queries
from data_to_s3 import get_the_latest_added
import boto3
from airflow.models import Variable
from io import StringIO


import csv

def insert_to_tables():
    """
    this function will create the tables in the RDS
    
    cur: is the cursor to execute commands
    conn: the connection to the postgresql database
    """
    hook = PostgresHook(postgres_conn_id="RDS_conn")
    
    last_added_tides = get_the_latest_added('tides.csv')
    print(last_added_tides)

    last_added_surf = get_the_latest_added('surf-report.csv')
    print(last_added_surf)
    s3 = boto3.resource('s3',
        aws_access_key_id=Variable.get('aws_access_key_id'),
        aws_secret_access_key=Variable.get('aws_secret_access_key')
    )
    bucket = s3.Bucket('surfingbucket')
    obj = bucket.Object(last_added_tides)
    taking_data_from_s3_tides= obj.get()['Body'].read().decode('utf-8')

    bucket = s3.Bucket('surfingbucket')
    obj = bucket.Object(last_added_surf)
    taking_data_from_s3_surf= obj.get()['Body'].read().decode('utf-8')
    
    try:
        with hook.get_conn() as conn:
            with conn.cursor() as cur:
                # skip the first line of the CSV file
                tides_data = csv.reader(StringIO(taking_data_from_s3_tides))
                next(tides_data)
                surf_data = csv.reader(StringIO(taking_data_from_s3_surf))
                next(surf_data)
                
                # pass the rest of the data to the copy_from method
                cur.copy_from(StringIO('\n'.join(['\t'.join(row) for row in tides_data])), 'staging_tides', sep='\t')
                cur.copy_from(StringIO('\n'.join(['\t'.join(row) for row in surf_data])), 'staging_surf_report', sep='\t')
                
                print("Data inserted using copy_from_datafile() successfully....")
                
                for query in insert_table_queries:
                    cur.execute(query)
                    conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error occurred: {error}")
        cur.close()


def main_insert():
    insert_to_tables()