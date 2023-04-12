
from dataclasses import dataclass
import cv2
import os


@dataclass
class VideoSceneDetector:
    video_path = None
    scenes_dir = None

    @staticmethod
    def generate_video_scene_images(video_path, scenes_dir):
        cap = cv2.VideoCapture(video_path)

        prev_frame = None
        prev_gray = None
        curr_frame = None
        curr_gray = None

        scene_list = []
        frame_index = 0
        mean_diffs = []
        num_diffs = 30  # Number of differences to use in the moving average.
        diff_index = 0  # Index of the oldest difference in the moving average.

        """Loop through the video frames."""
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Skip frames to reduce processing time.
            if frame_index % 10 != 0:
                frame_index += 1
                continue

            # Convert the frame to grayscale.
            curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            """If this is the first frame, initialize
            the previous frame and current frame."""
            if prev_frame is None:
                prev_frame = frame
                prev_gray = curr_gray
                curr_frame = frame.copy()
                frame_index += 1
                continue

            """Compute the mean absolute difference
            between the current and previous frames."""
            diff = cv2.absdiff(curr_gray, prev_gray)
            mean_diff = diff.mean()

            """Add the current mean absolute
            difference to the moving average."""
            if len(mean_diffs) < num_diffs:
                mean_diffs.append(mean_diff)
            else:
                mean_diffs[diff_index] = mean_diff
                diff_index = (diff_index + 1) % num_diffs

            """Set the threshold as the average of the last
            num_diffs mean absolute differences."""
            threshold = sum(mean_diffs) / len(mean_diffs)

            """If the mean absolute difference is above
            the threshold, a scene change is detected."""
            if mean_diff > threshold:
                scene_list.append(frame_index)
                scene_filename = f"scene_{len(scene_list):04d}.jpg"
                if not os.path.exists(scenes_dir):
                    os.makedirs(scenes_dir)
                scene_path = os.path.join(scenes_dir, scene_filename)
                cv2.imwrite(scene_path, curr_frame)

            prev_frame = frame
            prev_gray = curr_gray
            curr_frame = frame.copy()
            frame_index += 1

        cap.release()
