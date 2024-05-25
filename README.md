# big-data

This project is revenue management and vacation rental market research of travel and tourism industry (Airbnb). Airbnb is an online market place that enable users to list, find and rent vacation homes across the globe. but here we are taking data of Rio de janeiro city.

The business problem was to analyze the several reasons that affect the revenue and figuring out the optimal price range for guests and also having the information of when to upscale the properties and offering the best packages, amenities to the guests to increase the revenue. To achieve this I have designed two interactive dashboards, one for traveler so that he could find the best rental home as per needs. And second dashboard for property owners to know the trends in the market on that basis owner can take decisions to increase the revenue.

I have designed a pipeline in that we are ingesting the data from kaggle and putting it into landing zone of the data lake. I have used aws s3 as data lake here. as soon as the data come into landing zone we have trigger the Glue workflow using the lambda function. In that job trigger will trigger the glue job which will do all the processing on the data using the serverless Spark and we have stored the cleaned data in the curated zone of the data lake. After that the glue crawler will get triggered which will infer the schema. here we are using Athena as connector between the Power BI and data lake. on the power Bi we have created the report.

I created this whole pipeline using infrastructure as code for that we are using Aws CFT. I have automated this pipeline using Git Action.  
