import os
import yaml
from dataclasses import asdict, fields, is_dataclass, dataclass, field
from typing import Type, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from prettytable import PrettyTable


@dataclass
class MultiModalConfig:
    blip: str = "Salesforce/blip2-opt-2.7b"
    vit: str = "nlpconnect/vit-gpt2-image-captioning"


@dataclass
class OllamaConfig:
    Phi: str = "phi3"
    llama3: str = "llama3"
    temperature: int = 1
    top_p: float = 0.9


@dataclass
class ImageCompressionConfig:
    type: str = "webp"
    compress: bool = True
    compression_quality: int = 50
    resize_factor: float = 0.5


@dataclass
class TransformConfig:
    resize: tuple = (256, 256)
    center_crop: int = 224


@dataclass
class AppConfig:

    multimodal: MultiModalConfig = field(default_factory=MultiModalConfig)
    ollama: OllamaConfig = field(default_factory=OllamaConfig)
    image_compression: ImageCompressionConfig = field(
        default_factory=ImageCompressionConfig
    )
    transform_config: TransformConfig = field(default_factory=TransformConfig)

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
        if not isinstance(self.ollama.Phi, str) or not self.ollama.Phi.strip():
            raise ValueError(
                "The 'Phi' field in OllamaConfig must be a non-empty string."
            )
        if not isinstance(self.ollama.llama3, str) or not self.ollama.llama3.strip():
            raise ValueError(
                "The 'llama3' field in OllamaConfig must be a non-empty string."
            )
        if not isinstance(self.ollama.temperature, int):
            raise ValueError(
                "The 'temperature' field in OllamaConfig must be an integer."
            )
        if not isinstance(self.ollama.top_p, float):
            raise ValueError("The 'top_p' field in OllamaConfig must be a float.")

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


class ConfigManager:
    def __init__(self, config_file="config.yaml"):
        """
        A description of the entire function, its parameters, and its return types.
        """
        self.config_file = config_file
        self.app_config = AppConfig()
        self.load_config()

        self.observer = Observer()
        self.observer.schedule(
            ConfigFileChangeHandler(self),
            path=os.path.dirname(config_file) or ".",
            recursive=False,
        )
        self.observer.start()

    def load_config(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                config_data = yaml.safe_load(file)
            self._update_config_from_dict(self.app_config, config_data)
            self.app_config.validate()
            self.pretty_print_config()

    def save_config(self):
        """
        Saves the current configuration to the specified file.

        This function opens the specified configuration file in write mode and writes the current configuration object
        to it using the YAML serialization format. The `asdict` function is used to convert the configuration object
        into a dictionary, which is then dumped into the file using the `yaml.safe_dump` function. The `default_flow_style`
        parameter is set to `False` to ensure that the output is in the block style.

        Parameters:
            self (ConfigManager): The ConfigManager instance.

        Returns:
            None
        """
        with open(self.config_file, "w") as file:
            yaml.safe_dump(asdict(self.app_config), file, default_flow_style=False)

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
        print(table.get_string(sortby="Parameter"))

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
        return value

    def get_node(self, node_path: str) -> Any:
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


class ConfigFileChangeHandler(FileSystemEventHandler):
    def __init__(self, config_manager):
        """
        Initializes a new instance of the ConfigFileChangeHandler class.

        Args:
            config_manager (ConfigManager): An instance of the ConfigManager class.

        Returns:
            None
        """
        self.config_manager = config_manager

    def on_modified(self, event):
        """
        Handles the event when the configuration file is modified.

        Args:
            event (FileSystemEvent): The event object containing information about the file system event.

        Returns:
            None
        """
        if event.src_path == self.config_manager.config_file:
            print(
                f"Configuration file {self.config_manager.config_file} changed, reloading."
            )
            self.config_manager.load_config()
