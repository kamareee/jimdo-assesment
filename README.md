# Jimdo ETL 

## Introduction
This repo demonstrate an ETL, which will get data from a AWS SQS queue (from a AWS Data producer account) and after applying
some transformation, will insert data into a AWS Redshift cluster for BI reporting or further consumption by various stack-holder.
The detail description of the problem will be found in `resources/kinesis_to_redshift.md`

### Assumptions

- The data will be pulled by a `Lambda` function in Jimdo data producer and send to Jimdo Data Analytics AWS account. The DE might have
less access on the data producer account.
- A batch ETL has been proposed since end use of the data is not mentioned in the problem description. For real time use cases this architecture 
need to be modified
- `SQS` is chosen for this ETL since it can scale independently. Furthermore, configuring SQS queue is simpler and suitable for this batch processing.
- Proper security and trust between AWS accounts has been setup already
- Necessary IAM users and roles have been created to apply least privilege rule of access 

### Description of the ETL

Following diagram illustrate the proposed ETL. The overall ETL can be described as follows:

![](/jimdo-etl.jpg)

**Data from Data Producer account**

The data from the producer will be pulled from `SQS` queue via a `Lambda` function to a S3 bucket (called as `raw` here). A sample code for the function has been 
given in `lamda_to_raws3.py`. This function will create a unique file every 5 minutes within following folder structure:

`date=<etl date>/<etl_hour>/<unique_file_name>`

When a file lands on this S3 bucket, an event will be send to an SQS queue.

**Transform and Load ETL**

A Kubernetes CronJob (or an Airflow job) will be scheduled (every 5 minutes) to check the queue event generated in  the above step. 
This event will contain the file name information. A script similar to `raw_to_transformed.py` will be executed on each scheduled run which will
check the event information and get the latest file landed on the raw S3 bucket, do some transformation (if necessary) and
write to `transformed` S3 bucket in `parquet` format. Here, `parquet` is chosen since it is well recognized columnar format and 
provide efficient loading in a columnar DW like `Redshift`.

After writing to the transformed S3 bucket, same script can read the same file which has just been written and write it to  
the corresponding Redshift table using [`python-redshift`](https://github.com/aws/amazon-redshift-python-driver) connector. `COPY` command can 
also be used to achieve the same.

An alternate solution can be to schedule hourly ETL from `AWS Glue` or using k8s CronJob to load data into RedShift. In this
case, the loading user need to be setup with proper resource class and privilege so that it can write 1 Million record in two tables.

**Reprocessing/Backfilling of Data**
Data can be reprocessed from raw S3 using a separate ETL and by reading specific date/hour folder.