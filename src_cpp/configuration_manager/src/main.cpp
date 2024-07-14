#include <iostream>
#include "ConfigManager.h"

int main() {
    ConfigManager& configManager = ConfigManager::getInstance("config.yaml");
    AppConfig appConfig = configManager.getAppConfig();

    std::cout << "BLIP model name: " << appConfig.multimodal.blip << std::endl;

    return 0;
}
