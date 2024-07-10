import pytest
import cv2
import numpy as np
from processor.video_processor.scene_detector import SceneDetector


@pytest.fixture
def scene_detector():
    return SceneDetector(num_diffs=60)


def create_color_frame(width=640, height=480, color=(0, 0, 255)):
    """Creates a frame filled with a single color."""
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    frame[:] = color
    return frame


@pytest.mark.parametrize(
    "color1, color2", [((255, 0, 0), (0, 0, 255)), ((0, 255, 0), (0, 0, 255))]
)
def test_process_frame_with_color_changes(scene_detector, color1, color2):
    frame1 = create_color_frame(color=color1)
    frame2 = create_color_frame(color=color2)

    scene_detector.process_frame(frame1)
    scene_detector.process_frame(frame2)

    assert len(scene_detector.mean_diffs) == 1
    assert (
        scene_detector.mean_diffs[0] > 0
    ), f"Expected a positive mean diff, got {scene_detector.mean_diffs[0]}"


def test_reset_and_different_sizes(scene_detector):
    frame1 = create_color_frame(width=640, height=480, color=(0, 255, 0))
    frame2 = create_color_frame(width=320, height=240, color=(255, 0, 0))

    frame2_resized = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))

    scene_detector.process_frame(frame1)
    scene_detector.process_frame(frame2_resized)

    assert len(scene_detector.mean_diffs) == 1
    assert (
        scene_detector.mean_diffs[0] > 0
    ), f"Mean diff was not positive: {scene_detector.mean_diffs[0]}"
