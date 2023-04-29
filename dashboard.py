import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  
from datetime import date
import datetime
import psycopg2
import os
from dags.sql_queries import select_all_surf_report,select_all_tides


app = Dash(__name__)

conn = psycopg2.connect(
   database="", user='', password='', host='', port= ''
)
cursor = conn.cursor()



cursor.execute(select_all_surf_report)
surf_report = cursor.fetchall()

cursor.execute(select_all_tides)
tides_report = cursor.fetchall()

columns_surf = ['id',
            'probability' ,
            'surf_min' ,
            'surf_max' ,
            'surf_optimalScore' ,
            'surf_plus' ,
            'surf_humanRelation' ,
            'surf_raw_min' ,
            'surf_raw_max' ,
            'speed',
            'direction',
            'directionType',
            'gust',
            'optimalScore',
            'temperature',
            'condition']

surf_df = pd.DataFrame(surf_report,columns=columns_surf)
print(surf_df)
columns_tides = ['timestamp','tide','height']

tides_df = pd.DataFrame(tides_report,columns=columns_tides)
print(tides_df)
today = date.today()

#date_list to get the date of the past seven days
date_list = [today - datetime.timedelta(days=x) for x in range(7)]

water_height_list = ['NIGHT_MOSTLY_CLOUDY','NIGHT_MIST','MIST','CLEAR','MOSTLY_CLOUDY']

app.layout =  html.Div([

    html.H1("Surf Report", style={'text-align': 'center'}),


    dcc.Dropdown(id="slct_day",
                 options=[
                     {"label": date_list[0], "value": date_list[0]},
                     {"label": date_list[1], "value": date_list[1]},
                     {"label": date_list[2], "value": date_list[2]},
                     {"label": date_list[3], "value": date_list[3]},
                     {"label": date_list[3], "value": date_list[3]},
                     {"label": date_list[4], "value": date_list[4]},
                     {"label": date_list[5], "value": date_list[5]},
                     {"label": date_list[6], "value": date_list[6]}],
                 multi=False,
                 value=date_list[0],
                 style={'width': "40%"}
                 ),
    dcc.Dropdown(id="slct_condition",
                 options=[
                     {"label": water_height_list[0], "value": water_height_list[0]},
                     {"label": water_height_list[1], "value": water_height_list[1]},
                     {"label": water_height_list[2], "value": water_height_list[2]},
                     {"label": water_height_list[3], "value": water_height_list[3]},
                     {"label": water_height_list[4], "value": water_height_list[4]},
                     ],
                 multi=False,
                 value=water_height_list[0],
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='surfing_figure', figure={}),
    dcc.Graph(id='tides_figure', figure={})

])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='tides_figure', component_property='figure'),
     Output(component_id='surfing_figure', component_property='figure')],
    [Input(component_id='slct_day', component_property='value'),
     Input(component_id='slct_condition', component_property='value')]
)
def update_graph(option_slctd,option_slctc):
    

    if option_slctd  is None: 
        container = "No Date selected"
        option_slctd = str(date_list[0])
        container = "Date selected: {}".format(option_slctd)
    else: 
        container = "Date selected: {}".format(option_slctd)
    


    surf_filter = surf_df.copy()
    surf_filter = surf_filter[surf_filter["condition"] == option_slctc]

    tides_filter = tides_df.copy()
    tides_filter['timestamp'] = pd.to_datetime(tides_filter['timestamp'], unit='s')
    tides_filter = tides_filter[(tides_filter['timestamp'] > pd.to_datetime(option_slctd)) & (tides_filter['timestamp'] <= pd.to_datetime(option_slctd)+ pd.DateOffset(days=1))] 


    # Plotly Express
    fig1 = px.bar(surf_filter, x='temperature', y='speed' ,text="condition" )
    

    fig2 = px.line(tides_filter,x="timestamp",y="height",text="tide")
    fig2.update_traces(textposition='top center')
    return container,fig1,fig2












if __name__ == '__main__':
    app.run_server(debug=True)