# This script will read data from raw s3 bucket, parse into user_event and user_utm dataframe
# And write into transformed s3 bucket (in parquet format) in a folder structure
# date=<date>/<hour>/user_event(or user_utm)/<filename.parquet> i.e. date=2021-07-04/11/user_event/<filename.parquet>
# An IAM user has been created with read permission from raw bucket and write permission to transformed bucket
# Improvement: create a temp directory in the runtime environment to hold the generated files
# Improvement: Code improvement to make more modular and generalized (applying object oriented design)
# Improvement: Adding parallel processing using threading
# Improvement: Adding a function to read data (latest) from transformed s3 bucket and write into Redshift
# using COPY command or JDBC connector


import ast
import json
from io import BytesIO

import boto3

import pandas as pd


# return a list of files
def check_queue():
    pass


# Read the latest written file and write to Redshift
# Using of COPY command
def write_to_dw(list_of_files: list):
    print("Writing to DW")


def run_etl():
    raw_bucket_name = 'jimdodevraw'
    transformed_bucket_name = 'jimdodevtransformed'
    object_prefix_user_events = 'date=2021-07-04/11/user_event/'
    object_prefix_user_utm = 'date=2021-07-04/11/user_utm/'

    written_files = []

    user_events_data = []
    user_utm_data = []

    read_prefix = 'date=2021-07-04/11/'

    # file_names = check_queue()
    file_names = ['2021-07-04_11_data.txt']  # from check_queue() function

    s3_client = boto3.client('s3')

    # Reading the files from the queue, splitting to user_event and user_utm files and writing to transformed s3
    # Need improvement to increase performance
    for file in file_names:

        object_name = read_prefix + file

        with open('temp.txt', 'wb') as fl:
            s3_client.download_fileobj(raw_bucket_name, object_name, fl)

        file = open('temp.txt', 'r')
        contents = file.readlines()
        file.close()

        for content in contents:
            dt = json.loads(content)
            if 'user_account_id' in dt.keys():
                user_events_data.append(dt)
            else:
                user_utm_data.append(dt)

        df_user_events = pd.DataFrame(user_events_data)
        df_user_utm = pd.DataFrame(user_utm_data)

        # Refactor Needed
        filename_user_event = "2021-07-04_11_user_event.parquet"  # Add uuid for unique object name
        filename_user_utm = "2021-07-04_11_user_utm.parquet"  # Add uuid for unique object name
        object_name_user_event = object_prefix_user_events + filename_user_event
        object_name_user_utm = object_prefix_user_utm + filename_user_utm
        try:
            # Writing user_event processed file.
            df_user_events.to_parquet(filename_user_event)

            with open(filename_user_event, "rb") as f:
                s3_client.upload_fileobj(f, transformed_bucket_name, object_name_user_event)
                written_files.append(object_name_user_event)

            # Writing user_utm processed file. (Refactor needed to avoid code duplication)
            df_user_utm.to_parquet(filename_user_utm)

            with open(filename_user_utm, "rb") as f:
                s3_client.upload_fileobj(f, transformed_bucket_name, object_name_user_utm)
                written_files.append(object_name_user_utm)

            print("File writing successful")
            print(written_files)
        except Exception as e:
            print(e)

        write_to_dw(written_files)


if __name__ == "__main__":
    run_etl()