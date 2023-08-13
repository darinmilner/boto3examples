import boto3

s3 = boto3.resource("s3")

bucket_name = "taskapi-storage-bucket-useast1"

# iterate through buckets in the AWS account
my_buckets = [bucket.name for bucket in s3.buckets.all()]

if bucket_name not in my_buckets:
    print(f"{bucket_name} does not exist yet.")
    # create s3 bucket
    s3.create_bucket(Bucket=bucket_name)
    print(f"{bucket_name} has been created.")
else:
    print(f"{bucket_name} already exists.")

file1 = "file1.txt"
file2 = "file2.txt"

# upload files to bucket
s3.Bucket(bucket_name).upload_file(Filename=file1, key=file1)

# Read file
obj = s3.Object(bucket_name, file1)
body = obj.get()["Body"].read()
print(body)

# update file1 with contents of file2
s3.Object(bucket_name, file1).put(Body=open(file2, "rb"))
print(body)

# delete file and bucket
s3.Object(bucket_name, file1).delete()

bucket = s3.Bucket(bucket_name)
bucket.delete()
