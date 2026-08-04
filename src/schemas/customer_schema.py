from pyspark.sql.types import *

customer_schema = StructType([
    StructField("customer_id", StringType(), False),
    StructField("first_name", StringType(), False),
    StructField("last_name", StringType(), False),
    StructField("date_of_birth", DateType(), False),
    StructField("gender", StringType(), True),
    StructField("email", StringType(), True),
    StructField("phone", StringType(), False),
    StructField("pan", StringType(), False),
    StructField("aadhaar", StringType(), False),
    StructField("occupation", StringType(), True),
    StructField("annual_income", DecimalType(15, 2), True),
    StructField("branch_id", StringType(), False),
    StructField("customer_status", StringType(), False),
    StructField("created_timestamp", TimestampType(), False),
    StructField("updated_timestamp", TimestampType(), False)
])