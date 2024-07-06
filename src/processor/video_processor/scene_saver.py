import os
import cv2


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
