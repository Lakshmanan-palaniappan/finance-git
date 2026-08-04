from pyspark.sql.types import *

exchange_rate_schema = StructType([
    StructField("currency_code", StringType(), False),
    StructField("exchange_rate", DecimalType(18,6), False),
    StructField("effective_date", DateType(), False)
])