import boto3

# list s3 buckets
s3 = boto3.resource("s3")

for bucket in s3.buckets.all():
    print(bucket.name)
