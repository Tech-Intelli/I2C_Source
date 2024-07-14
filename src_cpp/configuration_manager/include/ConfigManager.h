#pragma once
#include <string>
#include <memory>
#include "yaml-cpp/yaml.h"
#include "ConfigModels.h"
/**
 * @brief Class for managing configuration settings.
 * 
 * This class provides functionality to access and manage configuration settings.
 * It enforces a singleton pattern to ensure only one instance exists.
 * 
 * Public Methods:
 *  - static ConfigManager& getInstance(const std::string& config_path = "config.yaml"): Returns the singleton instance of ConfigManager.
 *  - AppConfig getAppConfig() const: Returns the application configuration.
 * 
 * Private Methods:
 *  - ConfigManager(const std::string& config_path): Constructor to initialize the ConfigManager with a specified configuration file path.
 *  - void loadConfig(const std::string& config_path): Loads the configuration settings from the specified file path.
 * 
 * Note: Copying and assignment of ConfigManager instances are disabled.
 */
class ConfigManager {
public:
    static std::shared_ptr<ConfigManager>& getInstance(const std::string& config_path = "config.yaml");

    AppConfig getAppConfig() const;

private:
    AppConfig appConfig;
    static std::shared_ptr<ConfigManager> m_instance;
    ConfigManager(const std::string& config_path);
    void loadConfig(const std::string& config_path);

    ConfigManager(const ConfigManager&) = delete;
    ConfigManager& operator=(const ConfigManager&) = delete;
};
