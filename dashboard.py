import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from datetime import date
import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
import os
from dags.sql_queries import select_all_surf_report,select_all_tides

hook = PostgresHook(postgres_conn_id = 'RDS_conn')

conn = hook.get_conn()
cursor = hook.cursor

print(select_all_surf_report)
cursor.execute(select_all_surf_report)
conn.commit()
