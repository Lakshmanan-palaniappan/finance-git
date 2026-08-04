from pyspark.sql.types import *

customer_kyc_schema = StructType([
    StructField("customer_id", StringType(), False),
    StructField("pan_verified", BooleanType(), False),
    StructField("aadhaar_verified", BooleanType(), False),
    StructField("address_verified", BooleanType(), False),
    StructField("kyc_status", StringType(), False),
    StructField("expiry_date", DateType(), False)
])