import boto3
import time

# ec2 client
ec2 = boto3.client("ec2")

vpc_name = "main-vpc"

#check if vpc exists
response = ec2.describe_vpcs(
    Filters=[
        {"Name": "tag:Name", "Values": [vpc_name]}
    ]
)

vpcs = response.get("Vpc",[])

if vpcs:
    # skip creation
    vpc_id = vpcs[0]["VpcId"]
    print(f"VPC with id {vpc_id} already exists.")
else:
    vpc_response = ec2.create_vpc(CidrBlock="10.0.0.0/16")

    vpc_id = vpc_response["Vpc"]["VpcId"]

    # add delay to allow vpc to be created
    time.sleep(5)

    ec2.create_tags[vpc_id], Tags=[{
        "Key": "Name",
        "Value" : vpc_name
    }]
    print(f"VPC {vpc_name} with ID {vpc_id} has been created")