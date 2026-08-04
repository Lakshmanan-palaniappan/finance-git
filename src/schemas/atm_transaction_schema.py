from pyspark.sql.types import *

atm_transaction_schema = StructType([
    StructField("atm_transaction_id", StringType(), False),
    StructField("account_id", StringType(), False),
    StructField("atm_id", StringType(), False),
    StructField("amount", DecimalType(18,2), False),
    StructField("transaction_timestamp", TimestampType(), False),
    StructField("city", StringType(), False),
    StructField("status", StringType(), False)
])