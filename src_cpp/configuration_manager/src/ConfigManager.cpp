#include "ConfigManager.h"

/**
 * Constructor for ConfigManager class.
 *
 * @param config_path The path to the configuration file.
 *
 * @return None
 *
 * @throws None
 */
ConfigManager::ConfigManager(const std::string& config_path) {
    loadConfig(config_path);
}

/**
 * Loads the configuration settings from the specified file path.
 *
 * @param config_path The path to the configuration file
 *
 * @throws YAML::ParserException if there is an error parsing the YAML file
 */
void ConfigManager::loadConfig(const std::string& config_path) {
    YAML::Node config = YAML::LoadFile(config_path);

    appConfig.multimodal.blip = config["multimodal"]["blip"].as<std::string>();
    appConfig.multimodal.vit = config["multimodal"]["vit"].as<std::string>();
    appConfig.multimodal.llava = config["multimodal"]["llava"].as<std::string>();

    appConfig.ollama.variants.phi3 = config["ollama"]["variants"]["phi3"].as<std::string>();
    appConfig.ollama.variants.llama3 = config["ollama"]["variants"]["llama3"].as<std::string>();
    appConfig.ollama.variants.gemma2 = config["ollama"]["variants"]["gemma2"].as<std::string>();
    appConfig.ollama.use = config["ollama"]["use"].as<std::string>();
    appConfig.ollama.temperature = config["ollama"]["temperature"].as<int>();
    appConfig.ollama.top_p = config["ollama"]["top_p"].as<float>();
    appConfig.ollama.stream = config["ollama"]["stream"].as<bool>();

    appConfig.image_compression.type = config["image_compression"]["type"].as<std::string>();
    appConfig.image_compression.compress = config["image_compression"]["compress"].as<bool>();
    appConfig.image_compression.compression_quality = config["image_compression"]["compression_quality"].as<int>();
    appConfig.image_compression.resize_factor = config["image_compression"]["resize_factor"].as<float>();

    appConfig.transform_config.resize = std::make_tuple(
        config["transform_config"]["resize"][0].as<int>(),
        config["transform_config"]["resize"][1].as<int>()
    );
    appConfig.transform_config.center_crop = config["transform_config"]["center_crop"].as<int>();

    appConfig.model_selection.model_name = config["model_selection"]["model_name"].as<std::string>();

    appConfig.chroma_db.blip = config["chroma_db"]["blip"].as<std::string>();
    appConfig.chroma_db.llava = config["chroma_db"]["llava"].as<std::string>();

    appConfig.validate();
}

/**
 * Returns the singleton instance of ConfigManager initialized with the provided config_path.
 * 
 * @param config_path The path to the configuration file.
 * @return A reference to the singleton instance of ConfigManager.
 */
ConfigManager& ConfigManager::getInstance(const std::string& config_path) {
    static ConfigManager instance(config_path);
    return instance;
}

/**
 * Returns the AppConfig object containing the application configuration settings.
 *
 * @return The AppConfig object representing the application configuration.
 */
AppConfig ConfigManager::getAppConfig() const {
    return appConfig;
}
