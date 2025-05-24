import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
import re

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node airport_dim
airport_dim_node1746083067468 = glueContext.create_dynamic_frame.from_catalog(database="airline-datamart", table_name="dev_airlines_airports_dim", redshift_tmp_dir="s3://redshift-glue-temp-data/temp-data/airline-dim/", transformation_ctx="airport_dim_node1746083067468")

# Script generated for node daily_flights_data
daily_flights_data_node1746080805387 = glueContext.create_dynamic_frame.from_catalog(database="airline-datamart", table_name="daily_flights", transformation_ctx="daily_flights_data_node1746080805387")

# Script generated for node Filter_delay_then_sixty_min
Filter_delay_then_sixty_min_node1746081041719 = Filter.apply(frame=daily_flights_data_node1746080805387, f=lambda row: (row["depdelay"] >= 60), transformation_ctx="Filter_delay_then_sixty_min_node1746081041719")

# Script generated for node Join_dept_airport
Filter_delay_then_sixty_min_node1746081041719DF = Filter_delay_then_sixty_min_node1746081041719.toDF()
airport_dim_node1746083067468DF = airport_dim_node1746083067468.toDF()
Join_dept_airport_node1746083599839 = DynamicFrame.fromDF(Filter_delay_then_sixty_min_node1746081041719DF.join(airport_dim_node1746083067468DF, (Filter_delay_then_sixty_min_node1746081041719DF['originairportid'] == airport_dim_node1746083067468DF['airport_id']), "left"), glueContext, "Join_dept_airport_node1746083599839")

# Script generated for node modify_dept_airport_columns
modify_dept_airport_columns_node1746084737285 = ApplyMapping.apply(frame=Join_dept_airport_node1746083599839, mappings=[("carrier", "string", "carrier", "string"), ("destairportid", "long", "destairportid", "long"), ("depdelay", "long", "dep_delay", "bigint"), ("arrdelay", "long", "arr_delay", "bigint"), ("airport_id", "bigint", "airport_id", "long"), ("city", "string", "dep_city", "string"), ("name", "string", "dep_airport", "string"), ("state", "string", "dep_state", "string")], transformation_ctx="modify_dept_airport_columns_node1746084737285")

# Script generated for node Join_arr_airport
modify_dept_airport_columns_node1746084737285DF = modify_dept_airport_columns_node1746084737285.toDF()
airport_dim_node1746083067468DF = airport_dim_node1746083067468.toDF()
Join_arr_airport_node1746085281508 = DynamicFrame.fromDF(modify_dept_airport_columns_node1746084737285DF.join(airport_dim_node1746083067468DF, (modify_dept_airport_columns_node1746084737285DF['destairportid'] == airport_dim_node1746083067468DF['airport_id']), "left"), glueContext, "Join_arr_airport_node1746085281508")

# Script generated for node modify_arr_airport_columns
modify_arr_airport_columns_node1746085434818 = ApplyMapping.apply(frame=Join_arr_airport_node1746085281508, mappings=[("carrier", "string", "carrier", "string"), ("dep_delay", "bigint", "dep_delay", "bigint"), ("arr_delay", "bigint", "arr_delay", "bigint"), ("dep_city", "string", "dep_city", "string"), ("dep_state", "string", "dep_state", "string"), ("dep_airport", "string", "dep_airport", "string"), ("airport_id", "bigint", "airport_id", "long"), ("city", "string", "arr_city", "string"), ("name", "string", "arr_airport", "string"), ("state", "string", "arr_state", "string")], transformation_ctx="modify_arr_airport_columns_node1746085434818")

# Script generated for node Amazon Redshift
AmazonRedshift_node1746086037525 = glueContext.write_dynamic_frame.from_options(frame=modify_arr_airport_columns_node1746085434818, connection_type="redshift", connection_options={"redshiftTmpDir": "s3://redshift-glue-temp-data/temp-data/airline-fact/", "useConnectionProperties": "true", "dbtable": "airlines.daily_flights_fact", "connectionName": "Redshift connection", "preactions": "CREATE TABLE IF NOT EXISTS airlines.daily_flights_fact (carrier VARCHAR, dep_delay VARCHAR, arr_delay VARCHAR, dep_city VARCHAR, dep_state VARCHAR, dep_airport VARCHAR, airport_id BIGINT, arr_city VARCHAR, arr_airport VARCHAR, arr_state VARCHAR);"}, transformation_ctx="AmazonRedshift_node1746086037525")

job.commit()