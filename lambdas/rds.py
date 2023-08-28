import boto3
import io
import csv
import logging

s3_client = boto3.client("s3")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# db details, currency conversion
db_name = "billing-db"
secret_store_arn = "secret-manager-arn-here"
db_cluster_arn = "db-cluster-arn-here"
rds_client = boto3.client("rds-data")
currency_conversion = {
    "USD": 1,
    "CAD": 0.79,
    "MXN": 0.05
}

def process_record(record):
    id, company_name, country, city, product_line, item, bill_date, currency, bill_amount = record
    bill_amount = float(bill_amount)
    rate = currency_conversion.get(currency)
    usd_amount = 0
    if rate:
        usd_amount = bill_amount * rate
    else:
        logger.info(f"No rate found for {currency}")

    print(f"ID {id}, currency {currency}")

    # sql for inserting records
    sql_statement = (
        "INSERT IGNORE INTO billing_data "
        "id, company_name, country, city, product_line ",
        "item, bill_date, currency, bill_amount, bill_amount_usd"
        "VALUES (:id, :company_name, :country, :city, :product_line, "
        ":item, :bill_date, :currency, :bill_amount, :usd_amount)"
    )

    sql_parameters = [
        {"name": "id", "value": {"stringValue" : id}},
        {"name": "company_name", "value": {"stringValue": company_name}},
        {"name": "country", "value": {"stringValue", country}},
        {"name": "city": "value":{"stringValue": city}},
        {"name": "product_line", "value": {"stringValue": product_line}},
        {"name": "item", "value": {"stringValue": item}},
        {"name": "bill_date", "value": {"stringValue": bill_date}},
        {"name": "currency", "value": {"stringValue": currency}},
        {"name": "bill_amount", "value": {"doubleValue": bill_amount}},
        {"name": "usd_amount", "value": {"doubleValue": usd_amount}}
    ]

    response = execute_statement(sql_statement, sql_parameters)
    logger.info(f"SQL execution response: {response}")


def execute_statement(sql, parameters):
    try:
        response = rds_client.execute_statement(
            secretArn=secret_store_arn,
            database=db_name,
            resource=db_cluster_arn,
            sql=sql,
            parameters=parameters,
        )
    except Exception as e:
        logger.error(f"Error, could not connect to Aurora serverless {e}")

    return response


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
            # process records
            process_record()

        logger.info("Lambda has finished successfully.")
    except Exception as e:
        logger.error(f"Unexpected error. {e}")
