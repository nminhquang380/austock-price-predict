import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import boto3
import csv
from io import StringIO
# from sklearn.preprocessing import LabelEncoder

TICKERS = ['ANZ', 'BHP', 'CBA', 'CSL', 'FMG', 'GMG', 'MQG', 'NAB', 'NCM', 'REA', 'RIO', 'TLS', 'WBC', 'WES', 'WOW', 'XRO']
END = datetime.now()
START = END - timedelta(days=7)
# encoder = LabelEncoder()
# encoder.fit(TICKERS)

class LabelEncoder:
    def __init__(self):
        self.label_to_code = {}
        self.code_to_label = {}
        self.next_code = 0

    def fit(self, labels):
        for label in labels:
            if label not in self.label_to_code:
                self.label_to_code[label] = self.next_code
                self.code_to_label[self.next_code] = label
                self.next_code += 1

    def transform(self, labels):
        return [self.label_to_code[label] for label in labels]

    def inverse_transform(self, codes):
        return [self.code_to_label[code] for code in codes]
        
encoder = LabelEncoder()
encoder.fit(TICKERS)

def get_stock_prices(tickers, start, end):
    data = pd.DataFrame()
    for ticker in tickers:
        df_temp = yf.download(ticker+'.AX', start, end)
        df_temp['Ticker'] = ticker
        df_temp = df_temp.reset_index()
        data = pd.concat([data, df_temp])
        
    data["Day_of_year"] = data.Date.dt.dayofyear
    data["Year"] = data.Date.dt.year
    data['Lag_1'] = data['Adj Close'].shift(1)
    data['Lag_2'] = data['Adj Close'].shift(2)
    data['Date'] = data['Date'].astype(str)
    data.fillna(0, inplace=True)
    
    data['Ticker'] = encoder.transform(data['Ticker'])
    
    return data

def upload_csv_s3(dataframe,s3_bucket_name,csv_file_name):

    # creating s3 client connection
    client = boto3.client('s3')

    # placing file to S3, yf return a dataframe so we convert to csv file
    client.put_object(Body=dataframe.to_csv(index=False), Bucket=s3_bucket_name, Key=csv_file_name)
    print('Done uploading to S3')
    
def lambda_handler(event, context):
    table_data = get_stock_prices(TICKERS, START, END)
    table_rows = len(table_data)

    #create csv and upload in s3 bucket
    dt_string = datetime.now().strftime("%Y-%m-%d_%H%M")
    csv_file_name =  dt_string +'.csv'
    upload_csv_s3(table_data,'au-stock-price',csv_file_name)

    response = {
        "Rows": table_rows,
        "body": table_data.to_dict(orient='records')
    }

    return response
    
if __name__ == "__main__":
    lambda_handler(None, None)