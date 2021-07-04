import logging
import boto3
from datetime import datetime
import json


# Sample SQS message

sqs_message = {
    "Records": [
        {
            "request_id": "fc417c2b-fe7a-4737-afe2-bec49c0ebd6f",
            "request_timestamp": "2020-06-01 00:00:24.000000",
            "cookie_id": "a09c4ca3-d142-4312-ba78-029c3355b8ef",
            "topic": "dolphin_cms.wizard.step.color_palette.set",
            "message": "{\"isAffiliate\":false,\"language\":\"es\",\"isRecommendedPalette\":true,\"color\":\"#6d8d79\","
                       "\"paletteIndex\":\"0\",\"workspaceId\":\"ecaca5cd-e23c-4f6d-8ec9-ad8695b378d5\"}",
            "environment": "dolphin_cms",
            "website_id": None,
            "user_account_id": "0f36f200-df29-4fbf-8625-39a88b7f778c",
            "location": "https://cms.jimdo.com/wizard/color-palette/",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
            "referrer": "https://register.jimdo.com/es/product"
        },
        {
            "request_id": "cbae8544-ab7a-46a5-9253-a5c8f6612115",
            "source": "adwords",
            "medium": "cpc",
            "campaign": "Campaign Brand FR",
            "content": None,
            "term": "jimdo",
            "matchtype": "e",
            "network": "g",
            "ad_id": "12063526619",
            "ad_pos": "1t1",
            "placement": None,
            "placement_category": None,
            "testgroup": None,
            "device": "c"
        }
    ]
}

bucket = 'jimdodevraw'


def main():
    # Sample Lambda function to send to raw S3 bucket (refer to architecture diagram)
    date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    hour = str(datetime.now().hour)

    name = date + '_' + hour + '_data'
    file_type = '.txt'

    output_filename = name + file_type

    object_prefix = 'date=' + date + '/' + hour + '/' + output_filename

    records = sqs_message['Records']

    output_file = open(output_filename, 'w', encoding='utf-8')

    logging.info("Writing queue message to text file....")

    for record in records:
        json.dump(record, output_file)
        output_file.write("\n")

    output_file.close()

    # Writing to raw S3 bucket
    # The text file will be dumped to this raw bucket with prefix date=<etl date>/etl_hour
    # i.e. s3://jimdodevraw/date=2021-07-03/15/
    s3_client = boto3.client('s3')

    with open(output_filename, "rb") as f:
        s3_client.upload_fileobj(f, bucket, object_prefix)


if __name__ == "__main__":
    main()

