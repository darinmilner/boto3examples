import json
import boto3
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    ec2 = boto3.client("ec2")
    current_date = datetime.now().strftime("%Y-%m-%d")

    try:
        response = ec2.create_snapshot(
            VolumeId="vol-ec2volumeid",
            Description="MyEC2Snapshot",
            TagSpecifications = [
                {
                    "ResourceType": "snapshot",
                    "Tags" : [
                        {
                            "Key": "Name",
                            "Value": f"EC2-SnapShot-{current_date}"
                        }
                    ]
                }
            ]
        )

        logger.info(f"Successfully created snapshot: {json.dumps(response, default=str)}")

    except Exception as e:
        logger.error(f"Error creating snapshot {str(e)}")