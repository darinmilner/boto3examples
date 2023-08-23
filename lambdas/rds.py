import boto3
import io
import csv
import logging

s3_client = boto3.client("s3")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # get bucket and file name from event
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        fie_name = event["Records"][0]["s3"]["object"]["key"]

        # read file from s3
        response = s3_client.get_object(Bucket=bucket_name, Key=fie_name)
        data = response["Body"].read().decode("utf-8")

        csv_reader = csv.reader(io.StringIO(data))
        # skip header
        next(csv_reader)

        for record in csv_reader:
            print(record)

        logger.info("Lambda has finished successfully.")
    except Exception as e:
        logger.error(f"Unexpected error. {e}")
