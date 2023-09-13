# austock-price-predict
A website forecasts the stock prices in Australian stock market

## Acknowledges
I planned to implement this project 2 years ago, when I still studied my second year in Vietnam and I did, however, in that time, this website was very basic and most of the code was from another repo. Thus now I try to make a new one which would be more functionable and has more features.

This is not an article at all, however, I want to give more details about all the stages of this project such as my initial plan, problems I face with, how I solve them, and so on. Because currently I am studying Project Management subject, therefore I aspire to apply all skills I learn, and one of the most important task in PM (project management) is documentating. Now, let's start!

## Developing Process
In the beginning, I planned to make a stock price predicting website which includes a stimulated trading bot, but I relized that this plan had lack of detail and there were a lot of questions I must answer first:
- How many stock I want to analyze?
  - I think around 20 is a good number.
- Which market?
  - I am studying in Australia, so ASX20 would be a great choice.
- How can I get trading data of these stocks?
- How should I perform EDA and what ML technique I should use?
- What I know about trading bot? How will it work?

I found some interesting [article](https://medium.com/codex/build-a-stocks-price-prediction-app-powered-by-snowflake-aws-python-and-streamlit-part-1-of-3-c304a8b3e319) on Medium, however, it has some problems. It tends to develop a data warehouse in Snowflake which I have no idea and experience and it's not really related to Data Science field, moreover, it's not free so I decide to change a little bit from that project:
- Develop a database but not a data warehouse.
- Scrap data of Australian stock markets.
- Develop a trading bot which I found another article 

## Project Layout
1. Data collection: Automatically download the stock historical prices data in CSV format and save it to the AWS S3 bucket.
   - Create a S3 Bucket to store data.
   - Write Python code to pull stock price history using Yahoo Finance API and store .csv file. In my case, I store in the local machine because the file is light and we just do it once for history data. Then I push this file to S3 bucket.
   - Create a Database in RDS to store data and push the .csv file in S3 to create a table. I found an useful [tutorial](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PostgreSQL.S3Import.html#USER_PostgreSQL.S3Import.Overview).  
   - Create a Lambda Layer (package management for Lambda) for Lambda Function.
   - Write Lambda Function to push update data to S3 Bucket.
   - Transfer data from S3 Bucket to Lambda.
   - Store data in AWS RDS. 
2. Data Extraction, Preprocessing & EDA: Extract & Pre-process the data using Python and perform basic Exploratory Data Analysis.
   - Clean data: check null, duplicated.
   - Perform Time Series Analysis.
     - Trends.
     - Seasonalities.
     - Cyclic.
   - Features Engineering.
     - Lags.
     - Day, Year.
3. Machine Learning Model development: Develop a machine learning model, Train the model on historical data, Evaluate the model and perform hyperparameter fine-tune. I perform all of them on stock_price_preprocessed.csv.
   - Split data into training set and testing set.
   - Select the appropriate model, loss function.
   - Train model and predict.
   - Validate and select the best model. I have a problem that my model is a custom hybrid model so I have to create `fit`, `predict`, `save`, `load` function by myself. This [article](https://towardsdatascience.com/hybrid-rule-based-machine-learning-with-scikit-learn-9cb9841bebf2) would be helpful. Or on the easier way, use joblib. I save final_model.pkl here.
4. Machine Learning Model deployment: Deploy the final model on EC2.
  - Develop a Streamlit app locally.
  - Push the app on a EC2 instance.
5. Trading Bot development: Develop a trading bot, design profitable strategy.
6. Web App Development: Build a web app using Streamlit and Python to interact with the deployed model and display the predictions. And Deploy the final app on Streamlit Cloud.
