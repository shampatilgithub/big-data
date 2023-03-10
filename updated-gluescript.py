
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
df = spark.read.format('csv').options(sep=",", escape='"', mode="PERMISSIVE", header=True, multiLine=True).load('s3://airbnb-in-data/')


df.show(2)
df1 = df.drop("_c0",
"listing_url",
"scrape_id",
"name",
"summary",
"space",
"experiences_offered",
"neighborhood_overview",
"notes",
"transit",
"access",
"interaction",
"house_rules",
"thumbnail_url",
"medium_url",
"picture_url",
"xl_picture_url",
"host_id",
"host_url",
"host_location",
"host_about",
"host_response_rate",
"host_acceptance_rate",
"host_is_superhost",
"host_thumbnail_url",
"host_picture_url",
"host_neighbourhood",
"host_total_listings_count",
"host_verifications",
"host_has_profile_pic",
"street",
"neighbourhood",
"neighbourhood_group_cleansed",
"city",
"state",
"zipcode",
"market",
"smart_location",
"country_code",
"country",
"is_location_exact",
"bed_type",
"square_feet",
"weekly_price",
"monthly_price",
"cleaning_fee",
"guests_included",
"minimum_nights",
"maximum_nights",
"calendar_updated",
"has_availability",
"availability_30",
"availability_60",
"availability_90",
"calendar_last_scraped",
"number_of_reviews",
"first_review",
"last_review",
"review_scores_accuracy",
"review_scores_cleanliness",
"review_scores_checkin",
"review_scores_communication",
"review_scores_location",
"review_scores_value",
"requires_license",
"license",
"jurisdiction_names",
"is_business_travel_ready",
"require_guest_profile_picture",
"require_guest_phone_verification",
"calculated_host_listings_count",
"reviews_per_month",
"month",
"minimum_minimum_nights",
"maximum_minimum_nights",
"minimum_maximum_nights",
"maximum_maximum_nights",
"minimum_nights_avg_ntm",
"maximum_nights_avg_ntm",
"number_of_reviews_ltm",
"calculated_host_listings_count_entire_homes",
"calculated_host_listings_count_private_rooms",
"calculated_host_listings_count_shared_rooms")
#change datatype of columns
from pyspark.sql.functions import *
from pyspark.sql.types import DoubleType

df1 = df1.withColumn("bedrooms", col("bedrooms").cast("integer"))
df1 = df1.withColumn("id", col("id").cast("integer"))
df1 = df1.withColumn("last_scraped", to_date("last_scraped", "yyyy-MM-dd"))
df1 = df1.withColumn("host_listings_count", col("host_listings_count").cast("integer"))
df1 = df1.withColumn("host_since", to_date("host_since", "yyyy-MM-dd"))
df1 = df1.withColumn("accommodates", col("accommodates").cast("integer"))
df1 = df1.withColumn("bathrooms", col("bathrooms").cast("integer"))
df1 = df1.withColumn("beds", col("beds").cast("integer"))
df1 = df1.withColumn("bedrooms", col("bedrooms").cast("integer"))
df1 = df1.withColumn("review_scores_rating", col("review_scores_rating").cast("integer"))
df1 = df1.withColumn("latitude", col("latitude").cast(DoubleType()))
df1 = df1.withColumn("longitude", col("longitude").cast(DoubleType()))
df1 = df1.withColumn("availability_365", col("availability_365").cast("integer"))




#convert to month and year last_Scraped

from pyspark.sql.functions import date_format
from pyspark.sql.functions import month, year



df1 = df1.withColumn("month", date_format("last_scraped", "MMMM"))
df1 = df1.withColumn("year", year("last_scraped"))
df1 = df1.withColumn("month_num", month("last_scraped"))
#host since

df1 = df1.withColumn("host_month", date_format("host_since", "MMMM"))
df1 = df1.withColumn("host_year", year("host_since"))



#To see the null values present in table 
df1.select([count(when(col(c).isNull(),c)).alias(c) for c in df1.columns]).show()

