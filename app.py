import streamlit as st
from datetime import date
# from . import credentials
import pandas as pd

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

# import psycopg2
import sys
import boto3
import os
import json
import sqlalchemy

# Load credential
credential_file = open('credentials.json')
credentials = json.load(credential_file)


# Get data from yfinance API

START = "2013-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast App')

stocks = ('ANZ', 'BHP', 'CBA', 'CSL', 'FMG', 'GMG', 'MQG', 'NAB', 'NCM', 'REA', 'RIO', 'TLS', 'WBC', 'WES', 'WOW', 'XRO')
selected_stock = st.selectbox('Select dataset for prediction', stocks)

n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365


@st.cache_data
def load_data(ticker):
    ticker = ticker + '.AX'
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

# Get data from RDS PostgreSQL

# engine = psycopg2.connect(
# 	database=credentials['rds_database'],
# 	user=credentials['rds_user'],
# 	password=credentials['rds_password'],
# 	host=credentials['rds_host'],
# 	port=credentials['rds_port']
# )

database=credentials['rds_database']
user=credentials['rds_user']
password=credentials['rds_password']
host=credentials['rds_host']
port=credentials['rds_port']
db_url = f'postgresql://{user}:{password}@{host}:5432/{database}'
engine = sqlalchemy.create_engine(db_url)

@st.cache_data
def load_data_from_rds(ticker):
	table = 'stock_price'
	query = f"SELECT * FROM {table} WHERE Ticker = (SELECT Id FROM ticker WHERE Code = '{ticker}');"
	df = pd.read_sql(query, engine)
	return df

# Load data

data_load_state = st.text('Loading data...')
# data = load_data(selected_stock)
# data_load_state.text('Loading data... done!')
data = load_data_from_rds(selected_stock)
data_load_state.text('Loading data from RDS... done!')

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	# fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['date'], y=data['adj_close'], name="stock_adj_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['date','adj_close']]
df_train = df_train.rename(columns={"date": "ds", "adj_close": "y"})

m = Prophet(changepoint_prior_scale=0.005,
                     seasonality_prior_scale=0.03,
                     changepoint_range=1,
                     seasonality_mode='multiplicative')
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())
    
st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)

engine.dispose()