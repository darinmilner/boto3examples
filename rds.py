import boto3
import time

rds = boto3.client("rds")

username = "dbuser1"
password = "verysecretpw"
db_subnet_group = "vpc-subnet-group"
db_cluster_id = "my-rds-cluster"

# create the DB cluster
try:
    response = rds.descibe_db_clusters(
        DBClusterIdentifier=db_cluster_id,
    )
    print(f"The DB cluster named {db_cluster_id} already exists.  Skipping creation.")
except rds.exceptions.DBClusterNotFoundFault:
    response = rds.create_db_cluster(
        Engine="aurora-mysql",
        EngineVersion="5.7.mysql_aurora.2.08.3",
        DbClusterIdentifier=db_cluster_id,
        MasterUsername=username,
        MasterUserPassword=password,
        DatabaseName="my-db",
        EngineMode="serverless",
        ScalingConfiguration={
            "MinCapacity": 1,
            "MaxCapacity": 8,
            "AutoPause": True,
            "SecondsUntilAutoPause": 300
        }
    )
    print(f"DB cluster {db_cluster_id} has been created")

    # wait for DB cluster to become available
    while True:
        response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
        status = response["DBClusters"][0]["Status"]
        print(f"The status of the cluster is {status}")
        if status == "available":
            break
        print("Waiting for the DB Cluster to become available")
        time.sleep(40)

# update scaling configuration
response = rds.modify_db_cluster(
        DbClusterIdentifier=db_cluster_id,
        ScalingConfiguration={
            "MinCapacity": 1,
            "MaxCapacity": 16,
            "AutoPause": True,
            "SecondsUntilAutoPause": 600
        }
    )
print(f"DB cluster {db_cluster_id} has been modified.")

#delete cluster
response = rds.delete_db_cluster(
        DbClusterIdentifier=db_cluster_id,
        SkipFinalSnapShot=True,
    )
print(f"DB cluster {db_cluster_id} has been deleted.")