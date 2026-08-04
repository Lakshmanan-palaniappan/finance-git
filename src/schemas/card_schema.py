from pyspark.sql.types import *

card_schema = StructType([
    StructField("card_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("account_id", StringType(), False),
    StructField("card_number", StringType(), False),
    StructField("card_type", StringType(), False),
    StructField("card_network", StringType(), False),
    StructField("credit_limit", DecimalType(18,2), True),
    StructField("available_limit", DecimalType(18,2), True),
    StructField("issue_date", DateType(), False),
    StructField("expiry_date", DateType(), False),
    StructField("card_status", StringType(), False)
])