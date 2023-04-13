from pysurfline import SurfReport
import boto3
from datetime import date
import os

dag_path = os.getcwd()

## dowload the data
def download_data():
    params = {
    "spotId": "5842041f4e65fad6a77087f9",  # Spot ID for Huntington Beach
    "days": 1,
    "intervalHours": 1,
}

    today = date.today()
    surfdate = today.strftime("%d-%m-%y")

    report = SurfReport(params)
    print(report.api_log)

    surf_report = report.df.drop(columns=['utcOffset', 'swells'])
    surf_report.to_csv(dag_path+'/raw-data/' + surfdate + '-surf-report', sep='\t', index=False)




def load_s3_data():
    today = date.today()
    surfdate = today.strftime("%d-%m-%y")
    S3 = boto3.client('s3')
    S3.meta.client.upload_file(dag_path+'/raw_data/'+ surfdate +'-surf-report.csv','surfingbucket',surfdate +'-surf-report.csv')

def get_the_lastest_added():
    S3 = boto3.client('s3')
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s')) # lamda funtion to get the las modified 

    objs = S3.list_objects_v2(Bucket='surfingbucket')['Contents']
    last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][-1]
    return last_added


def download_s3_data():
    S3 = boto3.client('s3')
    last_added = get_the_lastest_added()
    S3.Bucket('surfingbucket').download_file(last_added,dag_path+'/processed_data/'+last_added)


