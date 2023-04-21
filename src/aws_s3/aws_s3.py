"""
Module for creating s3 buckets, upload and download images.
"""
import os
import boto3

# 
class AwsS3:
    """Create S3 bucket, Upload and Download image files.
    """
    s3 = boto3.client('s3')
    region = 'eu-central-1'

    @staticmethod
    def create_bucket(s3_bucket_name):
        """
        Creates an AWS S§ bucket
        """
        AwsS3.s3.create_bucket(Bucket=s3_bucket_name, CreateBucketConfiguration={
            'LocationConstraint': AwsS3.region})

    @staticmethod
    def upload_image_to_s3(image_path, s3_bucket_name):
        """
        Upload an image file to Amazon S3
        """
        key_name = os.path.basename(image_path)
        AwsS3.s3.upload_file(image_path, s3_bucket_name, key_name)

    @staticmethod
    def download_image_from_s3(image_save_path, key_name, s3_bucket_name):
        """_summary_

        Args:
            image_save_path (str): path/filename.jpg where the image will be saved
            key_name (str): file name in s3 bucket
            s3_bucket_name (str): Amazon S3 bucket name
        """
        AwsS3.s3.download_file(s3_bucket_name, key_name, image_save_path)
