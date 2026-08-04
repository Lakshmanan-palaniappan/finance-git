from pyspark.sql.types import *

branch_schema = StructType([
    StructField("branch_id", StringType(), False),
    StructField("branch_name", StringType(), False),
    StructField("city", StringType(), False),
    StructField("state", StringType(), False),
    StructField("region", StringType(), False),
    StructField("manager_name", StringType(), False)
])