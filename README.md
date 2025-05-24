# ✈️ Airline ETL Data Pipeline using AWS 

This project showcases a serverless, event-driven data pipeline built on AWS. It extracts raw airline data from S3, transforms it using AWS Glue, and loads it into Amazon Redshift for analytics. The entire workflow is orchestrated using **Amazon EventBridge** and **AWS Step Functions**.

---

## 🧱 Architecture Overview

- **S3** holds raw input data.
- **EventBridge** triggers the pipeline on new uploads.
- **Step Functions** coordinate the workflow.
- **AWS Glue** crawls, transforms, and loads data.
- **Amazon Redshift** stores final structured data for analytics.
- **SNS** sends notifications.
- **VPC** provides secure networking for Glue and Redshift.
- **IAM roles** manage permissions securely.

---

## 🗂 Data Storage

### S3 Bucket: `airlinedata-land-zn`

- `dim/` – Contains static airport dimension data.
- `daily_flights/` – Contains raw daily flight data (partitioned like a Hive table).

---

## 🧾 Redshift Schema

- **Cluster** created with proper VPC and IAM access.
- **Schema**: `airlines`
- **Tables**:
  - `airports_dim` (Dimension table)
  - `daily_flights_fact` (Fact table for transformed flight delay data)

### 🛠 SQL for Table Creation

```sql
CREATE SCHEMA airlines;

CREATE TABLE airlines.airports_dim (
    airport_id BIGINT,
    city VARCHAR(100),
    state VARCHAR(100),
    name VARCHAR(200)
);

COPY airlines.airports_dim
FROM 's3://airlinedata-land-zn/dim/airports.csv'
IAM_ROLE 'arn:aws:iam::XXXXXXXXXXXX:role/service-role/AmazonRedshift-CommandsAccessRole-YYYYMMDDTHHMMSS'
DELIMITER ','
IGNOREHEADER 1
REGION 'ap-south-1';

CREATE TABLE airlines.daily_flights_fact (
    carrier VARCHAR(10),
    dep_airport VARCHAR(200),
    arr_airport VARCHAR(200),
    dep_city VARCHAR(100),
    arr_city VARCHAR(100),
    dep_state VARCHAR(100),
    arr_state VARCHAR(100),
    dep_delay BIGINT,
    arr_delay BIGINT
);
```

## ⚙️ ETL Workflow

- Raw daily flight data is uploaded to S3 (`daily_flights/` folder).
- Amazon EventBridge detects the S3 upload and triggers a rule.
- AWS Step Function is invoked.
- Glue Crawler detects and catalogs the new data.
- Glue Job:
  - Joins flight data with `airports_dim`
  - Filters flights with delay > 60 minutes
  - Loads the transformed result into `daily_flights_fact` table in Redshift
- SNS sends success/failure notifications.

---

## 🛡️ Services Used

- Amazon S3  
- Amazon Redshift  
- Amazon EventBridge  
- AWS Glue (Crawler + Job)  
- AWS Step Functions  
- Amazon SNS  
- VPC for secure networking  
- IAM Roles for permission management  

---

## 📊 Final Outcome

- ✅ Scalable and automated ETL pipeline  
- ✅ Real-time S3-triggered data ingestion  
- ✅ Cleanly structured data in Redshift for analysis  
- ✅ Fully serverless with minimal manual intervention
