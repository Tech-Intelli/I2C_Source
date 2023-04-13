import os
import time
import openai
from cachemodel import CachedModel
from imagecompressor import ImageCompressor
from videoscenedetector import VideoSceneDetector
from videoscenedetector.videoscenedetector import SceneDetector, SceneSaver


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

    def generate_caption(self, image_path):
        compressed_image_path = ImageCompressor.compress(image_path, 10)
        image_pipeline = CachedModel.get_image_caption_pipeline(
            compressed_image_path)
        text = image_pipeline[0]['generated_text']
        content = f'''Write an instagram caption for this image
        and add exactly 30 hashtags. Don't forget to add some emojis: {text}'''
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
        #os.remove(scene_dir)
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
