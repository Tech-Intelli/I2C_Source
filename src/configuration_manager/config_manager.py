"""Configuration manager module."""

import os
import yaml
from dataclasses import asdict, fields, is_dataclass, dataclass, field
from typing import Type, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from prettytable import PrettyTable
from configuration_manager.config_models import (
    MultiModalConfig,
    OllamaConfig,
    ImageCompressionConfig,
    TransformConfig,
    ModelSelectionConfig,
)

from datetime import datetime
from utils.logger import log


@dataclass
class AppConfig:

    multimodal: MultiModalConfig = field(default_factory=MultiModalConfig)
    ollama: OllamaConfig = field(default_factory=OllamaConfig)
    image_compression: ImageCompressionConfig = field(
        default_factory=ImageCompressionConfig
    )
    transform_config: TransformConfig = field(default_factory=TransformConfig)
    model_selection: ModelSelectionConfig = field(default_factory=ModelSelectionConfig)

    def validate(self):
        """
        Validates the configuration fields of the AppConfig object.

        Raises:
            ValueError: If any of the configuration fields have invalid values.

        """
        # Validate MultiModalConfig
        if (
            not isinstance(self.multimodal.blip, str)
            or not self.multimodal.blip.strip()
        ):
            raise ValueError(
                "The 'blip' field in MultiModalConfig must be a non-empty string."
            )
        if not isinstance(self.multimodal.vit, str) or not self.multimodal.vit.strip():
            raise ValueError(
                "The 'vit' field in MultiModalConfig must be a non-empty string."
            )

        # Validate OllamaConfig
        if (
            not isinstance(self.ollama.variants.phi3, str)
            or not self.ollama.variants.phi3.strip()
        ):
            raise ValueError(
                "The 'phi' field in OllamaConfig must be a non-empty string."
            )
        if (
            not isinstance(self.ollama.variants.llama3, str)
            or not self.ollama.variants.llama3.strip()
        ):
            raise ValueError(
                "The 'llama3' field in OllamaConfig must be a non-empty string."
            )
        if (
            not isinstance(self.ollama.variants.gemma2, str)
            or not self.ollama.variants.gemma2.strip()
        ):
            raise ValueError(
                "The 'gemma2' field in OllamaConfig must be a non-empty string."
            )
        if not isinstance(self.ollama.use, str) or not self.ollama.use.strip():
            raise ValueError(
                "The 'use' field in OllamaConfig must be a non-empty string."
            )
        if not isinstance(self.ollama.temperature, int):
            raise ValueError(
                "The 'temperature' field in OllamaConfig must be an integer."
            )
        if not isinstance(self.ollama.top_p, float):
            raise ValueError("The 'top_p' field in OllamaConfig must be a float.")

        if not isinstance(self.ollama.stream, bool):
            raise ValueError("The 'stream' field in ollama must be a boolean.")

        # Validate ImageCompressionConfig
        if (
            not isinstance(self.image_compression.type, str)
            or not self.image_compression.type.strip()
        ):
            raise ValueError(
                "The 'type' field in ImageCompressionConfig must be a non-empty string."
            )
        if not isinstance(self.image_compression.compress, bool):
            raise ValueError(
                "The 'compress' field in ImageCompressionConfig must be a boolean."
            )
        if not isinstance(self.image_compression.compression_quality, int):
            raise ValueError(
                "The 'compression_quality' field in ImageCompressionConfig must be an integer."
            )
        if not isinstance(self.image_compression.resize_factor, float):
            raise ValueError(
                "The 'resize_factor' field in ImageCompressionConfig must be a float."
            )
        # Validate ModelSelectionConfig
        if (
            not isinstance(self.model_selection.model_name, str)
            or not self.model_selection.model_name.strip()
        ):
            raise ValueError(
                "The 'model_type' field in ModelSelectionConfig must be a non-empty string."
            )
        # Validate chroma_db config
        if (
            not isinstance(self.chroma_db.blip, str)
            or not self.chroma_db.blip.strip()
        ):
            raise ValueError(
                "The 'blip' field in ChromaDBConfig must be a non-empty string."
            )
        if (
            not isinstance(self.chroma_db.llava, str)
            or not self.chroma_db.llava.strip()
        ):
            raise ValueError(
                "The 'llava' field in ChromaDBConfig must be a non-empty string."
            )


