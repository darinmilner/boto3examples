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

    # internet gateway
    ig_name = "main-igw"


#check if internet gateway exists
response = ec2.describe_internet_gateways(
    Filters=[
        {"Name": "tag:Name", "Values": [ig_name]}
    ]
)

internet_gateways = response.get("internetGateways", [])

if internet_gateways:
    # skip creation
    ig_id = internet_gateways[0]["InternetGatewayId"]
    print(f"Internet gateway with id {ig_id} already exists.")
else:
    ig_response = ec2.create_internet_gateway()

    ig_id = ig_response["InternetGateway"]["InternetGatewayId"]

    ec2.create_tags[ig_id], Tags=[{
        "Key": "Name",
        "Value" : ig_name
    }]
    # attach to VPC
    ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=ig_id)
    print(f"Internet Gateway {ig_name} with ID {ig_id} has been created")
