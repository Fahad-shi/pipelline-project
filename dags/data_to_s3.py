import pysurfline 
from datetime import date
import os
from airflow.models import Variable
import boto3
import pandas as pd
import uuid

## dowload the data
def download_data_from_source():
    params = {
    "spotId": "5842041f4e65fad6a77087f9",  # Spot ID for Huntington Beach
    "days": 1,
    "intervalHours": 1,
}

    today = date.today()
    surfdate = today.strftime("%d-%m-%y")
    report = pysurfline.SurfReport(params)

    forecast = pysurfline.core.ForecastGetter('tides', params)
    tides_report = forecast.response.json()['data']
    tides_df = pd.DataFrame(tides_report)
    # Normalize the 'tides' column

    tides_df = pd.concat([tides_df.drop(['tides'], axis=1), pd.json_normalize(tides_df['tides'])], axis=1)
    tides_df = tides_df.drop(columns='utcOffset')
    
    
    
    surf_report = report.df.drop(columns=['utcOffset', 'swells','pressure'])
    id_column = [uuid.uuid4().hex for _ in range(len(surf_report))]
    surf_report.insert(0, 'id', id_column)

    directory = 'C:\\surfing_dashboard_project\\raw-data\\'
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        surf_report.to_csv(directory + surfdate + '-surf-report.csv', sep='\t', index=False)
        tides_df.to_csv(directory + surfdate + '-tides.csv', sep='\t', index=False)


def load_s3_data():
    today = date.today()
    surfdate = today.strftime("%d-%m-%y")
    s3 = boto3.client(
        's3',
        aws_access_key_id=Variable.get('aws_access_key_id'),
        aws_secret_access_key=Variable.get('aws_secret_access_key')
    )
    directory = 'C:\\surfing_dashboard_project\\raw-data\\'
    try:
        s3.upload_file(directory+ surfdate +'-surf-report.csv','surfingbucket',surfdate +'-surf-report.csv')
        s3.upload_file(directory+ surfdate +'-tides.csv','surfingbucket',surfdate +'-tides.csv')
    except Exception as e:
        print(e)
        raise e


def get_the_latest_added(filename):
    s3 = boto3.client(
        's3',
        aws_access_key_id=Variable.get('aws_access_key_id'),
        aws_secret_access_key=Variable.get('aws_secret_access_key')
    )
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s')) # lambda function to get the last modified 
    
    objs = s3.list_objects_v2(Bucket='surfingbucket')['Contents']
    filtered_objs = [obj for obj in objs if obj['Key'].endswith(filename)]
    
    if filtered_objs:
        last_added = sorted(filtered_objs, key=get_last_modified)[-1]['Key']
        return last_added
    else:
        raise Exception(f"No objects found in S3 bucket with filename {filename}")


