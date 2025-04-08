# s3_helpers.py
import boto3
import os
from aws_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, S3_BUCKET, S3_LOCATION

s3 = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def upload_graph_to_s3(file_path, username):
    try:
        if file_path is None:
            print("No graph file path provided")
            return None
            
        filename = f"{username}_network_graph.png"
        content_type = "image/png"
        
        with open(file_path, 'rb') as f:
            s3.upload_fileobj(
                f,
                S3_BUCKET,
                filename,
                ExtraArgs={
                    "ContentType": content_type
                }  # Removed ACL parameter
            )
        return f"{S3_LOCATION}{filename}"
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        return None


