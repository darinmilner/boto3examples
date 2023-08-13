import boto3

ec2 = boto3.resource("ec2")
instance_name = "boto3-test-ec2"

# store instance id
instance_id = None

# check if instance exists
instances = ec2.instances.all()
instance_exists = False

for instance in instances:
    for tag in instance.tag:
        if tag["key"] == "Name" and tag["Value"] == instance_name:
            instance_exists = True
            instance_id = instance.id
            print(f"Instance {instance_name} already exists")
            break
    if instance_exists:
        print("Instance already exists")
        break

if not instance_exists:
    new_instance = ec2.create_instance(
        ImageId="LINUX-AMI", # add valid AMI id
        MinCount=1,
        MaxCounr=1,
        KeyName="Your-Key-Pair", # add your key pair
        TagSpecifications=[
            {
                "ResourceType" : "instance",
                "Tags" :[
                     {
                        "Key": "Name",
                        "Value" : instance_name
                    },
                ],
            },
        ]
    )
    instance_id = new_instance[0].id
    print(f"Instance named {instance_name} with id {instance_id} created")


# Stop an instance
ec2.Instance(instance_id).stop()
print(f"Instance {instance_name} has been stopped.")

# Start an instance
ec2.Instance(instance_id).start()
print(f"Instance {instance_name} has been started.")

# Terminate an instance
# Stop an instance
ec2.Instance(instance_id).terminate()
print(f"Instance {instance_name} has been terminated.")