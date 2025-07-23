import boto3
import os


dynamodb = boto3.resource("dynamodb",
                            region_name=os.getenv("AWS_REGION", "ap-southeast-1"),
                            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "dummy"),
                            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "dummy"),
                            endpoint_url=os.getenv("DYNAMODB_URL", "http://localhost:8000"))

