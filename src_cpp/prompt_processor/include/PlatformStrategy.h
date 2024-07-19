/**
 * @file PlatformStrategy.h
 * @brief Header file for the PlatformStrategy class, responsible for generating platform-specific prompts using templates.
 *
 * This file contains the declaration of the PlatformStrategy class, which is designed to generate
 * prompts based on templates for different platforms. The class utilizes the PromptTemplateParser
 * for parsing template files and allows for the replacement of placeholder values with actual data.
 *
 * The PlatformStrategy class provides the following functionalities:
 * - Initialization based on a specified platform.
 * - Loading of template files from disk.
 * - Generation of prompts with dynamic replacements.
 *
 * The class is constructed with a platform identifier, which it uses to determine the appropriate
 * template file path. It then loads the template file and uses the PromptTemplateParser to process
 * the template and generate the final prompt string based on the provided replacements map.
 *
 * @see PromptTemplateParser
 * @see PromptParams
 */
#pragma once

#include <string>
#include <unordered_map>
#include <memory>
#include <fstream>
#include "PromptParams.h"
#include "PromptTemplateParser.h"

/**
 * @class PlatformStrategy
 * @brief Class for generating platform-specific prompts using templates.
 *
 * The PlatformStrategy class is responsible for generating prompts based on templates for different platforms.
 * It utilizes the PromptTemplateParser for parsing the template files and allows for dynamic replacement of
 * placeholder values with actual data provided in a replacements map.
 */
class PlatformStrategy
{
public:
    /**
     * @brief Destructor for the PlatformStrategy class.
     *
     * Default destructor to clean up resources used by the PlatformStrategy class.
     */
    ~PlatformStrategy() = default;

    /**
     * @brief Constructor for the PlatformStrategy class.
     *
     * Initializes the PlatformStrategy object with a specified platform identifier.
     *
     * @param platform The platform identifier to determine the template file path.
     */
    PlatformStrategy(std::string_view platform);

    /**
     * @brief Generates a prompt based on the loaded template and replacements map.
     *
     * This function generates the final prompt string by replacing placeholders in the loaded template
     * with actual values provided in the replacements map.
     *
     * @param replacementsMap A map containing placeholder-value pairs for template replacement.
     * @return The generated prompt string with placeholders replaced by actual values.
     */
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap);

private:
    std::unique_ptr<PromptTemplateParser> template_str; ///< Unique pointer to the PromptTemplateParser instance.
    std::string filepath;                               ///< Path to the template file.
    std::string templateData;                           ///< Content of the loaded template file.

    /**
     * @brief Determines the file path for the template based on the platform identifier.
     *
     * This function generates the file path for the template file based on the provided platform identifier.
     *
     * @param platform The platform identifier used to determine the template file path.
     * @return The generated file path for the template file.
     */
    std::string getFilePath(const std::string_view &platform);

    /**
     * @brief Loads the template file from disk.
     *
     * This function loads the template file from the specified file path and stores its content in templateData.
     *
     * @param file_path The path to the template file.
     * @param templateData Reference to a string where the loaded template data will be stored.
     */
    void loadTemplate(const std::string &file_path, std::string &templateData);

    /**
     * @brief Initializes the PlatformStrategy object based on the platform identifier.
     *
     * This function initializes the PlatformStrategy object by determining the template file path
     * based on the platform identifier and loading the corresponding template file.
     *
     * @param platform The platform identifier used for initialization.
     */
    void initialize(const std::string_view &platform);
};