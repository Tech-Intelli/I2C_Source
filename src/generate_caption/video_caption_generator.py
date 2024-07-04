import os
import shutil
from generate_caption import CaptionGenerator
from inference import InferenceAbstract
from inference.llava_model import LlavaModel
from video_scene_detector import VideoSceneDetector


class VideoCaptionGenerator(CaptionGenerator):
    """
    A class that generates captions for videos using a chatbot.
    """

    def __init__(self, chatbot, scene_detector, scene_saver):
        super().__init__(chatbot)
        self.scene_detector = scene_detector
        self.scene_saver = scene_saver

    def generate_caption(
        self,
        location,
        video_path,
        caption_size,
        context,
        style,
        num_hashtags,
        tone,
        social_media,
        device="cpu",
        collection=None,
    ):
        """
        Generate a caption for a video using a chatbot.

        Parameters:
        video_path (str): The path to the video file.
        caption_size (str): The desired size of the caption. Valid values are 'small', 'medium', 'large', 'very large', and 'blog post'.
        context (str): The context in which the caption will be used. Optional.
        style (str): The style in which the caption should be written.
        num_hashtags (int): The number of hashtags to include in the caption.
        tone (string): Caption tone.
        Returns:
        dict: A JSON object containing the response from the chatbot.
        """

        scene_dir = "extracted_images"
        os.makedirs(scene_dir, exist_ok=True)
        vid_scn_detector = VideoSceneDetector(
            video_path, self.scene_detector, self.scene_saver
        )
        vid_scn_detector.detect_scenes()
        image_list = os.listdir(scene_dir)
        all_captions = ""

        cachedModel: InferenceAbstract = LlavaModel(collection)
        for each_image in image_list:
            text = cachedModel.get_image_caption_pipeline(
                os.path.join(scene_dir, each_image)
            )
            all_captions += " " + text

        content = self._generate_content(
            all_captions,
            caption_size,
            context,
            style,
            tone,
            num_hashtags,
            location,
            social_media,
        )
        stream_caption = self._generate_caption_with_hashtags(content, num_hashtags)
        shutil.rmtree(scene_dir, ignore_errors=True)
        return stream_caption
