import cv2


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
                self.curr_frame = cv2.resize(
                    self.curr_frame,
                    (self.prev_frame.shape[1], self.prev_frame.shape[0]),
                )

            diff = cv2.absdiff(
                self.curr_gray, cv2.cvtColor(self.prev_frame, cv2.COLOR_BGR2GRAY)
            )
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
