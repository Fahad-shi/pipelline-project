from airflow.providers.postgres.hooks.postgres import PostgresHook
from sql_queries import create_table_queries, drop_table_queries

def drop_tables():
    """
    this function will drop any old tables in the RDS
    """
    hook = PostgresHook(postgres_conn_id='RDS_conn')
    for query in drop_table_queries:
        hook.run(query)
    return True

def create_tables():
    """
    this function will create the tables in the RDS
    """
    hook = PostgresHook(postgres_conn_id='RDS_conn')
    for query in create_table_queries:
        hook.run(query)
    return True
    
def main_create():
    """
    This function reads the credentials in the dwh.cfg file
    """
    drop_tables()
    create_tables()

if __name__ == "__main__":
    main_create()
