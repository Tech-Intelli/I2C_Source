"""
Detect and saves video frames to the specified directory
"""
# pylint: disable=E0401
# pylint: disable=E1101
# pylint: disable=W0719
# pylint: disable=R0903

import os
from dataclasses import dataclass
import cv2


@dataclass
class VideoSceneDetector:
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

    video_path: str
    scene_detector: 'SceneDetector'
    scene_saver: 'SceneSaver'

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

        if duration > 120:
            cap.release()
            raise Exception("Please provide a short duration video")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Skip frames to reduce processing time.
            if duration <= 10 and frame_index % 3 != 0:
                frame_index += 1
                continue
            elif duration > 10 and frame_index % 10 != 0:
                frame_index += 1
                continue
            self.scene_detector.process_frame(frame)
            if self.scene_detector.scene_changed():
                scene = self.scene_detector.get_scene()
                self.scene_saver.save_scene(scene)

            frame_index += 1

        cap.release()


class SceneDetector:
    """
    A class for detecting scene changes in a video.

    Attributes:
        prev_frame: numpy.ndarray or None, the previous frame of the video.
        prev_gray: numpy.ndarray or None, the previous frame in grayscale.
        curr_frame: numpy.ndarray or None, the current frame of the video.
        curr_gray: numpy.ndarray or None, the current frame in grayscale.
        mean_diffs: list, a list of mean differences between current and
        previous frames.
        num_diffs: int, the maximum number of mean differences to be stored in
        the mean_diffs list.
        diff_index: int, the index of the oldest mean difference in the
        mean_diffs list.

    Methods:
        process_frame(frame): Processes a new frame and updates the mean
        difference list.
        scene_changed(): Returns a boolean value indicating if a scene change
        has occurred.
        get_scene(): Returns the current frame.
    """

    def __init__(self, num_diffs=30):
        self.prev_frame = None
        self.prev_gray = None
        self.curr_frame = None
        self.curr_gray = None
        self.mean_diffs = []
        self.num_diffs = num_diffs
        self.diff_index = 0

    def process_frame(self, frame):
        """
        Processes a single frame of a video and updates mean_diffs list.

        This method calculates the difference between the current frame and
        the previous frame, and calculates the mean difference.
        It then appends the mean difference to mean_diffs list.
        If the length of mean_diffs list is greater than num_diffs,
        then the oldest difference is removed from the list.

        Parameters:
        ----------
        frame : ndarray
            A single frame of a video.
        """
        if self.curr_gray is not None:
            self.prev_frame = self.curr_frame
            self.prev_gray = self.curr_gray

        self.curr_frame = frame.copy()
        self.curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.prev_gray is not None:
            diff = cv2.absdiff(self.curr_gray, self.prev_gray)
            mean_diff = diff.mean()
            self.mean_diffs.append(mean_diff)

            if len(self.mean_diffs) > self.num_diffs:
                oldest_diff_index = self.diff_index - self.num_diffs
                self.mean_diffs.pop(oldest_diff_index)
            else:
                self.diff_index += 1

    def scene_changed(self):
        """
        Checks if a scene change has occurred.

        Returns:
            bool: True if a scene change has occurred, False otherwise.
        """

        if len(self.mean_diffs) < self.num_diffs:
            return False

        threshold = sum(self.mean_diffs) / len(self.mean_diffs)
        return self.mean_diffs[-1] > threshold

    def get_scene(self):
        """
        Returns the current frame.

        Returns:
            numpy.ndarray: The current frame.
        """
        return self.curr_frame


class SceneSaver:
    """
    A class that saves extracted scenes as JPEG images.

    Args:
        scenes_dir (str, optional): Directory where the extracted
        scenes will be saved. Defaults to 'extracted_images'.

    Attributes:
        scenes_dir (str): Directory where the extracted scenes will be saved.
        scene_list (list): List containing all the extracted scene frames.

    Methods:
        save_scene(scene): Saves the given scene as a JPEG image in the scenes directory.
    """

    def __init__(self, scenes_dir='extracted_images'):
        self.scenes_dir = scenes_dir
        self.scene_list = []

    def save_scene(self, scene):
        """
        Saves the given scene as a JPEG image in the scenes directory.

        Args:
            scene (numpy.ndarray): The scene frame to be saved.

        Returns:
            None
        """

        self.scene_list.append(scene)
        scene_filename = f"scene_{len(self.scene_list):04d}.jpg"
        if not os.path.exists(self.scenes_dir):
            os.makedirs(self.scenes_dir)
        scene_path = os.path.join(self.scenes_dir, scene_filename)
        cv2.imwrite(scene_path, scene)
