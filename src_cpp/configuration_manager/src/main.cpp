#include <iostream>
#include "ConfigManager.h"

/**
 * Main function that initializes a ConfigManager instance with a YAML configuration file,
 * retrieves the AppConfig from the ConfigManager, and prints the BLIP model name from the AppConfig.
 *
 * @return 0 indicating successful execution
 *
 * @throws None
 */
int main() {
    std::shared_ptr<ConfigManager>& configManager = ConfigManager::getInstance("config.yaml");
    AppConfig appConfig = configManager->getAppConfig();

    std::cout << "BLIP model name: " << appConfig.multimodal.blip << std::endl;

    return 0;
}
