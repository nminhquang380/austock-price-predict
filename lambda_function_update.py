import os
import boto3
import sqlalchemy
import re

def get_latest_file():
    s3 = boto3.client('s3')
    bucket_name = 'au-stock-price'
    
    # List objects in bucket
    object_list = s3.list_objects_v2(Bucket=bucket_name)
    
    # Check if there are any objects in bucket
    if 'Contents' in object_list:
        # Find the object with the latest LastModified timestamp
        latest_object = max(object_list['Contents'], key=lambda obj: obj['LastModified'])

        # Extract the filename
        filename = latest_object['Key']
        if re.match(r'^update_data_.*\.csv$', filename):
            return filename
    
    return None
        

def lambda_handler(event, context):
    # Get latest filename
    csv_file = get_latest_file()
    
    # Check the newest csv file
    if csv_file:
        # Connect to engine
        db_url = 'postgresql://<user>:<password>@<host>:5432/<database>'
        engine = sqlalchemy.create_engine(db_url)
        
        connection = engine.connect()
        
        insert_data_query = sqlalchemy.text(f"""
        SELECT aws_s3.table_import_from_s3(
        'stock_price', 'Date,Open,High,Low,Close,Adj_Close,Volume,Ticker,Day_of_year,Year,Lag_1,Lag_2', '(format csv, header true)',
        'au-stock-price',
        '{csv_file}',
        'ap-southeast-2',
        'YOUR-ACCESS-KEY', 'YOUR-SECRET-KEY'
        );
        """)

        connection.execute(insert_data_query)

        connection.close()
        