class ConfigManager:
    def __init__(self, config_file="config.yaml"):
        """
        Initializes the ConfigManager class with the given config_file.

        Args:
            config_file (str, optional): The path to the configuration file. Defaults to "config.yaml".

        Returns:
            None

        Initializes the following instance variables:
            - config_file (str): The path to the configuration file.
            - app_config (AppConfig): An instance of the AppConfig class.
            - version (tuple): The version loaded from the configuration file.
            - config_history (list): An empty list to store the configuration history.
            - observer (Observer): An instance of the Observer class for file system events.

        Initializes the file system watcher to monitor changes in the configuration file.
        Loads the configuration from the configuration file.
        """
        self.config_file = config_file
        self.app_config = AppConfig()
        self.version = self.load_version()  # Initialize with the last saved version
        self.config_history = []

        self.observer = Observer()
        self.observer.schedule(
            ConfigFileChangeHandler(self),
            path=os.path.dirname(config_file) or ".",
            recursive=False,
        )
        self.observer.start()

        self.load_config()  # Load the initial configuration

    def load_version(self):
        """
        Loads the version from the configuration file.

        Returns:
            tuple: A tuple representing the version loaded from the configuration file. If the version is not found, returns (0, 1, 0) by default.
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                config_data = yaml.safe_load(file)
                return config_data.get(
                    "version", (0, 1, 0)
                )  # Default to (0, 1, 0) if version not found
        else:
            return (0, 1, 0)  # Default starting version if config file doesn't exist

    def load_config(self):
        """
        Loads the configuration from the configuration file.
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                config_data = yaml.safe_load(file)
            self._update_config_from_dict(self.app_config, config_data)
            self.app_config.validate()
            self.pretty_print_config()

            # Save loaded config with a patch increment
            self.save_version("Loaded initial configuration", increment="patch")

    def save_config(self):
        """
        Saves the current configuration to a versioned file by generating the versioned file name,
        dumping the configuration using yaml.safe_dump, and updating the main config file with a new version number.
        """
        # Generate versioned file name
        versioned_file = self.generate_versioned_filename()

        # Save configuration to the versioned file
        with open(versioned_file, "w") as file:
            yaml.safe_dump(
                self.to_unordered_dict(self.app_config), file, default_flow_style=False
            )

        # Update the main config file with the new version number
        self.save_version("Saved current configuration", increment="patch")

    def save_version(self, message, increment="patch"):
        """
        Updates the version of the object based on the specified increment type and logs the versioning action to history.

        Parameters:
            message (str): A message describing the versioning action.
            increment (str, optional): The type of increment to apply to the version. Defaults to "patch".
                Must be one of "major", "minor", or "patch".

        Raises:
            ValueError: If the increment type is not one of "major", "minor", or "patch".

        Returns:
            None
        """
        # Update version based on the increment type
        major, minor, patch = self.version
        if increment == "major":
            major += 1
            minor = 0
            patch = 0
        elif increment == "minor":
            minor += 1
            patch = 0
        elif increment == "patch":
            patch += 1
        else:
            raise ValueError(
                "Invalid increment type. Use 'major', 'minor', or 'patch'."
            )

        self.version = (major, minor, patch)

        # Log the versioning action to history
        self.log_version_history(message)

    def generate_versioned_filename(self):
        """
        Generates a versioned file name based on the current version.

        Returns:
            str: The versioned file name with the format "{basename}_{version_str}{ext}".

        """
        # Generate a versioned file name based on the current version
        basename, ext = os.path.splitext(self.config_file)
        version_str = ".".join(map(str, self.version))
        versioned_file = f"{basename}_{version_str}{ext}"
        return versioned_file

    def log_version_history(self, message):
        """
        Log version history with timestamp and message
        """
        # Log version history with timestamp and message
        self.config_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "version": self.version,
            }
        )

    def get_config_version(self, version_number):
        """
        Retrieves the configuration version based on the provided version number.

        Args:
            version_number: The version number of the configuration.

        Returns:
            The configuration version associated with the provided version number.

        Prints an error message if the version number does not exist.
        """
        try:
            return self.config_versions[version_number]
        except IndexError:
            log.error(f"Version {version_number} does not exist.")

    def get_config_history(self):
        """
        Get the configuration history.

        Returns:
            list: The configuration history stored in the ConfigManager instance.
        """
        return self.config_history

    def rollback_to_version(self, version_number):
        """
        Rolls back the configuration to the specified version number.

        Args:
            version_number: The version number to which the configuration should be rolled back.

        Returns:
            None
        """
        try:
            version_to_restore = self.config_versions[version_number]
            self.app_config = version_to_restore
            self.save_config()  # Save the restored version to the config file
            log.info(f"Rolled back to version {version_number}.")
        except IndexError:
            log.error(f"Version {version_number} does not exist.")

    @staticmethod
    def get_config_manager():
        """
        Returns an instance of the ConfigManager class.

        This static method returns a singleton instance of the ConfigManager class.
        It ensures that only one instance of the class is created and returned. This is useful when you need to access the same instance of the ConfigManager class throughout your application.

        :return: An instance of the ConfigManager class.
        :rtype: ConfigManager
        """
        return ConfigManager()

    def get_app_config(self) -> AppConfig:
        """
        Returns the application configuration object.

        :return: An instance of the AppConfig class.
        :rtype: AppConfig
        """
        return self.app_config

    def set_app_config(self, **kwargs):
        """
        Updates the application configuration with the provided keyword arguments and saves the changes.

        Parameters:
            **kwargs (dict): Keyword arguments representing the configuration values to update.

        Returns:
            None
        """
        self._update_config_from_dict(self.app_config, kwargs)
        self.save_config()

    def pretty_print_config(self):
        """
        Pretty prints the application configuration.

        This function converts the application configuration object to a dictionary,
        creates a PrettyTable object, and populates it with the configuration data.
        Finally, it prints the table.

        Parameters:
            self (ConfigManager): The ConfigManager instance.

        Returns:
            None
        """
        config_dict = asdict(self.app_config)
        table = PrettyTable(field_names=["Parameter", "Value"], align="l")
        self._populate_table(config_dict, table)
        log.info(table.get_string())

    @staticmethod
    def _populate_table(config_dict, table, parent_key=""):
        """
        Populates a PrettyTable object with the given configuration dictionary.

        Args:
            config_dict (dict): The configuration dictionary to populate the table with.
            table (PrettyTable): The PrettyTable object to populate.
            parent_key (str, optional): The parent key of the current key. Defaults to ''.

        Returns:
            None
        """
        for key, value in config_dict.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                ConfigManager._populate_table(value, table, full_key)
            else:
                table.add_row([full_key, value])

    @staticmethod
    def _update_config_from_dict(config, config_dict):
        """
        Updates the configuration object `config` based on the values in the dictionary `config_dict`.

        Parameters:
            config: The configuration object to update.
            config_dict: The dictionary containing the values to update the configuration with.

        Returns:
            None
        """
        if config_dict is None:
            return

        for field in fields(config):
            value = config_dict.get(field.name)
            if value is not None:
                if is_dataclass(field.type):
                    nested_config = getattr(config, field.name)
                    ConfigManager._update_config_from_dict(nested_config, value)
                else:
                    setattr(
                        config, field.name, ConfigManager._cast_value(field.type, value)
                    )

    @staticmethod
    def _cast_value(type_: Type, value: Any) -> Any:
        """
        Casts the given value to the specified type.

        Args:
            type_ (Type): The type to cast the value to.
            value (Any): The value to be cast.

        Returns:
            Any: The casted value.

        """
        if type_ is int:
            return int(value)
        elif type_ is float:
            return float(value)
        elif type_ is bool:
            return bool(value)
        elif type_ is str:
            return str(value)
        else:
            return value

    def get_node(self, node_path):
        """
        Retrieves a nested node from the `app_config` object based on the given `node_path`.

        Args:
            node_path (str): The dot-separated path to the desired node.

        Returns:
            Any: The value of the nested node, or `None` if the node does not exist.
        """
        parts = node_path.split(".")
        current = self.app_config
        for part in parts:
            current = getattr(current, part, None)
            if current is None:
                break
        return current

    def to_unordered_dict(self, obj):
        """
        Converts a dataclass object to a standard dictionary without preserving field order.

        Args:
            obj: The dataclass object to convert.

        Returns:
            A standard dictionary representing the dataclass object.
        """
        if is_dataclass(obj):
            result = dict()
            for field in fields(obj):
                value = getattr(obj, field.name)
                result[field.name] = self.to_unordered_dict(value)
            return result
        elif isinstance(obj, list):
            return [self.to_unordered_dict(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self.to_unordered_dict(v) for k, v in obj.items()}
        else:
            return obj


class ConfigFileChangeHandler(FileSystemEventHandler):
    def __init__(self, config_manager):
        """
        Initializes the ConfigFileChangeHandler class with the given config_manager.

        Args:
            config_manager: The configuration manager object.

        Returns:
            None
        """
        self.config_manager = config_manager

    def on_modified(self, event):
        """
        Handles the event when a file is modified.

        Args:
            event (FileSystemEvent): The event object representing the file modification.

        Returns:
            None

        This function checks if the modified file is the configuration file. If it is, it prints a message indicating that the configuration file has changed and reloads the configuration.
        """
        if event.src_path == self.config_manager.config_file:
            log.warn(
                f"Configuration file {self.config_manager.config_file} changed, reloading."
            )
            self.config_manager.load_config()
