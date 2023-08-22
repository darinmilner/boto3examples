import csv
import datetime
import boto3

def lambda_handler(event, context):
    s3 = boto3.resource("s3")

    billing_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    csv_file = event["Records"][0]["s3"]["object"]["key"]

    error_bucket = "billing-bucket-errors"  # bucket name

    # download csv from s3 and read the content
    obj = s3.Object(billing_bucket, csv_file)
    data = obj.get()["body"].read().decode("utf-8").splitlines()
    # error found flag
    error_found = False
    # define productlines
    valid_products = ["Bakery","Dairy","Vegetables"]
    valid_currencies = ["USD","Baht","Riyal","Ringgit"]

    # read csv line by line
    for row in csv.reader(data[1:], delimiter=","):
        print(row)
        # extract data from csv
        date = row[6]
        product_line = row[4]
        currency = row[7]
        bill_amount = float(row[8])
        # check if the date is valid
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            error_found = True
            print(f"Error in record {row[0]}. incorrect date format: {date}")
            break
        if product_line not in valid_products:
            error_found = True
            print(f"Error in record {row[0]}. unrecognized product found: {product_line}")
            break
        if currency not in valid_currencies:
            error_found = True
            print(f"Error in record {row[0]}. unrecognized currency found: {currency}")
        # copy file to error bucket is an error was found
        if error_found:
            copy_source = {
                "Bucket" : billing_bucket,
                "key" : csv_file
            }
            try:
                s3.meta.client.copy(copy_source, error_bucket, csv_file)
                print(f"File moved to bucket {error_bucket}")
                # delete from original bucket
                s3.Object(billing_bucket, csv_file).delete()
            except Exception as e:
                print(f"Error deleting file {str(e)}")
    else:
        return {
            "statusCode" : 200,
            "body": "No errors found in the csv files"
        }