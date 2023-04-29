Project Name: Surfline Dashboard Project

Brief description of the project: 
This is an end-to-end data engineering project that involves retrieving data from Pysurfline API, making necessary changes, and then loading it to an S3 bucket. Afterward, the data is loaded to an AWS RDS instance, and then we connect to the RDS to retrieve the data to create a dashboard using Dash.

Table of Contents: 
- Technologies 
- Features 
- Getting Started 
- Installation 
- Usage 
- learning resources
- Acknowledgements 

Technologies: 
- Apache Airflow 
- Python 
- Docker 
- AWS RDS 
- Dash 

Features: 
- Retrieves data from Pysurfline API
- Performs necessary changes to data
- Loads data to an S3 bucket 
- Loads data to an AWS RDS instance 
- Connects to RDS to retrieve data for creating a dashboard using Dash 

Getting Started: 
To get started with this project, you need to clone the repository to your local machine. You will also need to set up the necessary environment variables to connect to the AWS RDS instance and S3 bucket. 

Installation: 
To install this project, you will need to follow the following steps:
1. Clone the repository to your local machine
2. Install the necessary dependencies and packages by running `docker-compose build` after that `docker-compose up`
3. Set up the environment variables to connect to the AWS RDS instance and S3 bucket or you set them up in Apache Airflow -> admin -> connections

Usage: 
To use this project, you will need to:
1. Run the DAG in Airflow to retrieve the data from Pysurfline API, perform necessary changes, and load it to S3 and RDS
2. Connect to the RDS instance to retrieve the data and create a dashboard using Dash 




learning resources:
- <a href ="https://www.youtube.com/watch?v=hSPmj7mK6ng">Introduction to Plotly</a>
- <a href= "https://www.youtube.com/watch?v=aTaytcxy2Ck"> Running Airflow 2.0 with Docker in 5 mins</a>

Acknowledgements: 
I would like to acknowledge the following resources and people for their help or inspiration:
- Pysurfline API for providing the surf data
- Apache Airflow for providing a framework for creating data pipelines
- AWS RDS for providing a managed relational database service
- Dash for providing a framework for building interactive web-based dashboards.
