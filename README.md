
# Real-Time Analytics with Apache Spark and Amazon Kinesis

This repository demonstrates a real-time analytics pipeline for processing IoT sensor data using **Apache Spark Structured Streaming** on **Amazon EMR Serverless**. The pipeline ingests data from **Amazon Kinesis**, processes it in real time, and stores aggregated metrics in **Amazon S3**.

---

## 🛠️ **Use Case Overview**

### Objective
- Process IoT sensor data in real time.
- Calculate average temperature and humidity by sensor every minute.
- Store aggregated results in Amazon S3 for visualization.

### Workflow
1. **Data Source**:
   - Streaming IoT sensor data into an Amazon Kinesis stream.
   - Example schema: `sensor_id, temperature, humidity, timestamp`.

2. **Processing**:
   - Use Apache Spark Structured Streaming on EMR Serverless to:
     - Read from Kinesis.
     - Compute real-time metrics.
     - Write results to S3 in Parquet format.

3. **Visualization**:
   - Visualize aggregated metrics using AWS QuickSight or Tableau.

---

## 🗂️ **Folder Structure**

```
.
├── scripts/
│   ├── real_time_analytics.py     # PySpark streaming script
├── README.md                      # Project documentation
```

---

## 📋 **Sample Data**

### Input (Streaming Data)
```json
{"sensor_id": "sensor_1", "temperature": 22.5, "humidity": 45.2, "timestamp": "2025-01-15T10:15:30Z"}
{"sensor_id": "sensor_2", "temperature": 23.0, "humidity": 50.0, "timestamp": "2025-01-15T10:15:31Z"}
```

### Output (Aggregated Metrics)
| window_start      | window_end        | sensor_id | avg_temperature | avg_humidity |
|-------------------|-------------------|-----------|-----------------|--------------|
| 2025-01-15 10:15 | 2025-01-15 10:16  | sensor_1  | 22.15           | 44.6         |
| 2025-01-15 10:15 | 2025-01-15 10:16  | sensor_2  | 23.0            | 50.0         |

---

## ⚙️ **How to Run**

1. Upload the script to S3:
   ```bash
   aws s3 cp real_time_analytics.py s3://your-bucket-name/scripts/
   ```

2. Run the EMR Serverless job:
   ```bash
   aws emr-serverless start-job-run \
       --application-id <application-id> \
       --execution-role-arn <execution-role-arn> \
       --job-driver '{
           "sparkSubmit": {
               "entryPoint": "s3://your-bucket-name/scripts/real_time_analytics.py",
               "sparkSubmitParameters": "--conf spark.executor.memory=2g --conf spark.executor.cores=2"
           }
       }' \
       --configuration-overrides '{
           "monitoringConfiguration": {
               "s3MonitoringConfiguration": {
                   "logUri": "s3://your-bucket-name/logs/"
               }
           }
       }'
   ```

3. Visualize results using QuickSight or Tableau.

---

## 📊 **Expected Outcome**
- **Real-Time Metrics**: Aggregated data by sensor every minute.
- **Processed Data**: Available in Amazon S3 for visualization and reporting.

---

## 📧 **Contact**
For questions or suggestions:
- **Email**: kanthravulapati@gmail.com 
- **GitHub**: [https://github.com/krishnaravulapati](https://github.com/krishnaravulapati)

---
