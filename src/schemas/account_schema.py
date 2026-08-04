from pyspark.sql.types import *

account_schema = StructType([
    StructField("account_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("account_number", StringType(), False),
    StructField("account_type", StringType(), False),
    StructField("currency", StringType(), False),
    StructField("balance", DecimalType(18, 2), False),
    StructField("interest_rate", DecimalType(5, 2), True),
    StructField("branch_id", StringType(), False),
    StructField("account_status", StringType(), False),
    StructField("opened_date", DateType(), False),
    StructField("closed_date", DateType(), True),
    StructField("created_timestamp", TimestampType(), False),
    StructField("updated_timestamp", TimestampType(), False)
])