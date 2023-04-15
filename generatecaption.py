import os
import shutil
import time
import openai
from cachemodel import CachedModel
from imagecompressor import ImageCompressor
from videoscenedetector import VideoSceneDetector, SceneDetector, SceneSaver


class Chatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.openai = openai

    def get_response(self, content):
        self.openai.api_key = self.api_key
        responseJson = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}]
        )
        return responseJson


class ImageCaptionGenerator:
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def generate_caption(self, image_path, caption_size):
        compressed_image_path = ImageCompressor.compress(image_path, 10)
        image_pipeline = CachedModel.get_image_caption_pipeline(
            compressed_image_path)
        text = image_pipeline[0]['generated_text']
        caption_size_description = ""
        if caption_size == 'small':
            caption_size_description = "caption within 2-3 sentences"
        elif caption_size == 'medium':
            caption_size_description = "caption within 5-7 sentences"
        elif caption_size == 'large':
            caption_size_description = "caption within 10-15 sentences"
        elif caption_size == 'very large':
            caption_size_description = "30-50 sentences"
        elif caption_size == 'blog post':
            caption_size_description = "blog post description"

        content = f'''Write a {caption_size_description} for instagram
        for this image and add most popular 30 hashtags.
        Don't forget to add some emojis: {text}'''
        responseJson = self.chatbot.get_response(content)
        return responseJson, compressed_image_path


class VideoCaptionGenerator:
    def __init__(self, chatbot, scene_detector, scene_saver):
        self.chatbot = chatbot
        self.scene_detector = scene_detector
        self.scene_saver = scene_saver

    def generate_caption(self, video_path):
        scene_dir = "extracted_images"
        vid_scn_detector = VideoSceneDetector(
            video_path,
            self.scene_detector,
            self.scene_saver)
        vid_scn_detector.detect_scenes()
        image_list = os.listdir(scene_dir)
        all_captions = ""
        for eachImage in image_list:
            image_pipeline = CachedModel.get_image_caption_pipeline(
                os.path.join(scene_dir, eachImage))
            text = image_pipeline[0]['generated_text']
            all_captions += " " + text
        content = f'''Connect these sentences and rewrite
        an artistic paragraph:{all_captions}'''
        responseJson = self.chatbot.get_response(content)
        shutil.rmtree(scene_dir, ignore_errors=True)
        return responseJson


if __name__ == '__main__':
    start_time = time.time()
    chatbot = Chatbot(os.environ["OPENAI_API_KEY"])
    image_caption_generator = ImageCaptionGenerator(chatbot)
    video_caption_generator = VideoCaptionGenerator(
        chatbot,
        SceneDetector(),
        SceneSaver()
    )
    print(video_caption_generator.generate_caption(
        "IMG_8160.MOV")["choices"][0]["message"]["content"])
    elapsed_time = time.time() - start_time
    print(f"It took {elapsed_time} seconds to generate video caption")
