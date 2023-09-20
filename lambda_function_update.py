import os
import boto3
import sqlalchemy
import tempfile
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
    csv_file = get_latest_file()
    
    engine = sqlalchemy.create_engine()