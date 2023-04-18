import pysurfline 
from datetime import date
import os
from airflow.models import Variable
import boto3


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
    print(report.api_log)

    surf_report = report.df.drop(columns=['utcOffset', 'swells'])

    directory = 'C:\\surfing_dashboard_project\\raw-data\\'
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    surf_report.to_csv(directory + surfdate + '-surf-report.csv', sep='\t', index=False)



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

    except Exception as e:
        print(e)
        raise e


def get_the_lastest_added():
    s3 = boto3.client(
        's3',
        aws_access_key_id=Variable.get('aws_access_key_id'),
        aws_secret_access_key=Variable.get('aws_secret_access_key')
    )
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s')) # lambda function to get the last modified 

    objs = s3.list_objects_v2(Bucket='surfingbucket')['Contents']
    last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][-1]
    return last_added


def download_s3_data():
    s3 = boto3.client(
        's3',
        aws_access_key_id=Variable.get('aws_access_key_id'),
        aws_secret_access_key=Variable.get('aws_secret_access_key')
    )
    directory = 'C:\\surfing_dashboard_project\\processed_data\\'
    last_added = get_the_lastest_added()
    s3.download_file('surfingbucket',last_added,directory+last_added)


