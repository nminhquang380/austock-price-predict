# austock-price-predict
A website forecasts the stock prices in Australian stock market.

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
- Develop a trading bot which I found another article.

## Project Layout
1. Data collection: Automatically download the stock historical prices data in CSV format and save it to the AWS S3 bucket.
   - Create a S3 Bucket to store data.
   - Write Python code to pull stock price history using Yahoo Finance API and store .csv file. In my case, I store in the local machine because the file is light and we just do it once for history data. Then I push this file to S3 bucket.
   - Create a Database in RDS to store data and push the .csv file in S3 to create a table. I found an useful [tutorial](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PostgreSQL.S3Import.html#USER_PostgreSQL.S3Import.Overview).  
   - Create a Lambda Layer (package management for Lambda) for Lambda Function. This [link](https://aws.plainenglish.io/monitoring-apples-stock-prices-with-aws-lambda-cloudwatch-and-rds-13b572c73cb0) would be helpful.
   - Write Lambda Function to push update data to S3 Bucket. Add a Trigger to automatically run Lambda Function, I schedule with rate 7 days.
   - Transfer data from S3 Bucket to Lambda. Add a Trigger but event-based (when the first Lambda Function run).
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
   - Validate and select the best model.
4. Machine Learning Model deployment: Deploy the final model on EC2.
  - Develop a Streamlit app locally.
  - Push the app on a EC2 instance. It's not easy as I thought, you should read about AWS EC2 and if it raises some issues, I advise you to read the common issues first.
  - Pull training data from our RDS PostgreSQL Database.
  - Use the validated model from previous step.
5. Trading Bot development: Develop a trading bot, design profitable strategy. (still in process)
6. Web App Development: Build a web app using Streamlit and Python to interact with the deployed model and display the predictions. And Deploy the final app on AWS EC2.
Now you can reach this app via this [link](http://3.27.120.16:8501/), believe me it's safe :v

## Problems and Further Development
I spent almost 3 weeks to finish whole this project by myself and there are some problems and what I learnt from them:
- Regardless of what articles and guidance you refer, please read thru it thoroughly first. If you miss somethings, it can cost you a ton of time to search and read about these issues.
- Learn enough about your cloud platform before start. I was firmly new with AWS which have ton of things I have to learn if want to use it effectively, however, just learn enough.
- Understand clearly what you want to do first, try whatever to make it detailed as much as possible. If not, feel free to design it again from scratch, it just take several days :))
- Don't be afraid of getting errors, this is the way we learn. The sooner you get errors, the sooner I can repair them.

Some techniques I learn from this project:
- Sure, AWS. There are bunch of interesting things in this site. And now I know a little about how to use:
  - AWS IAM: First of all, you have to create policies, roles, users for further use.
  - AWS Lambda: Serverless function, very useful if you just need to run few functions.
  - AWS RDS: Database.
  - AWS S3: Simple Store Service where you can store some files for further use.
  - AWS EC2: Server for running app.
  - And how they can connect together.
- Time Series Analysis. Truly, forecasting stock prices never be an easy tasks, especially the recent data is extremely fluctuate due the pandemic. However, I had chance to apply what I learnt from this [course](https://www.kaggle.com/learn/time-series).
- Machine Learning.
- Data Engineering.
- Deployment. 

In the future, there are somethings I could improve:
- Data Pipeline. The volume of data I used in this project is pretty small so my pipeline is simple.
- MLOps for developing and deploying Models more effectively.
- A trading bot. In the beginning, I tended to build a trading bot which gives user some advice to investing, however, I believe that in present my prediction is not believable enough to do this.

## Conclusion
My project has fulfilled its requirements to build a wed-based application to predict Australian Stocks Price and taught me somethings new rather than working only on my Jupyter notebooks.
 
To conclude, thank you for time. I understand that my project still has many problems, so it would be very nice to me if you could give me some advice and feedback to improve it. Many thanks!