"""
Detect and saves video frames to the specified directory
"""

import cv2


class VideoProcessor:
    """
    Class that detects and saves different scenes in a given video file.

    Attributes:
    -----------
    video_path : str
        Path to the video file.
    scene_detector : SceneDetector
        An instance of SceneDetector class that detects scene changes.
    scene_saver : SceneSaver
        An instance of SceneSaver class that saves detected scenes.
    """

    def __init__(self, video_path, scene_detector, scene_saver):
        """
        Initializes the VideoProcessor with the provided video_path, scene_detector, and scene_saver.

        Args:
            video_path (str): Path to the video file.
            scene_detector (SceneDetector): An instance of SceneDetector class that detects scene changes.
            scene_saver (SceneSaver): An instance of SceneSaver class that saves detected scenes.
        """
        self.video_path = video_path
        self.scene_detector = scene_detector
        self.scene_saver = scene_saver

    def detect_scenes(self):
        """
        Detects and saves different scenes in a video file.

        This method reads each frame of the video and checks if there is any
        scene change. If there is a scene change, then it saves the current
        frame as a new scene. It uses SceneDetector and SceneSaver classes
        to detect and save scenes respectively.
        """
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        frame_index = 0
        last_saved_frame_index = 0
        min_frames_between_saves = 30

        if duration <= 10:
            skip_rate = 3
        elif duration <= 15:
            skip_rate = 5
        elif duration <= 30:
            skip_rate = 10
        elif duration <= 45:
            skip_rate = 15
        elif duration <= 60:
            skip_rate = 20
        else:
            skip_rate = 30

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_index % skip_rate != 0:
                frame_index += 1
                continue

            self.scene_detector.process_frame(frame)
            if self.scene_detector.scene_changed():
                if frame_index - last_saved_frame_index >= min_frames_between_saves:
                    scene = self.scene_detector.get_scene()
                    self.scene_saver.save_scene(scene)
                    last_saved_frame_index = frame_index

            frame_index += 1

        cap.release()
        self.scene_detector.reset_state()