#remove null values from data
df1 = df1.filter(col("description").isNotNull())
df1 = df1.filter(col("host_name").isNotNull())
df1 = df1.filter(col("host_since").isNotNull())
df1 = df1.filter(col("bathrooms").isNotNull())
df1 = df1.filter(col("beds").isNotNull())
df1 = df1.filter(col("bedrooms").isNotNull())

#replace null values with mode(within an hour) in host_response_time column
df1= df1.fillna({"host_response_time":"within an hour"})
df1= df1.fillna({"review_scores_rating":94})
df1= df1.fillna({"security_deposit":0})

#replacements of values
df1 = df1.withColumn('price', regexp_replace(col('price'), '\$', ''))
df1 = df1.withColumn("security_deposit", regexp_replace(col("security_deposit"), "\$", ""))
df1 = df1.withColumn("extra_people", regexp_replace(col("extra_people"), "\$", ""))
df1 = df1.withColumn("amenities", regexp_replace(col("amenities"), '"', ""))
df1 = df1.withColumn("description", regexp_replace(col("description"), ',', ""))
df1 = df1.withColumn("host_identity_verified", regexp_replace(col("host_identity_verified"), 't', "True"))
df1 = df1.withColumn("host_identity_verified", regexp_replace(col("host_identity_verified"), 'f', "False"))
df1 = df1.withColumn("instant_bookable", regexp_replace(col("instant_bookable"), 't', "True"))
df1 = df1.withColumn("instant_bookable", regexp_replace(col("instant_bookable"), 'f', "False"))

df1 = df1.withColumn('accommodates', regexp_replace(col('accommodates'), '160', '2'))
df1 = df1.withColumn('bathrooms', regexp_replace(col('bathrooms'), '200', '2'))
df1 = df1.withColumn('bathrooms', regexp_replace(col('bathrooms'), '250', '2'))
df1 = df1.withColumn("bedrooms", when(
    col("bedrooms").isin("250", "251", "254", "255", "256"),
    "2").otherwise(col("bedrooms")))

df1 = df1.withColumn("amenities", regexp_replace(col("amenities"), r'\{', r'['))
df1 = df1.withColumn("amenities", regexp_replace(col("amenities"), r'\}', r']'))
df1 = df1.withColumn("amenities", regexp_replace(col("amenities"), ',', '  '))

#label availibiity_365 column
df1 = df1.withColumn("availability", 
                              when(df1["availability_365"] < 100, "Low")
                              .when((df1["availability_365"] >= 100) & (df1["availability_365"] < 250), "Medium")
                              .otherwise("High"))

#drop availability_365 column
df2=df1.drop("availability_365")

for column in df2.columns:
    df2 = df2.withColumn(column, regexp_replace(col(column), ',', ''))


df2.show(2)

df2 = df2.withColumn("bedrooms", col("bedrooms").cast("integer"))
df2 = df2.withColumn("id", col("id").cast("integer"))
df2 = df2.withColumn("last_scraped", to_date("last_scraped", "yyyy-MM-dd"))
df2 = df2.withColumn("host_listings_count", col("host_listings_count").cast("integer"))
df2 = df2.withColumn("host_since", to_date("host_since", "yyyy-MM-dd"))
df2 = df2.withColumn("accommodates", col("accommodates").cast("integer"))
df2 = df2.withColumn("bathrooms", col("bathrooms").cast("integer"))
df2 = df2.withColumn("beds", col("beds").cast("integer"))
df2 = df2.withColumn("bedrooms", col("bedrooms").cast("integer"))
df2 = df2.withColumn("review_scores_rating", col("review_scores_rating").cast("integer"))
df2 = df2.withColumn("latitude", col("latitude").cast(DoubleType()))
df2 = df2.withColumn("longitude", col("longitude").cast(DoubleType()))


dynamic_frame = DynamicFrame.fromDF(df2, glueContext, "csv_file")
dynamic_frame.printSchema()
output_dir = "s3://airbnb-out-data/"
glueContext.write_dynamic_frame.from_options(frame = dynamic_frame, connection_type = "s3", connection_options = {"path": output_dir}, format = "parquet")

job.commit()


