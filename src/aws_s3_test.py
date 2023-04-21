"""
This is a primitive implementation and testing.
Either it will later be refactored to something more accurate or deleted
"""
import os
# pylint: disable=E0401
from aws_s3 import AwsS3
import generate_caption


def generate_image_caption_test():
    """
    Upload an image to S3, download it an generate caption
    """
    # pylint: disable=C0301
    image_path = '''/Users/dipanjandas/Development/ProjectAndIdeas/talkativeAI/ExplAIstic/src/tests/test_resources/images/small_image.jpg'''
    s3_bucket_name = "explaisticbucket"
    key_name = "nature_upload.jpg"
    # upload the image to s3
    AwsS3.upload_image_to_s3(
        image_path, s3_bucket_name, key_name)
    # download the image here from s3 bucket
    image_path = '''/Users/dipanjandas/Development/ProjectAndIdeas/talkativeAI/ExplAIstic/src/tests/test_resources/images/nature_download.jpg'''
    AwsS3.download_image_from_s3(image_path, key_name, s3_bucket_name)
    chatbot = generate_caption.Chatbot(os.environ["OPENAI_API_KEY"])
    image_caption_generator = generate_caption.ImageCaptionGenerator(chatbot)
    caption, _ = image_caption_generator.generate_caption(
        image_path, "small", "", "cool", 30)
    print(caption["choices"][0]["message"]["content"])


generate_image_caption_test()
