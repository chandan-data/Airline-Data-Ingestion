# ✈️ Airline Data Ingestion Project

This project demonstrates an end-to-end data ingestion pipeline using AWS services.

## 🚀 Technologies Used
- AWS Glue (Crawler + ETL Job)
- AWS Step Functions
- Amazon SNS (for notifications)
- Python (for job scripts)
- S3 (for data storage)

## 🛠 Workflow Overview
1. Crawler starts and scans S3 for new airline data
2. Once crawler completes, Glue job processes the data
3. Step Function monitors status and sends success/failure notifications
