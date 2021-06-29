### Background
We need to store important information transmitted from front-end to generate insights for various stakeholders. Tracking endpoint receives the data from front-end and stores it in a Kinesis stream (or SQS) as JSON.

### Your task
Your task is to build an ETL pipeline to process Kinesis (SQS) records into a Redshift cluster in a reliable and scalable way. Here are some things to keep in mind:
	
1. The Kinesis stream (or SQS) and Redshift cluster reside in different AWS accounts, and we don't want to make Redshift publicly accessible.
2. The architecture of the pipeline should allow re-importing records to Redshift. But please do not spend time implementing the methods for this, we are only interested in the architecture to make this possible. 
3. The volume of events in Kinesis stream (or SQS) is approximately 1 million per hour, but we should be able to scale the pipeline if volume increases.
4. The JSON body of an event in Kinesis stream (or SQS) is like [this](https://gist.githubusercontent.com/gunes-jimdo/e9a775b27b9647aae944f069b4a441b8/raw/3cd67f0b5a99158a3a9f1280314712f4376bcbf2/user_event.json) and [this](https://gist.githubusercontent.com/gunes-jimdo/e9a775b27b9647aae944f069b4a441b8/raw/256d65b1d22a4be7c40e2a412dda614acf21a88a/user_utm.json).
5. The target table schema is like [this](https://gist.githubusercontent.com/gunes-jimdo/e9a775b27b9647aae944f069b4a441b8/raw/3cd67f0b5a99158a3a9f1280314712f4376bcbf2/events_schema.sql) and [this](https://gist.githubusercontent.com/gunes-jimdo/e9a775b27b9647aae944f069b4a441b8/raw/256d65b1d22a4be7c40e2a412dda614acf21a88a/schema_utm.sql).

The solution should be based on AWS services, but the architecture is up to you.

### Requirements
Please provide your solution in a Github repository. Add documentation and tests as you prefer. Please use Terraform to manage infrastructure. In ideal case, we can run your code and infrastructure to process records from the Kinesis stream (or SQS).