"""
Module for creating s3 buckets, upload and download images.
"""
# pylint: disable=E0401
import logging
import boto3
from botocore import exceptions


class AwsS3:
    """Create S3 bucket, Upload and Download image files.
    """
    s3 = boto3.client('s3')
    region = 'eu-central-1'

    @staticmethod
    def create_bucket(s3_bucket_name):
        """
        Creates an AWS S3 bucket
        """
        try:
            AwsS3.s3.create_bucket(Bucket=s3_bucket_name, CreateBucketConfiguration={
                'LocationConstraint': AwsS3.region})
        except exceptions.ClientError as error:
            logging.error(
                'Error creating AWS S3 Bucket: %s due to error:\n%s', s3_bucket_name, error)

    @staticmethod
    def upload_file_to_s3(image_path, s3_bucket_name, key_name):
        """
        Upload an image file to Amazon S3
        """
        try:
            AwsS3.s3.upload_file(image_path, s3_bucket_name, key_name)
        except exceptions.ClientError as error:
            logging.error('Error uploading file: %s to %s due to error:\n%s',
                          image_path, s3_bucket_name, error)
            return False
        return True

    @staticmethod
    def upload_file_object_to_s3(image_stream, s3_bucket_name, key_name):
        """
        Upload an image file to Amazon S3
        """
        try:
            AwsS3.s3.upload_fileobj(image_stream, s3_bucket_name, key_name)
        except exceptions.ClientError as error:
            logging.error('Error uploading file: %s to %s due to error:\n%s',
                          image_stream, s3_bucket_name, error)
            return False
        return True

    @staticmethod
    def download_image_from_s3(image_save_path, key_name, s3_bucket_name):
        """Download image from S3 bucket.

        Args:
            image_save_path (str): path/filename.jpg where the image will be saved
            key_name (str): file name in s3 bucket
            s3_bucket_name (str): Amazon S3 bucket name
        """
        try:
            AwsS3.s3.download_file(s3_bucket_name, key_name, image_save_path)
        except exceptions.ClientError as error:
            logging.error(
                'Error downloading %s from %s due to error:\n%s', key_name, s3_bucket_name, error)
            return False
        return True

    @staticmethod
    def delete_file_from_s3(s3_bucket_name, key_name):
        """
        Delete a file from Amazon S3

        Args:
            s3_bucket_name (str): Amazon S3 bucket name
            key_name (str): file name in s3 bucket
        """
        try:
            AwsS3.s3.delete_object(s3_bucket_name, key_name)
        except exceptions.ClientError as error:
            logging.error(
                'Error deleting %s from %s due to error:\n%s', key_name, s3_bucket_name, error)
            return False
        return True
