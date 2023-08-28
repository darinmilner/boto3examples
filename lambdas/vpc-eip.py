import boto3

def lambda_handler(event, context):
    ec2_resource = boto3.resource("ec2")
    test_allocation_id = "eip-alloc-id"

    for elastic_ip in ec2_resource.vpc_addresses.all():
        print(elastic_ip)
        # check unassociated elastic ips
        if elastic_ip.instance_id is None and elastic_ip.ip_allocation_id == test_allocation_id:
            print(f"{elastic_ip} is not associated with an instance")
            elastic_ip.release()  # release the elastic ip



    return {
        "statusCode": 200,
        "body": "Lambda invoked successfully"
    }
