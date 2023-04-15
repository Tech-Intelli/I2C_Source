from dataclasses import dataclass
import cv2
import os


@dataclass
class VideoSceneDetector:
    video_path: str
    scene_detector: 'SceneDetector'
    scene_saver: 'SceneSaver'

    def detect_scenes(self):
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        frame_index = 0

        if duration > 120:
            cap.release()
            return

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
    def __init__(self, num_diffs=30):
        self.prev_frame = None
        self.prev_gray = None
        self.curr_frame = None
        self.curr_gray = None
        self.mean_diffs = []
        self.num_diffs = num_diffs
        self.diff_index = 0

    def process_frame(self, frame):
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
        if len(self.mean_diffs) < self.num_diffs:
            return False

        threshold = sum(self.mean_diffs) / len(self.mean_diffs)
        return self.mean_diffs[-1] > threshold

    def get_scene(self):
        return self.curr_frame


class SceneSaver:
    def __init__(self, scenes_dir='extracted_images'):
        self.scenes_dir = scenes_dir
        self.scene_list = []

    def save_scene(self, scene):
        self.scene_list.append(scene)
        scene_filename = f"scene_{len(self.scene_list):04d}.jpg"
        if not os.path.exists(self.scenes_dir):
            os.makedirs(self.scenes_dir)
        scene_path = os.path.join(self.scenes_dir, scene_filename)
        cv2.imwrite(scene_path, scene)
