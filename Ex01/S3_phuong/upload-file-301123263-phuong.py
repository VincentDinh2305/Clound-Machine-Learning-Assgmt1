# DINH HOANG VIET PHUONG - 301123263

import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from datetime import datetime

def create_bucket(bucket_name, region="us-east-1"):
    try:
        s3_client = boto3.client('s3', region_name=region)
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print(f"Bucket {bucket_name} created successfully.")
        return True
    except ClientError as e:
        print(f"AWS Error: {e.response['Error']['Message']}")
        return False


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"{file_name} uploaded successfully to {bucket}.")
    except ClientError as e:
        print(f"Failed to upload {file_name}. AWS Error: {e.response['Error']['Message']}")
    except NoCredentialsError:
        print("Credentials not available.")


def generate_bucket_name(base_name):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{base_name}-{timestamp}"


def main():
    base_bucket_name = 'files-301123263-phuongdinh'
    region = 'us-east-1'

    # Generate a unique bucket name to avoid conflicts
    bucket_name = generate_bucket_name(base_bucket_name)

    # Create the S3 bucket
    if not create_bucket(bucket_name, region):
        print(f"Failed to create bucket {bucket_name}. Exiting...")
        return

    # List of files to upload
    files_to_upload = ['phuong1.txt', 'phuong2.txt', 'phuong3.txt']
    for file_name in files_to_upload:
        upload_file(file_name, bucket_name)


if __name__ == '__main__':
    main()
