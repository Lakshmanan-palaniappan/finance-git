from pyspark.sql.types import *

login_activity_schema = StructType([
    StructField("login_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("login_timestamp", TimestampType(), False),
    StructField("device", StringType(), False),
    StructField("ip_address", StringType(), False),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("city", StringType(), False),
    StructField("country", StringType(), False),
    StructField("login_status", StringType(), False)
])