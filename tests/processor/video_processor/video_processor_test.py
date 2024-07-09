import pytest
from unittest.mock import patch, MagicMock
import cv2
from processor.video_processor import VideoProcessor
from processor.video_processor.scene_detctor import SceneDetector
from processor.video_processor.scene_saver import SceneSaver

@pytest.fixture
def mock_video_capture():
    """
    Fixture that creates a mock VideoCapture object for testing purposes.

    Returns:
        MagicMock: A mock object that simulates the behavior of VideoCapture.
    """
    mock_cap = MagicMock()
    # Simulate reading 150 frames followed by an end-of-file signal
    mock_cap.read.side_effect = [(True, f'frame{i}'.encode()) for i in range(1, 151)] + [(False, None)]
    mock_cap.get.side_effect = lambda x: 30 if x == cv2.CAP_PROP_FPS else 150
    return mock_cap

@pytest.fixture
def mock_scene_detector():
    """
    Creates a mock SceneDetector object for testing purposes.

    Returns:
        MagicMock: A mock object that simulates the behavior of SceneDetector.
    """
    mock_detector = MagicMock(spec=SceneDetector)
    # Ensure enough values to avoid StopIteration
    mock_detector.scene_changed.side_effect = [False, True] * 300
    return mock_detector

@pytest.fixture
def mock_scene_saver():
    """
    Creates a mock SceneSaver object for testing purposes.
    """
    return MagicMock(spec=SceneSaver)

@patch("cv2.VideoCapture")
def test_detect_scenes(mock_cv2_VideoCapture, mock_video_capture, mock_scene_detector, mock_scene_saver):
    """
    Test function for detecting scenes in a video.
    
    Args:
        mock_cv2_VideoCapture: A mock object simulating the behavior of cv2.VideoCapture.
        mock_video_capture: A mock object for video capture.
        mock_scene_detector: A mock object for detecting scene changes.
        mock_scene_saver: A mock object for saving scenes.
    
    Returns:
        None
    """
    mock_cv2_VideoCapture.return_value = mock_video_capture
    video_path = "test_video.mp4"

    processor = VideoProcessor(video_path, mock_scene_detector, mock_scene_saver)
    processor.detect_scenes()

    print(f"Read call count: {mock_video_capture.read.call_count}")
    print(f"Process frame call count: {mock_scene_detector.process_frame.call_count}")
    print(f"Scene changed call count: {mock_scene_detector.scene_changed.call_count}")
    print(f"Save scene call count: {mock_scene_saver.save_scene.call_count}")

    assert mock_video_capture.read.call_count == 151  # 150 frames + 1 stop frame

    # Calculate the expected number of processed frames based on skip rate logic
    expected_processed_frames = sum(1 for i in range(150) if i % 3 == 0)
    assert mock_scene_detector.process_frame.call_count == expected_processed_frames
    assert mock_scene_detector.scene_changed.call_count == expected_processed_frames
    assert mock_scene_saver.save_scene.call_count >= 1  # Saved scene at least once when scene changed

    mock_scene_detector.reset_state.assert_called_once()

@patch("cv2.VideoCapture")
def test_detect_scenes_with_different_durations(mock_cv2_VideoCapture, mock_video_capture, mock_scene_detector, mock_scene_saver):
    """
    Test function for detecting scenes with different durations in a video.
    
    Args:
        mock_cv2_VideoCapture: A mock object simulating the behavior of cv2.VideoCapture.
        mock_video_capture: A mock object for video capture.
        mock_scene_detector: A mock object for detecting scene changes.
        mock_scene_saver: A mock object for saving scenes
    
    Returns:
        None
    """
    video_durations = [5, 12, 25, 40, 50, 70]
    expected_skip_rates = [3, 5, 10, 15, 20, 30]

    for duration, expected_skip_rate in zip(video_durations, expected_skip_rates):
        frame_count = duration * 30  # Assuming 30 fps

        # Mock the get method to return correct fps and frame count
        mock_video_capture.get.side_effect = lambda x: 30 if x == cv2.CAP_PROP_FPS else frame_count
        mock_video_capture.read.side_effect = [(True, f'frame{i}'.encode()) for i in range(1, frame_count + 1)] + [(False, None)]

        mock_cv2_VideoCapture.return_value = mock_video_capture
        video_path = "test_video.mp4"

        processor = VideoProcessor(video_path, mock_scene_detector, mock_scene_saver)
        processor.detect_scenes()

        # Calculate the number of frames that should be processed based on the skip rate
        expected_processed_frames = (frame_count + expected_skip_rate - 1) // expected_skip_rate
        print(f"Duration: {duration}s, Skip rate: {expected_skip_rate}, Expected frames processed: {expected_processed_frames}")
        print(f"Process frame call count: {mock_scene_detector.process_frame.call_count}")

        assert mock_scene_detector.process_frame.call_count == expected_processed_frames

        mock_scene_detector.reset_state.reset_mock()
        mock_scene_detector.process_frame.reset_mock()
        mock_scene_saver.save_scene.reset_mock()

@patch("cv2.VideoCapture")
def test_no_scene_change(mock_cv2_VideoCapture, mock_video_capture, mock_scene_detector, mock_scene_saver):
    """
    Test function for detecting no scene change in a video.
    
    Args:
        mock_cv2_VideoCapture: A mock object simulating the behavior of cv2.VideoCapture.
        mock_video_capture: A mock object for video capture.
        mock_scene_detector: A mock object for detecting scene changes.
        mock_scene_saver: A mock object for saving scenes.
    
    Returns:
        None
    """
    mock_scene_detector.scene_changed.side_effect = [False] * 300

    mock_video_capture.get.side_effect = lambda x: 30 if x == cv2.CAP_PROP_FPS else 150
    mock_video_capture.read.side_effect = [(True, f'frame{i}'.encode()) for i in range(1, 151)] + [(False, None)]

    mock_cv2_VideoCapture.return_value = mock_video_capture
    video_path = "test_video.mp4"

    processor = VideoProcessor(video_path, mock_scene_detector, mock_scene_saver)
    processor.detect_scenes()

    print(f"Save scene call count (no scene change): {mock_scene_saver.save_scene.call_count}")

    assert mock_scene_saver.save_scene.call_count == 0  # No scenes saved since no scene changes
