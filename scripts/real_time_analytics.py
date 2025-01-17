
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, avg

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Real-Time Analytics") \
    .getOrCreate()

# Kinesis stream parameters
kinesis_stream_name = "your-kinesis-stream"
region = "your-region"

# Read data from Kinesis
raw_stream = spark.readStream \
    .format("kinesis") \
    .option("streamName", kinesis_stream_name) \
    .option("region", region) \
    .option("initialPosition", "latest") \
    .load()

# Parse the JSON data
stream_data = raw_stream.selectExpr("CAST(data AS STRING) as json_data")
parsed_data = stream_data.selectExpr(
    "json_tuple(json_data, 'sensor_id', 'temperature', 'humidity', 'timestamp') as (sensor_id, temperature, humidity, timestamp)"
).select(
    col("sensor_id"),
    col("temperature").cast("double"),
    col("humidity").cast("double"),
    col("timestamp").cast("timestamp")
)

# Calculate averages over 1-minute windows
aggregated_data = parsed_data.groupBy(
    window(col("timestamp"), "1 minute"),
    col("sensor_id")
).agg(
    avg("temperature").alias("avg_temperature"),
    avg("humidity").alias("avg_humidity")
)

# Write results to S3
query = aggregated_data.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "s3://your-bucket-name/processed/real_time_analytics/") \
    .option("checkpointLocation", "s3://your-bucket-name/checkpoints/real_time_analytics/") \
    .start()

query.awaitTermination()
