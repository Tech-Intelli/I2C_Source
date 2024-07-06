"""
Detect and saves video frames to the specified directory
"""

import os
from dataclasses import dataclass
import cv2


@dataclass
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

    video_path: str
    scene_detector: "SceneDetector"
    scene_saver: "SceneSaver"

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
        """
        Initializes a new instance of the SceneDetector class.

        Args:
            num_diffs (int, optional): The maximum number of mean differences to be stored in the mean_diffs list. Defaults to 30.

        Attributes:
            prev_frame (numpy.ndarray or None): The previous frame of the video.
            curr_frame (numpy.ndarray or None): The current frame of the video.
            mean_diffs (list): A list of mean differences between current and previous frames.
            num_diffs (int): The maximum number of mean differences to be stored in the mean_diffs list.
            diff_index (int): The index of the oldest mean difference in the mean_diffs list.
        """
        self.prev_frame = None
        self.curr_frame = None
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
        self.curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.curr_frame = frame.copy()
        if self.prev_frame is not None:
            if self.curr_frame.shape != self.prev_frame.shape:
                print(
                    f"Frame size mismatch: prev_frame {self.prev_frame.shape}, curr_frame {self.curr_frame.shape}"
                )
                self.curr_frame = cv2.resize(
                    self.curr_frame,
                    (self.prev_frame.shape[1], self.prev_frame.shape[0]),
                )

            diff = cv2.absdiff(self.curr_frame, self.prev_frame)
            mean_diff = diff.mean()
            self.mean_diffs.append(mean_diff)

            if len(self.mean_diffs) > self.num_diffs:
                self.mean_diffs.pop(0)

        self.prev_frame = self.curr_frame

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

    def reset_state(self):
        """
        Resets the state of the object.

        This method resets the `prev_frame` attribute to `None` and clears the `mean_diffs` list.

        Parameters:
            None

        Returns:
            None
        """
        self.prev_frame = None
        self.mean_diffs = []


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

    def __init__(self, scenes_dir="extracted_images"):
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
