import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import boto3
import csv
from io import StringIO

TICKER = 'ANZ.AX'
end = datetime.now()
start = end - timedelta(days=365*5+1)

def upload_csv_s3(dataframe,s3_bucket_name,csv_file_name):

    # creating s3 client connection
    client = boto3.client('s3')

    # placing file to S3, yf return a dataframe so we convert to csv file
    client.put_object(Body=dataframe.to_csv(), Bucket=s3_bucket_name, Key=csv_file_name)
    print('Done uploading to S3')
    
def lambda_handler(event, context):
    stock_prices = yf.download('ANZ.AX',start, end)
    table_data = stock_prices
    table_rows = len(table_data)

    #create csv and upload in s3 bucket
    dt_string = datetime.now().strftime("%Y-%m-%d_%H%M")
    csv_file_name =  TICKER+'_' +dt_string +'.csv'
    upload_csv_s3(table_data,'au-stock-price',csv_file_name)

    response = {
        "Rows": table_rows,
        "body": table_data.to_dict(orient='records')
    }

    return response
    
if __name__ == "__main__":
    lambda_handler(None, None)