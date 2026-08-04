from pyspark.sql.types import *

transaction_schema = StructType([
    StructField("transaction_id", StringType(), False),
    StructField("account_id", StringType(), False),
    StructField("transaction_timestamp", TimestampType(), False),
    StructField("transaction_type", StringType(), False),
    StructField("amount", DecimalType(18, 2), False),
    StructField("currency", StringType(), False),
    StructField("merchant_id", StringType(), True),
    StructField("channel", StringType(), False),
    StructField("branch_id", StringType(), False),
    StructField("transaction_status", StringType(), False)
])