#pragma once
#include <string>
#include <memory>
#include "yaml-cpp/yaml.h"
#include "ConfigModels.h"

class ConfigManager {
public:
    static ConfigManager& getInstance(const std::string& config_path = "config.yaml");

    AppConfig getAppConfig() const;

private:
    AppConfig appConfig;

    ConfigManager(const std::string& config_path);
    void loadConfig(const std::string& config_path);

    ConfigManager(const ConfigManager&) = delete;
    ConfigManager& operator=(const ConfigManager&) = delete;
};
