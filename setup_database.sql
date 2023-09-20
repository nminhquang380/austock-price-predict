drop table stock_price;

create table stock_price (
id int GENERATED ALWAYS AS identity primary key,
Date varchar(120),
Open float,
High float,
Low float,
Close float,
Adj_Close float,
Volume int,
Ticker int,
Day_of_year int,
Year int,
Lag_1 float,
Lag_2 float
);

SELECT aws_s3.table_import_from_s3(
'stock_price', 'Date,Open,High,Low,Close,Adj_Close,Volume,Ticker,Day_of_year,Year,Lag_1,Lag_2', '(format csv, header true)',
'au-stock-price',
'stock_price_preprocessed.csv',
'ap-southeast-2',
'YOUR-ACCESS-KEY', 'YOUR-SECRET-KEY'
);

alter table stock_price alter column Date type date
using to_date(Date, 'DD/MM/YYYY');

drop table ticker;

create table ticker (
Id int primary key,
Code varchar(5),
Company_name varchar(200)
);

SELECT aws_s3.table_import_from_s3(
'ticker', 'Code,Company_name,Id', '(format csv, header true)',
'au-stock-price',
'ticker_data.csv',
'ap-southeast-2',
'YOUR-ACCESS-KEY', 'YOUR-SECRET-KEY'
);

ALTER TABLE stock_price 
ADD CONSTRAINT fk_ticker_id
FOREIGN KEY (Ticker)
REFERENCES ticker (Id);
